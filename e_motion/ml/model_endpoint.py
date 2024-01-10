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
from api.models import LearningModel, Project
import torch
import torch.optim as optim
import numpy as np
import io

BATCH_SIZE = 2

def train(project_id, model_id):
    model_django = load_model_params(model_id)

    print(f"Passed project_id: {project_id}, model_id: {model_id}")
    print("Initializing model...")
    try:
        model = initialize_model(project_id, model_id)
    except Exception as e:
        print(e)
        raise e
    print("Model initialized.")

    print("CocoDetectorModule about to be loaded.")
    try:
        module = CocoDetectorModule(model)
    except Exception as e:
        print(e)
        raise e
    print("CocoDetectorModule loaded.")

    print("Loading Dataset...")
    try:
        # project_root = project_root_from_id(project_id)
        dataset_path = dataset_path_from_id(project_id)
        annotation_path = annotation_path_from_id(model_id)
        dataset = DetectorDataset(dataset_path, annotation_path, get_transform())
        indices = torch.randperm(len(dataset)).tolist()
        # val_size = len(dataset) * model_django.validation_set_size #?
        val_size = model_django.validation_set_size
        indices_train = indices[:-val_size]
        indices_valid = indices[-val_size:]
        print(f"indices: {indices}, val_size: {val_size}, indices_train: {indices_train}, indices_valid: {indices_valid}")
        print(f"Dataset size: {len(dataset)}, indices_train size: {len(indices_train)}") 
        print(f"indices_valid size: {len(indices_valid)}")
    except Exception as e:
        print(e)
        raise e
    print("Dataset loaded.")

    print("Initializing coco loaders...")
    try:
        loader_train = initialize_coco_loader(dataset_path, annotation_path, BATCH_SIZE, 
                                              True, indices_train)
        loader_valid = initialize_coco_loader(dataset_path, annotation_path, BATCH_SIZE, 
                                              True, indices_valid)
    except Exception as e:
        print(e)
        raise e
    print("Coco loaders initialized.")

    print("Training the model...")
    trainer = L.Trainer(limit_train_batches=100, max_epochs=model_django.epochs, 
                        accelerator="gpu")
    trainer.fit(model=module, train_dataloaders=loader_train)
    print("Model training completed.")

    # trainer.save_checkpoint(model_checkpoint_from_id(model_id))
    print("Saving the model...")
    try:
        checkpoint = model.state_dict()
        # Convert checkpoint to bytes
        buffer = io.BytesIO()
        torch.save(checkpoint, buffer)
        checkpoint_bytes = buffer.getvalue()
        model_django.checkpoint = checkpoint_bytes
        model_django.save(update_fields=["checkpoint"]) 
    except Exception as e:
        print(e)
        raise e
    print("Model saved.")

    print("Evaluating the model...")
    try:
        result = evaluate_detector(model_id, module, loader_valid.dataset)
    except Exception as e:
        print(e)
        raise e
    print("Model evaluation completed.")
    return result

def predict(project_id, model_id):
    dataset_path = dataset_path_from_id(project_id)
    # root = project_root_from_id(project_id)
    model_django = load_model_params(model_id)

    # checkpoint_path = model_checkpoint_from_id(model_id)
    model = initialize_model(project_id, model_id).load_state_dict(model_django.checkpoint)
    module = CocoDetectorModule(model)

    image_paths = image_paths_for_prediction(project_id, model_id)
    images = [read_image(path) for path in image_paths]

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


def image_paths_for_prediction(project_id, model_id):
    # root = project_root_from_id(project_id)
    dataset_path = dataset_path_from_id(project_id)
    json_path = annotation_path_from_id(model_id) + "/result.json" # hardcoded annotation file name
    # labels_path = project_labels_path_from_id(project_id)
    
    with open(json_path) as json_file:
        json_data = json.load(json_file)
        labeled_image_paths = [os.path.join(dataset_path, image["file_name"]) 
                               for image in json_data["images"]]
    all_image_names = os.listdir(dataset_path)
    all_image_paths = [os.path.join(dataset_path, name) for name in all_image_names]
    unlabeled_image_paths = set(all_image_paths) - set(labeled_image_paths)
    
    return unlabeled_image_paths

def project_classes(model_id):
    # json_path = project_labels_path_from_id(project_id)
    json_path = annotation_path_from_id(model_id) + "/result.json" # hardcoded annotation file name
    with open(json_path) as json_file:
        json_data = json.load(json_file)
    return [category["name"] for category in json_data["categories"]]

def initialize_model(project_id, model_id):
    model_params = load_model_params(model_id)  # TODO thresh in params
    print("loaded model params (initialize_model())")
    num_classes = len(project_classes(model_id))
    print(f"num_classes: {num_classes}, initialize_model()")
    return CocoDetectorResnet(num_classes, 0.1)

def initialize_optimizer(model, model_id):
        model_params = load_model_params(model_id)
        return optim.AdamW(
            model.parameters(),
            lr=model_params.learning_rate,
            weight_decay=model_params.weight_decay,
        )


def initialize_coco_loader(dataset_path, annotation_path, batch_size, is_shuffled=False, 
                           indices=None):
    # project_root = project_root_from_id(project_id)
    dataset = DetectorDataset(dataset_path, annotation_path, get_transform())
    
    if indices != None:
        dataset = Subset(dataset, indices)

    print(f"dataset size: {len(dataset)}")

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


# def project_labels_path_from_id(project_id):
#     root = project_root_from_id(project_id)
#     return os.path.join(root, "result.json")


# def project_root_from_id(project_id):
#     project = Project.objects.get(pk=project_id)
#     return f"uploads/{project.dataset_url}"

def dataset_path_from_id(project_id):
    current_directory = os.getcwd()
    print(f"{current_directory}, dataset_path_from_id()")
    return f"{current_directory}/uploads/datasets/{project_id}"

def annotation_path_from_id(model_id):
    current_directory = os.getcwd()
    print(f"{current_directory}, annotation_path_from_id()")
    return f"{current_directory}/uploads/annotations/{model_id}"


# def model_checkpoint_from_id(model_id):
#     return os.path.join(os.curdir, "models", model_id, "checkpoint.cpt")


def load_model_params(model_id):
    print("Loading model params... (load_model_params())")
    return LearningModel.objects.get(pk=model_id)