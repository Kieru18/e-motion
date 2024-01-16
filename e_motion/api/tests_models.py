from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Project, LearningModel
from django.contrib.auth.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test', password='test')

    def test_username(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')
        self.assertEqual(user.username, 'test')

    def test_email_field(self):
        user = User.objects.get(id=1)
        email_field = user._meta.get_field('email')
        self.assertFalse(email_field.null)
        self.assertTrue(email_field.blank)

    def test_superuser(self):
        superuser = User.objects.create_superuser('admin', 'admin@admin.com', 'adminpass')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_string_representation(self):
        user = User.objects.get(id=1)
        self.assertEqual(str(user), 'test')

    def test_user_verbose_name_plural(self):
        self.assertEqual(User._meta.verbose_name_plural, 'users')

    def test_user_first_name(self):
        user = User.objects.get(id=1)
        user.first_name = 'John'
        user.save()
        self.assertEqual(user.first_name, 'John')

    def test_user_last_name(self):
        user = User.objects.get(id=1)
        user.last_name = 'Doe'
        user.save()
        self.assertEqual(user.last_name, 'Doe')


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test', password='test')
        Project.objects.create(title='title', description='desc', label_studio_project='1', user=user)

    def test_fields_values(self):
        project = Project.objects.get(id=1)
        self.assertEqual(project.id, 1)
        self.assertEqual(project.project_id, 1)
        self.assertEqual(project.title, 'title')
        self.assertEqual(project.description, 'desc')
        self.assertEqual(project.label_studio_project, '1')

    def test_foreign_key(self):
        project = Project.objects.get(id=1)
        user = User.objects.get(id=1)
        self.assertEqual(project.user, user)

    def test_title_constraints(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('title').max_length
        nullable = project._meta.get_field('title').null
        self.assertEqual(max_length, 100)
        self.assertFalse(nullable)

    def test_description_constraints(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('description').max_length
        nullable = project._meta.get_field('description').null
        self.assertEqual(max_length, 250)
        self.assertTrue(nullable)

    def test_label_studio_project_constraints(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('label_studio_project').max_length
        nullable = project._meta.get_field('label_studio_project').null
        self.assertEqual(max_length, 150)
        self.assertTrue(nullable)

    def test_description_default_value(self):
        project = Project.objects.create(title='title2', label_studio_project='3', user=User.objects.get(id=1))
        self.assertIsNone(project.description)


class LearningModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test', password='test')
        project = Project.objects.create(title='title', description='desc', label_studio_project='1', user=user)
        LearningModel.objects.create(name='model',
                                     architecture='Faster RCNN',
                                     learning_rate=0.0001,
                                     weight_decay=0.9,
                                     epochs=200,
                                     validation_set_size=2,
                                     project=project)

    def test_fields_values(self):
        model = LearningModel.objects.get(id=1)
        self.assertEqual(model.id, 1)
        self.assertEqual(model.model_id, 1)
        self.assertEqual(model.name, 'model')
        self.assertEqual(model.learning_rate, 0.0001)
        self.assertEqual(model.weight_decay, 0.9)
        self.assertEqual(model.epochs, 200)
        self.assertEqual(model.validation_set_size, 2)

    def test_foreign_key(self):
        project = Project.objects.get(id=1)
        model = LearningModel.objects.get(id=1)
        self.assertEqual(model.project, project)

    def test_name_constraints(self):
        model = LearningModel.objects.get(id=1)
        max_length = model._meta.get_field('name').max_length
        nullable = model._meta.get_field('name').null
        self.assertEqual(max_length, 60)
        self.assertFalse(nullable)

    def test_architecture_constraints(self):
        model = LearningModel.objects.get(id=1)
        max_length = model._meta.get_field('architecture').max_length
        nullable = model._meta.get_field('architecture').null
        self.assertEqual(max_length, 60)
        self.assertFalse(nullable)

    def test_lr_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('learning_rate').null
        self.assertTrue(nullable)

    def test_wd_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('weight_decay').null
        self.assertTrue(nullable)

    def test_epochs_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('epochs').null
        self.assertTrue(nullable)

    def test_val_size_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('validation_set_size').null
        self.assertTrue(nullable)

    def test_miou_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('miou_score').null
        self.assertTrue(nullable)

    def test_top1_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('top1_score').null
        self.assertTrue(nullable)

    def test_top5_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('top5_score').null
        self.assertTrue(nullable)

    def test_checkpoint_constraints(self):
        model = LearningModel.objects.get(id=1)
        nullable = model._meta.get_field('checkpoint').null
        self.assertTrue(nullable)

    def test_default_values_for_scores_and_checkpoint(self):
        model = LearningModel.objects.create(name='model2', architecture='Faster RCNN', project=Project.objects.get(id=1))
        self.assertIsNone(model.miou_score)
        self.assertIsNone(model.top1_score)
        self.assertIsNone(model.top5_score)
        self.assertIsNone(model.checkpoint)
