from django.test import TestCase
from ml.model_endpoint import initialize_optimizer, load_model_params
from ml.detector_module import CocoDetectorResnet, CocoDetectorModule
from ml.data_utils import parse_image_json, serialize_predictions, image_predictions_to_id, parse_predictions, sample_prediction_to_dict
from api.models import LearningModel, Project, User
import torch
# Create your tests here.
class DataParsingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test', password='test')
        project = Project.objects.create(title='title', description='desc', label_studio_project='1', user=user)

        LearningModel.objects.create(
            name = "name",
            learning_rate = 0.01,
            weight_decay = 1e-7,
            epochs = 2,
            project = project
        )

    def _create_annotaton(self, id, image_id, category_id, bbox):
        x0, y0, x1, y1 = bbox
        return {
            "id": id,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": [],
            "bbox": [
                x0,
                y0,
                x1,
                y1
            ],
            "ignore": 0,
            "iscrowd": 0,
            "area": 41832.81222497799,
            }
    
    def _create_categories(self, names):
        return [
            {"id": i, "name": name} for i, name in enumerate(names)
        ]


    def _create_labeled_data(self):
        bbox_0 = [18.1, 41.7, 221.3, 189.]
        bbox_1 = [179.6, 177.9, 192., 189.]
        return {
            "images": [
                {
                "width": 600,
                "height": 403,
                "id": 0,
                "file_name": "images\\sample.jpg"
                }
            ],
            "categories": self._create_categories(["A", "B"]),
            "annotations": [
                self._create_annotaton(0, 0, 0, bbox_0),
                self._create_annotaton(1, 0, 1, bbox_1),
            ]
        }


    def _create_model(self, num_classes):
        return CocoDetectorResnet(num_classes, 0.1)


    def test_create_optimizer(self):
        model = self._create_model(2)
        initialize_optimizer(model, 1)

    def test_create_detector_module(self):
        model = self._create_model(2)
        CocoDetectorModule(model)

    def test_parsing_image_json(self):
        labeled_data = self._create_labeled_data()
        parsed_data = parse_image_json(labeled_data)
        self.assertEqual(2, len(parsed_data))

        img_path, annotations = parsed_data
        
        self.assertEqual(1, len(img_path))
        self.assertEqual((2, 4), annotations[0]["boxes"].shape)
        self.assertEqual((2,), annotations[0]["labels"].shape)

    def test_serialize_predictions(self):
        image_shapes = [(3, 600, 403)]
        labeled_data = self._create_labeled_data()
        classes = ["A", "B"]
        img_path, annotations = parse_image_json(labeled_data)
        annotations[0]["scores"] = torch.tensor([0.5, 1])
        
        serialized_preds = serialize_predictions(image_shapes, annotations, img_path, "v", classes, 5)

        preds = serialized_preds[0]["predictions"][0]
        self.assertAlmostEqual(0.75, preds["score"])
        self.assertEqual(1, len(serialized_preds))
        self.assertEqual(2, len(preds["result"]))
