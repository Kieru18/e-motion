from .detector_dataset import DetectorDataset
from .detector_module import CocoDetectorModule, CocoDetectorResnet
from torch.utils.data import DataLoader, Subset
import json
import lightning as L
import os
from pycocotools.cocoeval import COCOeval
from .data_utils import load_coco_from_prediction, serialize_predictions
from torchvision.io import read_image
from torchvision.transforms import v2 as T
from ..api.models import LearningModel, Project
import torch
import torch.optim as optim
import numpy as np
from pathlib import Path

BATCH_SIZE = 2

def train(project_id, model_id):
    model_django = load_model_params(model_id)

    model = initialize_model(model_id)
    module = CocoDetectorModule(model)
    
    images = images_from_paths(labeled_image_paths(project_id, model_id))

    indices = torch.randperm(len(images)).tolist()
    val_size = int(len(images) * 0.5)
    indices_train = indices[:-val_size]
    indices_valid = indices[-val_size:]


    loader_train = initialize_coco_loader(project_id, model_id, BATCH_SIZE, True, indices_train)
    loader_valid = initialize_coco_loader(project_id, model_id, BATCH_SIZE, True, indices_valid)

    trainer = L.Trainer(limit_train_batches=100, max_epochs=2, accelerator="gpu")
    trainer.fit(model=module, train_dataloaders=loader_train)

    # trainer.save_checkpoint(model_checkpoint_from_id(model_id))
    checkpoint = model.state_dict()
    model_django.checkpoint = checkpoint
    model_django.save(update_fields=["checkpoint"]) 
    
    return evaluate_detector(module, loader_valid.dataset)

def predict(project_id, model_id):
    model_django = load_model_params(model_id)

    # checkpoint_path = model_checkpoint_from_id(model_id)
    model = initialize_model(model_id).load_state_dict(model_django.checkpoint)
    module = CocoDetectorModule(model)

    image_paths = unlabeled_image_paths(project_id, model_id)
    images = images_from_paths(image_paths)

    eval_transform = get_transform()
    transformed_images = [eval_transform(image) for image in images]

    shapes = [image.shape for image in images]
    predictions = module.predict(transformed_images)

    classes = project_classes(model_id)

    return serialize_predictions(shapes, predictions, image_paths, model_id, classes)


def evaluate_detector(model_id, model: CocoDetectorModule, dataset):
    model_django = load_model_params(model_id)

    coco_gt = dataset.coco
    
    images = [img for img, _ in dataset]
    pred = model.predict(images)
    coco_pred = load_coco_from_prediction(pred, coco_gt.cats, coco_gt.imgs)

    # initialize the COCOeval object by passing the coco object with
    # ground truth annotations, coco object with detection results
    cocoEval = COCOeval(coco_gt, coco_pred, "bbox")

    # run evaluation for each image, accumulates per image results
    # display the summary metrics of the evaluation
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()

    model_django.miou_score = np.array([max(x, 0) for x in list(cocoEval.stats[:5])]).mean()
    model_django.top1_score = max(cocoEval.stats[:5])
    model_django.top5_score = min(cocoEval.stats[:5])

    model_django.save(update_fields=["miou_score", "top1_score", "top5_score"])

    return cocoEval.stats


def images_from_paths(image_paths):
    return [read_image(path) for path in image_paths]


def labeled_image_paths(project_id, model_id):
    images_path = project_image_paths_from_id(project_id)
    
    labeled_paths = model_labels(model_id)["images"]
    labeled_names = [Path(path["file_name"]).name for path in labeled_paths]
    
    return list(filter(lambda x: Path(x).name in labeled_names, images_path))


def unlabeled_image_paths(project_id, model_id):
    all_images_path = project_image_paths_from_id(project_id)

    labeled_paths = labeled_image_paths(project_id, model_id)
    unlabeled_paths = set(all_images_path) - set(labeled_paths)
    
    return list(unlabeled_paths)


def project_classes(model_id):
    labels_data = model_labels(model_id)
    return [category["name"] for category in labels_data["categories"]]


def initialize_model(model_id):
    model_params = load_model_params(model_id)  # TODO thresh in params
    num_classes = len(project_classes(model_id))
    return CocoDetectorResnet(num_classes, 0.1)


def initialize_optimizer(model, model_id):
        model_params = load_model_params(model_id)
        return optim.AdamW(
            model.parameters(),
            lr=model_params.learning_rate,
            weight_decay=model_params.weight_decay,
        )


def initialize_coco_loader(project_id, model_id, batch_size, is_shuffled=False, indices=None):
    image_paths = labeled_image_paths(project_id, model_id)
    images = images_from_paths(image_paths)

    dataset = DetectorDataset(images, model_labels(model_id), get_transform())
    
    if indices != None:
        dataset = Subset(dataset, indices)

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=is_shuffled,
        num_workers=0,
        collate_fn=collate_fn
    )


def get_transform():
    transforms = []
    transforms.append(T.ToDtype(torch.float, scale=True))
    transforms.append(T.ToPureTensor())
    return T.Compose(transforms)

def collate_fn(batch):
    return tuple(zip(*batch))


def model_labels(model_id):
    root = project_root_from_id()
    labels_path = os.path.join(root, "annotations", str(model_id), "result.json")
    labels_data = None
    with open(labels_path) as json_file:
        labels_data = json.load(json_file)
    return labels_data


def project_image_paths_from_id(project_id):
    root = project_root_from_id()
    dataset_path = os.path.join(root, "datasets", str(project_id))
    image_names = os.listdir(dataset_path)
    return [os.path.join(dataset_path, name) for name in image_names]


def project_root_from_id(project_id):
    project = Project.objects.get(pk=project_id)
    return f"uploads/{project.dataset_url}"


def load_model_params(model_id):
    return LearningModel.objects.get(pk=model_id)