from typing import Any
from lightning.pytorch.utilities.types import STEP_OUTPUT
import torch.nn as nn
from torchvision.models.detection.faster_rcnn import (
    FastRCNNPredictor,
    fasterrcnn_resnet50_fpn,
    fasterrcnn_resnet50_fpn_v2,
)
import torch.optim as optim
import lightning as L
import torch
import torchvision
from abc import ABC, abstractmethod

# apply Non-Maximum Supression to prediction
def apply_nms(orig_prediction, iou_thresh):
    # torchvision returns the indices of the bboxes to keep
    keep = torchvision.ops.nms(
        orig_prediction["boxes"], orig_prediction["scores"], iou_thresh
    )

    final_prediction = orig_prediction
    final_prediction["boxes"] = final_prediction["boxes"][keep]
    final_prediction["scores"] = final_prediction["scores"][keep]
    final_prediction["labels"] = final_prediction["labels"][keep]

    return final_prediction


class CocoDetectorABC(nn.Module):
    """
    Abstract base class for the COCO Detector.

    Args:
        num_classes (int): Number of classes in the dataset.
        iou_thresh (float): IoU threshold for non-maximum suppression.
        **kwargs: Additional keyword arguments.

    Attributes:
        num_classes (int): Number of classes.
        iou_thresh (float): IoU threshold for NMS.
        model: Model to be initialized in subclasses.
    """
    def __init__(self, num_classes, iou_thresh, **kwargs) -> None:
        super().__init__(**kwargs)
        self.num_classes = num_classes
        self.iou_thresh = iou_thresh
        self.model = self._initialize_model()

    @abstractmethod
    def _initialize_model(self):
        """
        Abstract method for initializing the model.
        """

    def forward(self, x, y):
        """
        Forward pass of the model.

        Args:
            x: Input tensor.
            y: Ground truth tensor.

        Returns:
            Model output.
        """
        return self.model(x, y)

    def predict(self, x):
        """
        Make predictions using the model.

        Args:
            x: Input tensor.

        Returns:
            list: List of final predictions after NMS.
        """
        y_hat = list(self.model(x))

        predictions = []
        for sample in y_hat:
            predictions.append(apply_nms(sample, self.iou_thresh))
        return predictions


class CocoDetectorResnet(CocoDetectorABC):
    """
    Subclass of CocoDetectorABC for ResNet-based object detection model.

    Args:
        num_classes (int): Number of classes in the dataset.
        iou_thresh (float): IoU threshold for non-maximum suppression.
        **kwargs: Additional keyword arguments.
    """
    def __init__(self, num_classes, iou_thresh, **kwargs) -> None:
        super().__init__(num_classes, iou_thresh, **kwargs)

    def _initialize_model(self):
        """
        Initialize the ResNet-based object detection model.

        Returns:
            torchvision.models.detection.FasterRCNN: Initialized FasterRCNN model.
        """
        model = fasterrcnn_resnet50_fpn(weights="DEFAULT")
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, self.num_classes)
        return model


class CocoDetectorModule(L.LightningModule):
    """
    Lightning Module for training, validation, and testing of the COCO Detector.

    Args:
        model (CocoDetectorABC): COCO Detector model.

    Attributes:
        model (CocoDetectorABC): COCO Detector model.
    """


    def __init__(self, model: CocoDetectorABC):
        super().__init__()
        self.model = model

    def training_step(self, batch, batch_idx):
        """
        Training step for Lightning Module.

        Args:
            batch: Batch of training data.
            batch_idx (int): Batch index.

        Returns:
            torch.Tensor: Loss value for training.
        """
        self.model.train()
        loss_value = self._model_loss(batch, True)

        self.log("train_loss", loss_value)

        return loss_value

    def validation_step(self, batch, batch_idx) -> STEP_OUTPUT:
        """
        Validation step for Lightning Module.

        Args:
            batch: Batch of validation data.
            batch_idx (int): Batch index.

        Returns:
            torch.Tensor: Loss value for validation.
        """
        self.model.train()
        loss_value = self._model_loss(batch, False)

        self.log("valid_loss", loss_value)

        return loss_value

    def test_step(self, batch, batch_idx) -> STEP_OUTPUT:
        """
        Test step for Lightning Module.

        Args:
            batch: Batch of test data.
            batch_idx (int): Batch index.

        Returns:
            torch.Tensor: Loss value for testing.
        """
        self.model.train()
        loss_value = self._model_loss(batch, False)

        self.log("test_loss", loss_value)

        return loss_value

    def _model_loss(self, batch, is_training):
        """
        Compute the loss for the object detection model.

        Args:
            batch: Input batch data.
            is_training (bool): Flag indicating whether it is a training step.

        Returns:
            torch.Tensor: Loss value.
        """

        x, y = batch
        self.model.train()

        images = list(image.to(self.device) for image in x)
        targets = [
            {
                k: v.to(self.device) if isinstance(v, torch.Tensor) else v
                for k, v in t.items()
            }
            for t in y
        ]
        with torch.cuda.amp.autocast():
            loss_dict = self.model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

        if not is_training:
            self.optimizers().zero_grad()

        return losses

    def predict(self, x) -> Any:
        """
        Perform predictions using the model.

        Args:
            x: Input data.

        Returns:
            List[dict]: List of final predictions after NMS.
        """
        self.model.eval()
        return self.model.predict(x)

    def configure_optimizers(self):
        """
        Configure the optimizer for the Lightning Module.

        Returns:
            torch.optim.Optimizer: The optimizer for the model training.
        """
        optimizer = optim.SGD(
            self.model.parameters(), lr=0.0001, momentum=0.9, weight_decay=0.0005
        )
        return optimizer
