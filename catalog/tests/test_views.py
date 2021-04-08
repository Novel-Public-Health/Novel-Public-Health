from django.test import TestCase

# Create your tests here.


from catalog.models import Director
from django.urls import reverse


class DirectorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create directors for pagination tests
        number_of_directors = 13
        for director_id in range(number_of_directors):
            Director.objects.create(name='Christian {0}'.format(director_id))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/directors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get('/catalog/directors/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/catalog/directors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/director_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get('/catalog/directors/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['director_list']) == 10)

    def test_lists_all_directors(self):
        # Get second page and confirm it has (exactly) the remaining 3 items
        response = self.client.get('/catalog/directors/'+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['director_list']) == 3)

import datetime
from django.utils import timezone

from catalog.models import Movie, Genre, Language
from django.contrib.auth.models import User  # Required to assign User as a borrower

from django.contrib.auth.models import Permission  # Required to grant the permission needed to set a movie as returned.

class DirectorCreateViewTest(TestCase):
    """Test case for the DirectorCreate view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Set movie as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a movie
        test_director = Director.objects.create(name='John Smith')

        # Manually check redirect because we don't know what director was created
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/directors/'))
