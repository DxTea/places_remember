from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from places.models import Place
from users.models import Profile


class AddPlaceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)  # Создаем профиль для пользователя
        self.client.login(username='testuser', password='testpassword')

    def test_add_place(self):
        # Создание нового места
        response = self.client.post(reverse('places:add_place'), {
            'title': 'New Place',
            'location': 'Some Location',
            'comment': 'Some Comment'
        })

        # Проверка, что место было успешно создано
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление
        self.assertEqual(Place.objects.count(), 1)  # Ожидаем наличие одного места в базе данных

        new_place = Place.objects.first()
        self.assertEqual(new_place.title, 'New Place')
        self.assertEqual(new_place.location, 'Some Location')
        self.assertEqual(new_place.comment, 'Some Comment')
        self.assertEqual(new_place.profile, self.user.profile)

    def test_add_place_with_empty_fields(self):
        # Попытка создания нового места с пустыми полями
        response = self.client.post(reverse('places:add_place'), {
            'title': '',
            'location': '',
            'comment': ''
        })

        # Проверка, что место не было создано
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный ответ
        self.assertEqual(Place.objects.count(), 0)  # Ожидаем отсутствие мест в базе данных

    def test_add_place_with_existing_title(self):
        # Создание первого места с определенным названием
        Place.objects.create(title='Existing Place', location='Some Location', comment='Some Comment',
                             profile=self.user.profile)

        # Попытка создания нового места с тем же названием
        response = self.client.post(reverse('places:add_place'), {
            'title': 'Existing Place',
            'location': 'New Location',
            'comment': 'New Comment'
        })

        # Проверка, что место не было создано и получили ошибку уникальности
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный ответ
        self.assertEqual(Place.objects.count(), 1)  # Ожидаем наличие только одного места в базе данных
        self.assertFormError(response, 'form', 'title', 'Место с таким названием уже существует.')


class PlacesTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя и профиль
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)

        # Создаем места пользователя
        self.place1 = Place.objects.create(title='Place 1', location='Location 1', comment='Comment 1',
                                           profile=self.profile)
        self.place2 = Place.objects.create(title='Place 2', location='Location 2', comment='Comment 2',
                                           profile=self.profile)

    def test_display_user_places(self):
        # Аутентифицируем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Проверка отображения всех мест пользователя на странице places.html

        response = self.client.get(reverse('places:places'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'places.html')
        self.assertContains(response, 'Мои места')
        self.assertQuerysetEqual(
            response.context['profile_places'],
            ['Place 1', 'Place 2'],
            transform=str,
            ordered=False
        )
