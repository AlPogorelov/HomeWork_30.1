from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group

from courses.models import Course
from materials.models import Lesson
from users.models import User, Subscription


class LessonCRUDTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя (обычный пользователь)
        self.user = User.objects.create_user(
            email='testuser@example.com',  # Используем email
            password='testpassword'
        )

        # Создаем тестового модератора
        self.moderator = User.objects.create_user(
            email='moderator@example.com',  # Используем email
            password='modpassword'
        )
        # Создаем группу "Moder" и добавляем модератора в группу
        self.moder_group = Group.objects.create(name='Moder')
        self.moderator.groups.add(self.moder_group)

        # Создаем тестовый курс
        self.course = Course.objects.create(
            course_name='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            lesson_name='Test Lesson',
            description='Test Lesson Description',
            video_url='http://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        # URL для CRUD операций
        self.create_url = reverse('materials:lesson_create')  # lesson/create/
        self.list_url = reverse('materials:lesson_list')  # lesson/
        self.detail_url = reverse('materials:lesson_get', args=[self.lesson.id])  # lesson/<int:pk>/
        self.update_url = reverse('materials:lesson_update', args=[self.lesson.id])  # lesson/update/<int:pk>/
        self.delete_url = reverse('materials:lesson_delete', args=[self.lesson.id])  # lesson/delete/<int:pk>/

    def test_lesson_create_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'lesson_name': 'New Lesson',
            'description': 'New Lesson Description',
            'video_url': 'http://www.youtube.com/watch?v=new_video',
            'course': self.course.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(lesson_name='New Lesson').exists())

    def test_lesson_create_invalid_video_url(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'lesson_name': 'Invalid Lesson',
            'description': 'Invalid Lesson Description',
            'video_url': 'http://example.com/invalid_video',
            'course': self.course.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)  # Проверяем, что ошибка связана с video_url

    def test_lesson_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_lesson_retrieve_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lesson_name'], self.lesson.lesson_name)

    def test_lesson_update_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'lesson_name': 'Updated Lesson',
            'description': 'Updated Lesson Description',
            'video_url': 'http://www.youtube.com/watch?v=updated_video',
            'course': self.course.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.lesson_name, 'Updated Lesson')

    def test_lesson_update_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        data = {
            'lesson_name': 'Updated Lesson by Moderator',
            'description': 'Updated Lesson Description by Moderator',
            'video_url': 'http://www.youtube.com/watch?v=updated_video_by_moderator',
            'course': self.course.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.lesson_name, 'Updated Lesson by Moderator')

    def test_lesson_delete_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_delete_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

        # Создаем тестовый курс
        self.course = Course.objects.create(
            course_name='Test Course',
            description='Test Description',
            owner=self.user
        )

        # URL для подписки/отписки
        self.subscribe_url = reverse('users:subscribe')  # Используем имя URL из urls.py

    def test_subscribe_to_course(self):
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Отправляем запрос на подписку
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})

        # Проверяем, что подписка создана
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Отправляем запрос на отписку
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})

        # Проверяем, что подписка удалена
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_to_course_unauthenticated(self):
        # Отправляем запрос на подписку без аутентификации
        response = self.client.post(self.subscribe_url, {'course_id': self.course.id})

        # Проверяем, что доступ запрещен
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_to_nonexistent_course(self):
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Отправляем запрос на подписку с несуществующим course_id
        nonexistent_course_id = 999
        response = self.client.post(self.subscribe_url, {'course_id': nonexistent_course_id})

        # Проверяем, что возвращается ошибка 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
