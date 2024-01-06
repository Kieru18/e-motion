import torch
import numpy as np
import json
from pycocotools.coco import COCO
from pathlib import Path
from collections import defaultdict
import numpy as np
import os


def load_coco_from_json(path):
    coco = COCO()
    with open(path) as json_file:
        json_data = json.load(json_file)
        coco.dataset = json_data
        coco.createIndex()
    return coco

def load_coco_from_prediction(prediction, categories, image_data):
    coco = COCO()

    coco.dataset = prediction
    coco.createIndex()
    return coco



def parse_image_json(label_data):
    # label_data = json.loads(label_task_json)
    coco = COCO()
    coco.dataset = label_data
    coco.createIndex()
    ids = list(sorted(coco.imgs.keys()))
    images, annotations = [], []

    for id in ids:
        img, ann = coco_image_data(coco, id)
        images.append(img)
        annotations.append(ann)

    return images, annotations


def coco_image_data(coco, img_id):
    # List: get annotation id from coco
    ann_ids = coco.getAnnIds(imgIds=img_id)
    # Dictionary: target coco_annotation file for an image
    coco_annotation = coco.loadAnns(ann_ids)

    # path for input image
    image_path = coco.loadImgs(img_id)[0]['file_name']

    # number of objects in the image
    num_objs = len(coco_annotation)

    boxes = []
    for i in range(num_objs):
        xmin = coco_annotation[i]['bbox'][0]
        ymin = coco_annotation[i]['bbox'][1]
        xmax = xmin + coco_annotation[i]['bbox'][2]
        ymax = ymin + coco_annotation[i]['bbox'][3]
        boxes.append([xmin, ymin, xmax, ymax])
    boxes = torch.as_tensor(boxes, dtype=torch.float32)

    labels = [sample["category_id"] for sample in coco_annotation]
    labels = torch.tensor(labels, dtype=torch.int64)
    img_id = torch.tensor([img_id])
    areas = []
    for i in range(num_objs):
        areas.append(coco_annotation[i]['area'])
    areas = torch.as_tensor(areas, dtype=torch.float32)
    iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

    # Annotation is in dictionary format
    my_annotation = {}
    my_annotation["boxes"] = boxes
    my_annotation["labels"] = labels
    my_annotation["image_id"] = img_id
    my_annotation["area"] = areas
    my_annotation["iscrowd"] = iscrowd

    return image_path, my_annotation


def serialize_predictions(image_shapes, predictions, image_paths, model_version, classes):
    return[
        image_predictions_to_id(path, model_version, shape, y, classes) for shape, y, path in zip(image_shapes, predictions, image_paths)
    ]
    

def image_predictions_to_id(image_path, model_version, image_shape, prediction, classes):
    classes_by_id = {i: c for i, c in enumerate(classes)}

    output = {
        "data": {},
        "predictions": [],
    }
    prediction_dict = {}

    output["data"]["image"] = image_path
    prediction_dict["model_version"] = model_version

    prediction_dict["result"] = parse_predictions(image_shape, prediction, classes_by_id)


    prediction_dict["score"] = prediction["scores"].mean().item()
    output["predictions"] = [prediction_dict]
    return output


def parse_predictions(image_shape, prediction, classes_by_id):
    metadata = {}
    _, image_height, image_width = image_shape
    metadata["original_width"] = image_width
    metadata["original_height"] = image_height

    metadata["image_rotation"] = 0
    metadata["from_name"] = "label"
    metadata["to_name"] = "image"
    metadata["type"] = "rectanglelabels"

    boxes = prediction["boxes"]
    labels = prediction["labels"]

    sample_predictions = []
    for i in range(len(boxes)):
        sample_dict = metadata.copy()
        sample_dict["id"] = str(i)

        sample_dict["value"] = sample_prediction_to_dict(image_shape, boxes[i], labels[i], classes_by_id)
        
        sample_predictions.append(sample_dict)

    return sample_predictions

def sample_prediction_to_dict(image_shape, bbox, label, classes_by_id):
    _, image_height, image_width = image_shape
    x0, y0, x1, y1 = bbox.tolist()

    x = x0 / image_width * 100
    y = y0 / image_height * 100
    
    width = (x1 - x0) / image_width * 100
    height = (y1 - y0) / image_height * 100

    return{
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "rotation": 0,
        "rectanglelabels": [ 
            classes_by_id[label.item()]
        ]
    }
