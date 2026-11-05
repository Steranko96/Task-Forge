
from django.contrib.auth import get_user_model
from django.db import IntegrityError, connection, transaction
from django.test import TestCase

from .models import Task


class TaskModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="test-password-only",
        )

    def test_task_defaults(self):
        task = Task.objects.create(
            owner=self.user,
            title="Learn Django testing",
        )

        self.assertEqual(task.description, "")
        self.assertFalse(task.is_completed)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_task_fields_persist(self):
        task = Task.objects.create(
            owner=self.user,
            title="Original title",
            description="Original description",
        )

        task.title = "Updated title"
        task.description = "Updated description"
        task.is_completed = True
        task.save()

        saved_task = Task.objects.get(pk=task.pk)

        self.assertEqual(saved_task.title, "Updated title")
        self.assertEqual(
            saved_task.description,
            "Updated description",
        )
        self.assertTrue(saved_task.is_completed)
        self.assertEqual(saved_task.owner, self.user)

    def test_task_requires_owner(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Task.objects.create(
                    title="Ownerless task",
                )

        self.assertFalse(
            Task.objects.filter(title="Ownerless task").exists()
        )

    def test_task_string_representation(self):
        task = Task.objects.create(
            owner=self.user,
            title="Readable task",
        )

        self.assertEqual(str(task), "Readable task")

    def test_database_is_postgresql(self):
        self.assertEqual(connection.vendor, "postgresql")
