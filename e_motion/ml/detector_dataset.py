import os
import torch

from torchvision.io import read_image
from torchvision.transforms.v2 import functional as F
from torch.utils.data import Dataset
from pycocotools.coco import COCO
from .data_utils import parse_image_json
import json

class DetectorDataset(Dataset):
    def __init__(self, images, label_data, transforms):
        self.transforms = transforms
        
        self.targets = parse_image_json(label_data)
        self.images = images

        coco = COCO()
        coco.dataset = label_data
        coco.createIndex()
        
        self.coco = coco

    def __getitem__(self, idx):
        # load images and masks
        img = self.images[idx]
        target = self.targets[idx]

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.images)