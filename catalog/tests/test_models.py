from django.test import TestCase

# Create your tests here.

from catalog.models import Director, Genre, Language, Movie, Profile


class DirectorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods.
        Director.objects.create(name='Big Bob')

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
        self.assertEquals(director.get_absolute_url(), '/directors/1')

class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up most popular genres.
        cls.genres = ['Action', 'Fantasy', 'Comedy', 'Romance', 'Documentary']
        for name in cls.genres:
            Genre.objects.create(name=name)

    def test_name_label(self):
        for num, name in enumerate(self.genres, start=1):
            genre = Genre.objects.get(id=num)
            field_label = genre._meta.get_field('name').verbose_name
            self.assertEquals(field_label, 'name')
            # test the name of the genre
            self.assertEquals(genre.name, name)

class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up most popular languages.
        cls.languages = ['Mandarin Chinese', 'Spanish', 'English', 'Hindi']
        for name in cls.languages:
            Language.objects.create(name=name)

    def test_name_label(self):
        for num, name in enumerate(self.languages, start=1):
            language = Language.objects.get(id=num)
            field_label = language._meta.get_field('name').verbose_name
            self.assertEquals(field_label, 'name')
            # test the name of the language
            self.assertEquals(language.name, name)

import re

class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.imdb_movie = Movie.objects.create(
            title='Concussion',
            imdb_link='https://www.imdb.com/title/tt3322364/'
        )

        cls.non_imdb_movie = Movie.objects.create(
            title='Public Health YOU Should Know',
            director=Director.objects.create(name='Big Bob'),
            language=Language.objects.create(name='English'),
            summary="This movie is the greatest thing to ever see. \
                     Forreal.",
            genre=Genre.objects.create(name='Documentary'),
            year='2021'
        )

    def test_non_imdb_movie(self):
        self.assertEquals(self.non_imdb_movie.director.name, 'Big Bob')
        self.assertEquals(self.non_imdb_movie.language.name, 'English')
        self.assertEquals(self.non_imdb_movie.genre.name, 'Documentary')

    def test_imdb_movie(self):
        imdb_stats = self.imdb_movie.get_imdb_stats()
        self.assertEquals(imdb_stats[0], 2015)
        self.assertEquals(imdb_stats[1]['name'], 'Peter Landesman')
        self.assertTrue(re.match(r'(Biography|Drama|Sport)', imdb_stats[2]))