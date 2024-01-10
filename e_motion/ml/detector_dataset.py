import os
import torch

from torchvision.io import read_image
from torchvision.transforms.v2 import functional as F
from torch.utils.data import Dataset
from pycocotools.coco import COCO
from .data_utils import parse_image_json
import json

class DetectorDataset(Dataset):
    def __init__(self, dataset_path, annotation_path, transforms=None, indices=None):
        self.indices = indices
        self.dataset_path = dataset_path
        self.annotation_path = annotation_path
        self.transforms = transforms
        
        with open(os.path.join(annotation_path, "result.json")) as f:
            json_data = json.load(f)
        self.img_paths, self.targets = parse_image_json(json_data)

        coco = COCO()
        coco.dataset = json_data
        coco.createIndex()
        
        self.coco = coco

    def __getitem__(self, idx):

        image_id = idx if not self.indices else self.indices[idx]
        # load images and masks
        img_path = os.path.join(self.dataset_path, self.img_paths[image_id])

        img = read_image(img_path)
        target = self.targets[image_id]

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.img_paths) if not self.indices else len(self.indices)