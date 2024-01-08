from typing import Any
from lightning.pytorch.utilities.types import STEP_OUTPUT
import torch.nn as nn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor, fasterrcnn_resnet50_fpn, fasterrcnn_resnet50_fpn_v2
import torch.optim as optim
import lightning as L
import torch
import torchvision
from abc import ABC, abstractmethod

# apply Non-Maximum Supression to prediction
def apply_nms(orig_prediction, iou_thresh):
    # torchvision returns the indices of the bboxes to keep
    keep = torchvision.ops.nms(orig_prediction['boxes'], orig_prediction['scores'], iou_thresh)
    
    final_prediction = orig_prediction
    final_prediction['boxes'] = final_prediction['boxes'][keep]
    final_prediction['scores'] = final_prediction['scores'][keep]
    final_prediction['labels'] = final_prediction['labels'][keep]

    return final_prediction


class CocoDetectorABC(nn.Module):
    def __init__(self, num_classes, iou_thresh,  **kwargs) -> None:
        super().__init__(**kwargs)
        self.num_classes = num_classes
        self.iou_thresh = iou_thresh
        self.model = self._initialize_model()

    @abstractmethod
    def _initialize_model(self):
        pass

    def forward(self, x, y):
        return self.model(x, y)
    
    def predict(self, x):
        y_hat = list(self.model(x))

        predictions = []
        for sample in y_hat:
            predictions.append(apply_nms(sample, self.iou_thresh))
        return predictions

class CocoDetectorResnet(CocoDetectorABC):
    def __init__(self, num_classes, iou_thresh, **kwargs) -> None:
        super().__init__(num_classes, iou_thresh, **kwargs)

    def _initialize_model(self):
        model = fasterrcnn_resnet50_fpn(weights="DEFAULT")
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, self.num_classes)
        return model


class CocoDetectorModule(L.LightningModule):
    def __init__(self, model: CocoDetectorABC):
        super().__init__()
        self.model = model

    def training_step(self, batch, batch_idx):
        self.model.train()
        loss_value = self._model_loss(batch, True)

        self.log("train_loss", loss_value)

        return loss_value
    
    def validation_step(self, batch, batch_idx) -> STEP_OUTPUT:
        self.model.train()
        loss_value = self._model_loss(batch, False)

        self.log("valid_loss", loss_value)

        return loss_value
    
    def test_step(self, batch, batch_idx) -> STEP_OUTPUT:
        self.model.train()
        loss_value = self._model_loss(batch, False)

        self.log("test_loss", loss_value)

        return loss_value
    
    def _model_loss(self, batch, is_training):
        x, y = batch
        self.model.train()

        images = list(image.to(self.device) for image in x)
        targets = [{k: v.to(self.device) if isinstance(v, torch.Tensor) else v for k, v in t.items()} for t in y]
        with torch.cuda.amp.autocast():
            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

        if not is_training:
            self.optimizers().zero_grad()

        return losses
    
    def predict(self, x) -> Any:
        self.model.eval()
        return self.model.predict(x)

    def configure_optimizers(self):
        optimizer = optim.SGD(
            self.model.parameters(),
            lr=0.0001,
            momentum=0.9,
            weight_decay=0.0005
        )
        return optimizer