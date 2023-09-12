from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Lesson
from education.paginators import CoursePaginator
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.ru', password='12345', is_active=True)
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': 'Kusto Test',
            'description': 'Kusto Test',
            'link': 'https://www.youtube.com/watch?v=NtjXWzZnGJQ',
            'owner': self.user.pk,
        }

    def test_create_lesson(self):

        """Тест создания урока"""

        link_lesson_create = reverse('education:lesson_create')
        response = self.client.post(link_lesson_create, self.data)
        data_response_true = {
            'id': response.json()['id'],
            'name': 'Kusto Test',
            'description': 'Kusto Test',
            'preview': None,
            'link': 'https://www.youtube.com/watch?v=NtjXWzZnGJQ',
            'course': None,
            'owner': self.user.pk
        }
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json(), data_response_true)
        self.assertTrue(Lesson.objects.all().exists())

    def test_read_lesson(self):
        
        """Тест чтения данных"""
        
        link_lesson_create = reverse('education:lesson_create')
        response = self.client.post(link_lesson_create, self.data)
        lesson_id = response.json()['id']
        data_response_detail_true = {
            'id': lesson_id,
            'name': 'Kusto Test',
            'description': 'Kusto Test',
            'preview': None,
            'link': 'https://www.youtube.com/watch?v=NtjXWzZnGJQ',
            'course': None,
            'owner': self.user.pk
        }
        data_response_list_true = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [data_response_detail_true]
        }
        self.link_lesson_list = reverse('education:lesson_list')
        response = self.client.get(self.link_lesson_list)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        if Lesson.objects.all().count() > CoursePaginator.page_size:
            self.assertEquals(response.json(), data_response_list_true)
        else:
            self.assertEquals(response.json(), [data_response_detail_true])
        self.link_lesson_detail = reverse('education:lesson_get', kwargs={'pk': lesson_id})
        response = self.client.get(self.link_lesson_detail)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), data_response_detail_true)

    def test_update_lesson(self):
        
        """Тест обновления данных об уроке"""
        
        link_lesson_create = reverse('education:lesson_create')
        response = self.client.post(link_lesson_create, self.data)
        lesson_id = response.json()['id']
        data_response_update_put = {
            'name': 'Kusto Test',
            'description': 'Kusto Test',
            'link': 'https://www.youtube.com/'
        }
        data_response_update_put_true = {
            'id': lesson_id,
            'name': 'Kusto Test',
            'description': 'Kusto Test',
            'preview': None,
            'link': 'https://www.youtube.com/',
            'course': None,
            'owner': self.user.pk
        }
        self.link_lesson_update = reverse('education:lesson_update', kwargs={'pk': lesson_id})
        response = self.client.put(self.link_lesson_update, data_response_update_put)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), data_response_update_put_true)
        data_response_update_patch = {
            'description': 'test test'
        }
        data_response_update_patch_true = {
            'id': lesson_id,
            'name': 'Kusto Test',
            'description': 'test test',
            'preview': None,
            'link': 'https://www.youtube.com/',
            'course': None,
            'owner': self.user.pk
        }
        response = self.client.patch(self.link_lesson_update, data_response_update_patch)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), data_response_update_patch_true)

    def test_delete_lesson(self):

        """Тест удаление урока"""

        link_lesson_create = reverse('education:lesson_create')
        response = self.client.post(link_lesson_create, self.data)
        lesson_id = response.json()['id']
        self.link_lesson_delete = reverse('education:lesson_delete', kwargs={'pk': lesson_id})
        response = self.client.delete(self.link_lesson_delete)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(email='test1@test1.ru', password='12345', is_active=True)
        self.user2 = User.objects.create(email='test2@test2.ru', password='12345', is_active=True)
        self.user1.save()
        self.user2.save()
        self.client.force_authenticate(user=self.user1)
        self.data_course = {
            'name': 'Разработчик Python',
            'description': 'Курс SkyPro',
            'link': 'https://www.youtube.com/watch?v=NtjXWzZnGJQ',
            'owner': self.user1.pk,
        }
        link_course_create = reverse('education:courses-list')
        response = self.client.post(link_course_create, self.data_course)
        self.course_id = response.json()['id']

    def test_update_subscription(self):

        """Обновление подписки тест"""

        self.data_subscription = {
            'course': self.course_id,
            'subscriber': self.user2.pk,
        }
        link_subscription_create = reverse('education:subscription-list')
        response = self.client.post(link_subscription_create, self.data_subscription)
        # Проверка подписки user1
        self.client.force_authenticate(user=self.user1)
        link_course_detail = reverse('education:courses-list')
        response = self.client.get(link_course_detail)
        self.assertFalse(response.json()[0]['subscription'])
        # Проверка подписки user2
        self.client.force_authenticate(user=self.user2)
        link_course_detail = reverse('education:courses-list')
        response = self.client.get(link_course_detail)
        self.assertTrue(response.json()[0]['subscription'])
