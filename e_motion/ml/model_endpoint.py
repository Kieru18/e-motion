from .detector_dataset import DetectorDataset
from .detector_module import CocoDetectorModule, CocoDetectorResnet, CocoDetectorABC
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
import ast
import pickle
from pathlib import Path

BATCH_SIZE = 2


def train(project_id: int, model_id: int) -> list[float]:
    """
    Train the object detection model.

    Args:
        project_id (int): ID of the project.
        model_id (int): ID of the model.

    Returns:
        list: COCO evaluation statistics.
    """

    model_django = load_model_params(model_id)

    print(f"Passed project_id: {project_id}, model_id: {model_id}")
    print("Initializing model...")
    try:
        model = initialize_model(model_id)
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
        dataset_path = dataset_path_from_id(project_id)
        annotation_path = annotation_path_from_id(model_id)
        dataset = DetectorDataset(dataset_path, annotation_path, get_transform())
        indices = torch.randperm(len(dataset)).tolist()

        val_size = model_django.validation_set_size
        indices_train = indices[:-val_size]
        indices_valid = indices[-val_size:]

        print(
            f"indices: {indices}, val_size: {val_size}, indices_train: {indices_train}, indices_valid: {indices_valid}"
        )
        print(f"Dataset size: {len(dataset)}, indices_train size: {len(indices_train)}")
        print(f"indices_valid size: {len(indices_valid)}")
    except Exception as e:
        print(e)
        raise e
    print("Dataset loaded.")

    print("Initializing coco loaders...")
    try:
        loader_train = initialize_coco_loader(
            dataset_path, annotation_path, BATCH_SIZE, True, indices_train
        )
        loader_valid = initialize_coco_loader(
            dataset_path, annotation_path, BATCH_SIZE, True, indices_valid
        )
    except Exception as e:
        print(e)
        raise e
    print("Coco loaders initialized.")

    print("Training the model...")
    try:
        trainer = L.Trainer(
            limit_train_batches=100, max_epochs=model_django.epochs, accelerator="auto"
        )
        trainer.fit(model=module, train_dataloaders=loader_train, val_dataloaders=loader_valid)
    except Exception as e:
        print(e)
        raise e
    print("Model training completed.")
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
        dataset_eval = DetectorDataset(
            dataset_path, annotation_path, get_transform(), indices_valid
        )
        result = evaluate_detector(model_id, module, dataset_eval)
    except Exception as e:
        print(e)
        raise e
    print("Model evaluation completed.")
    return result


def predict(project_id: int, model_id: int) -> dict:
    """
    Train the object detection model.

    Args:
        project_id (int): ID of the project.
        model_id (int): ID of the model.

    Returns:
        dict: COCO prediction dictionary
    """
    model_django = load_model_params(model_id)
    image_paths = image_paths_for_prediction(project_id, model_id)

    print(f"Image paths prediction: {image_paths}")
    buffer = io.BytesIO(model_django.checkpoint)
    model = initialize_model(model_id)
    model.load_state_dict(torch.load(buffer))

    module = CocoDetectorModule(model)

    images = [read_image(path) for path in image_paths]

    eval_transform = get_transform()
    transformed_images = [eval_transform(image) for image in images]

    shapes = [image.shape for image in images]
    print("Shapes:", shapes)
    predictions = module.predict(transformed_images)

    classes = project_classes(model_id)
    dataset_url = load_project_url(project_id)
    return serialize_predictions(shapes, predictions, image_paths, model_id, classes, dataset_url)


def evaluate_detector(model_id: int, model: CocoDetectorModule, dataset: DetectorDataset) -> list[float]:
    """
    Evaluate the object detection model using COCO evaluation.

    Args:
        model_id (int): ID of the model.
        model (CocoDetectorModule): Object detection model.
        dataset (DetectorDataset): COCO dataset for evaluation.

    Returns:
        list: COCO evaluation statistics.
    """
    model_django = load_model_params(model_id)

    coco_gt = dataset.coco

    images = [img for img, _ in dataset]
    pred = model.predict(images)
    coco_pred = load_coco_from_prediction(pred)

    # initialize the COCOeval object by passing the coco object with
    # ground truth annotations, coco object with detection results
    cocoEval = COCOeval(coco_gt, coco_pred, "bbox")

    # run evaluation for each image, accumulates per image results
    # display the summary metrics of the evaluation
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()

    model_django.miou_score = np.array(
        [max(x, 0) for x in list(cocoEval.stats[:5])]
    ).mean()
    model_django.top1_score = max(cocoEval.stats[:5])
    model_django.top5_score = min(cocoEval.stats[:5])

    print("Evaluation results:")
    print(
        f"miou_score: {model_django.miou_score}, top1_score: {model_django.top1_score}, top5_score: {model_django.top5_score}"
    )
    model_django.save(update_fields=["miou_score", "top1_score", "top5_score"])
    print("Evaluation results saved.")

    return cocoEval.stats


def image_paths_for_prediction(project_id: int, model_id: int):
    """
    Get unlabeled image paths for prediction.

    Args:
        project_id (int): ID of the project.
        model_id (int): ID of the model.

    Returns:
        set[str]: Unlabeled image paths.
    """

    dataset_path = dataset_path_from_id(project_id)
    json_path = os.path.join(
        annotation_path_from_id(model_id), "result.json"
    )

    with open(json_path) as json_file:
        json_data = json.load(json_file)
        annotation_list = json_data["annotations"]
        labeled_image_ids = set(data["image_id"] for data in annotation_list)

        labeled_image_paths = [
            os.path.join(dataset_path, Path(image["file_name"]).name)
            for image in json_data["images"] if image["id"] in labeled_image_ids
        ]

    all_image_names = os.listdir(dataset_path)
    all_image_paths = [os.path.join(dataset_path, name) for name in all_image_names]
    unlabeled_image_paths = set(all_image_paths) - set(labeled_image_paths)

    return unlabeled_image_paths


def project_classes(model_id: int):
    """
    Get the list of classes from the annotation file of the model.

    Args:
        model_id (int): ID of the model.

    Returns:
        list: List of class names.
    """

    json_path = os.path.join(
        annotation_path_from_id(model_id), "result.json"
    )
    with open(json_path) as json_file:
        json_data = json.load(json_file)
    return [category["name"] for category in json_data["categories"]]


def initialize_model(model_id: int):
    """
    Initialize the object detection model.

    Args:
        model_id (int): ID of the model.

    Returns:
        CocoDetectorResnet: Initialized object detection model.
    """
    print("loaded model params (initialize_model())")
    num_classes = len(project_classes(model_id))
    print(f"num_classes: {num_classes}, initialize_model()")
    return CocoDetectorResnet(num_classes, 0.1)


def initialize_optimizer(model: CocoDetectorABC, model_id: int):
    """
    Initialize the optimizer for the object detection model.

    Args:
        model: Object detection model.
        model_id (int): ID of the model.

    Returns:
        torch.optim.AdamW: Initialized optimizer.
    """
    model_params = load_model_params(model_id)
    return optim.AdamW(
        model.parameters(),
        lr=model_params.learning_rate,
        weight_decay=model_params.weight_decay,
    )


def initialize_coco_loader(
    dataset_path: str, annotation_path: str, batch_size: int, is_shuffled: bool = False, indices: list[int] | None = None
):
    """
    Initialize COCO DataLoader for the object detection dataset.

    Args:
        dataset_path (str): Path to the dataset.
        annotation_path (str): Path to the annotation file.
        batch_size (int): Batch size.
        is_shuffled (bool): Flag for shuffling the dataset.
        indices (list): List of indices to subset the dataset.

    Returns:
        DataLoader: COCO DataLoader.
    """
    dataset = DetectorDataset(dataset_path, annotation_path, get_transform())

    if indices != None:
        dataset = Subset(dataset, indices)

    print(f"dataset size: {len(dataset)}")

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=is_shuffled,
        num_workers=0,
        collate_fn=collate_fn,
    )


def get_transform():
    transforms = []
    transforms.append(T.ToDtype(torch.float, scale=True))
    transforms.append(T.ToPureTensor())
    return T.Compose(transforms)


def collate_fn(batch):
    return tuple(zip(*batch))


def dataset_path_from_id(project_id: int):
    """
    Get the dataset path based on the project ID.

    Args:
        project_id (int): ID of the project.

    Returns:
        str: Dataset path.
    """
    current_directory = os.getcwd()
    return os.path.join(
        current_directory, "uploads", "datasets", str(project_id)
    )


def annotation_path_from_id(model_id: int):
    """
    Get the annotation path based on the model ID.

    Args:
        model_id (int): ID of the model.

    Returns:
        str: Annotation path.
    """
    current_directory = os.getcwd()
    return os.path.join(
        current_directory, "uploads", "annotations", str(model_id)
    )


def load_model_params(model_id: int):
    """
    Load model parameters from the database.

    Args:
        model_id (int): ID of the model.

    Returns:
        LearningModel: Model parameters.
    """
    print("Loading model params... (load_model_params())")
    return LearningModel.objects.get(pk=model_id)


def load_project_url(project_id: int):
    """
    Load project url from the database.

    Args:
        project_id (int): ID of the project.

    Returns:
        Int: Dataset url.
    """
    print("Loading model params... (load_model_params())")
    return int(Project.objects.get(pk=project_id).dataset_url)
