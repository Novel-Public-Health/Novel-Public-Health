from django.test import TestCase

# Create your tests here.

from catalog.models import Director


class DirectorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Director.objects.create(first_name='Big', last_name='Bob')

    def test_name_label(self):
        director = Director.objects.get(id=1)
        field_label = director._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_date_of_birth_label(self):
        director = Director.objects.get(id=1)
        field_label = director._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        director = Director.objects.get(id=1)
        field_label = director._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_get_absolute_url(self):
        director = Director.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(director.get_absolute_url(), '/catalog/directors/1')
