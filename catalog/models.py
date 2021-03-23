from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.conf import settings

from s3direct.fields import S3DirectField

class Genre(models.Model):
    """Model representing a movie genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a movie genre (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the movie's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Movie(models.Model):
    """Model representing a movie (but not a specific copy of a movie)."""
    title = models.CharField(max_length=200)
    #director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because movie can only have one director, but directors can have multiple movies
    # Director as a string rather than object because it hasn't been declared yet in file.
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the movie")
    """
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    """
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True)

    imdb = models.CharField('IMDB id', max_length=10, help_text='grabbed from imdb links. for example, <a target="_blank" '
                                                                'href="https://www.imdb.com/title/tt3322364/">Concussion</a> is 3322364')

    #file = models.FileField(upload_to='movie-uploads/')
    file = S3DirectField(dest='videos', blank=True)
    #image = S3DirectField(dest='images', blank=True)
    
    duration = models.CharField(max_length=200)
    fps = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['title', 'director']

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular movie instance."""
        return reverse('movie-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_video_and_imdb_stats(self):
        from moviepy.editor import VideoFileClip
        import datetime
        #filename = str(settings.BASE_DIR) + self.file.url
        clip = VideoFileClip(self.file)
        duration       = str(datetime.timedelta(seconds=round(clip.duration)))
        fps            = clip.fps
        width, height  = clip.size

        # importing the module 
        import imdb  
        ia = imdb.IMDb() 
        movie = ia.get_movie(self.imdb)
        
        return [duration, fps, (width, height), movie['year'], movie['directors'][0], movie['genres'][0] ]

    def save(self, *args, **kwargs):
        super(Movie, self).save(*args, **kwargs)
        """Use a custom save to end date any subCases"""

        specs = self.get_video_and_imdb_stats()
        orig = Movie.objects.get(id=self.id)
        orig.duration = specs[0]
        orig.fps = specs[1]
        orig.dimensions = specs[2]
        orig.year = specs[3]
        orig.director.name = specs[4] #todo

        # check if genre name already exists. if not, create and assign to the movie
        genre = None
        try:
            genres = orig.genre.__class__.objects.all()
            for g in genres:
                if (g.name == specs[5]):
                    genre = g
            genre = genre if genre is not None else Genre.objects.create(name=specs[5])
        except:
            genre = Genre.objects.create(name=specs[5])
        orig.genre = genre

        super(Movie, orig).save(update_fields=['duration', 'fps', 'dimensions', 'year', 'director', 'genre'])

import uuid  # Required for unique movie instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower


class MovieInstance(models.Model):
    """Model representing a specific copy of a movie (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular movie across whole library")
    movie = models.ForeignKey('Movie', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Movie availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set movie as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.movie.title)


class Director(models.Model):
    """Model representing a director."""
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the url to access a particular director instance."""
        return reverse('director-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name
