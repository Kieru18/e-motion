import os
import torch

from torchvision.io import read_image
from torchvision.transforms.v2 import functional as F
from torch.utils.data import Dataset
from pycocotools.coco import COCO
from .data_utils import parse_image_json
import json


class DetectorDataset(Dataset):
    """
    Dataset class for object detection.

    Args:
        dataset_path (str): Path to the dataset.
        annotation_path (str): Path to the annotation file.
        transforms (callable, optional): Optional transforms to be applied to the data.
        indices (list, optional): List of indices to subset the dataset.

    Attributes:
        indices (list): List of indices to subset the dataset.
        dataset_path (str): Path to the dataset.
        annotation_path (str): Path to the annotation file.
        transforms (callable, optional): Optional transforms to be applied to the data.
        img_paths (list): List of image paths.
        targets (list): List of targets.
        coco (pycocotools.coco.COCO): COCO object for indexing.

    Methods:
        __getitem__: Get a specific item from the dataset.
        __len__: Get the length of the dataset.
    """

    def __init__(self, dataset_path, annotation_path, transforms=None, indices=None):
        """
        Initialize the DetectorDataset.

        Args:
            dataset_path (str): Path to the dataset.
            annotation_path (str): Path to the annotation file.
            transforms (callable, optional): Optional transforms to be applied to the data.
            indices (list, optional): List of indices to subset the dataset.
        """
        
        self.indices = indices
        self.dataset_path = dataset_path
        self.annotation_path = annotation_path
        self.transforms = transforms

        with open(os.path.join(annotation_path, "result.json")) as f:
            json_data = json.load(f)
        
        json_data["images"] = self._training_image_data(json_data) 
        self.img_paths, self.targets = parse_image_json(json_data)

        coco = COCO()
        coco.dataset = json_data
        coco.createIndex()

        self.coco = coco

    def _training_image_data(self, json_data):
        annotation_list = json_data["annotations"]
        labeled_ids = set(data["image_id"] for data in annotation_list)
        return [data for data in json_data["images"] if data["id"] in labeled_ids]

    def __getitem__(self, idx):
        """
        Get a specific item from the dataset.

        Args:
            idx (int): Index of the item.

        Returns:
            tuple: Tuple containing the image and its target.
        """

        image_id = idx if not self.indices else self.indices[idx]
        # load images and masks
        img_path = os.path.join(self.dataset_path, self.img_paths[image_id])

        img = read_image(img_path)
        target = self.targets[image_id]

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        """
        Get the length of the dataset.

        Returns:
            int: Length of the dataset.
        """
        
        return len(self.img_paths) if not self.indices else len(self.indices)
