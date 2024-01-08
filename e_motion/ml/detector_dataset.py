import os
import torch

from torchvision.io import read_image
from torchvision.transforms.v2 import functional as F
from torch.utils.data import Dataset
from pycocotools.coco import COCO
from .data_utils import parse_image_json
import json

class DetectorDataset(Dataset):
    def __init__(self, root, transforms):
        self.root = root
        self.transforms = transforms
        
        with open(os.path.join(root, "result.json")) as f:
            json_data = json.load(f)
        self.img_paths, self.targets = parse_image_json(json_data)

        coco = COCO()
        coco.dataset = json_data
        coco.createIndex()
        
        self.coco = coco

    def __getitem__(self, idx):
        # load images and masks
        img_path = os.path.join(self.root, self.img_paths[idx])

        img = read_image(img_path)
        target = self.targets[idx]

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.img_paths)