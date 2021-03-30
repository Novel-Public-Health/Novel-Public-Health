from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 

from s3direct.fields import S3DirectField

import imdb
from moviepy.editor import VideoFileClip
import datetime

from scholarly import scholarly, ProxyGenerator

import sys, re, os

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
    title = models.CharField(max_length=200, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id and left blank.')

    imdb_link = models.CharField('IMDB Link', max_length=100, blank=True, help_text='For example, here is <a target="_blank" '
                                                                'href="https://www.imdb.com/title/tt3322364/">Concussion\'s link</a>.')

    # Foreign Key used because movie can only have one director, but directors can have multiple movies
    # Director as a string rather than object because it hasn't been declared yet in file.
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True, blank=True, help_text='This field will be overwritten \
                                                                                                if given a valid IMDB id and left blank.')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=5000, null=True, blank=True, help_text="Enter a brief description of the movie. This field will \
                                                                                    be overwritten if given a valid IMDB id and left blank.")

    # Genre class has already been defined so we can specify the object above.
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True, help_text='This field will be overwritten if given \
                                                                                                        a valid IMDB id and left blank.')
    year = models.CharField(max_length=200, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id and left blank.')

    file = S3DirectField(dest='videos', blank=True)
    #image = S3DirectField(dest='images', blank=True)
    
    duration = models.CharField(max_length=200)
    fps = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=200)

    max_num_find_articles = models.IntegerField('Max number of research articles', default=5, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Default number is 5.")
    found_articles = models.TextField('Found Research Articles', max_length=5000, null=True, blank=True, help_text="HTML list output of found research \
                                                                                    articles on Google Scholar. Clear the text to find new articles.")
    
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
        return self.title if self.title else ''
    
    def get_movie_url(self):
        return (self.file).replace(" ", "+")

    def get_video_stats(self):
        #filename = str(settings.BASE_DIR) + self.file.url
        clip = VideoFileClip(self.get_movie_url())
        duration       = str(datetime.timedelta(seconds=round(clip.duration)))
        fps            = clip.fps
        width, height  = clip.size
        return [duration, fps, (width, height)]

    def get_imdb_stats(self): 
        ia = imdb.IMDb() 
        reg = re.compile(r'^.*(ch|co|ev|nm|tt)(\d{7}\d*)\/?$')
        id_found = reg.match(self.imdb_link)
        if id_found:
            movie = ia.get_movie(id_found.group(2))   
            return [movie['year'], movie['directors'][0], movie['genres'][0], movie['title'], movie.get('plot')[0]]
        else:
            raise Exception(f"No imdb match found for imdb link: {self.imdb_link}")

    def get_research_articles(self, max_num):
        search_str = f'{self.title} {self.director.name}'
        output = f""
        try:
            pg = ProxyGenerator()
            ip = os.environ['PROXY_IP']
            #print(sys.stderr, ip) # to make sure your env variable is set
            pg.SingleProxy(http = ip, https = ip)
            o = scholarly.use_proxy(pg)
            search_query = scholarly.search_pubs(search_str)
            for i in range(0, max_num):
                curr = next(search_query)
                #scholarly.pprint(curr)
                title = curr['bib']['title']
                # check for curr['pub_url'] 
                if 'pub_url' in curr:
                    output += f"<li>\n\t<a target='_blank' href=\"{curr['pub_url']}\">{title}</a>\n\t<br>\n"
                else:
                    output += f"<li>\n\t{title}\n\t<br>\n"
                # check for curr['bib']['abstract']
                if 'bib' in curr and 'abstract' in curr['bib']:
                    output += f"\t<p>{curr['bib']['abstract']}</p>\n"

                output += f"</li>\n"
        except Exception as e:
            print(sys.stderr, e)
        return output

    def save(self, *args, **kwargs):
        super(Movie, self).save(*args, **kwargs)
        """Use a custom save to end date any subCases"""
        
        orig = Movie.objects.get(id=self.id)
        fields_to_update = []

        try:
            specs = self.get_video_stats()
            orig.duration = specs[0]
            orig.fps = specs[1]
            orig.dimensions = specs[2]
            fields_to_update.extend(['duration', 'fps', 'dimensions'])
        except Exception as e:
            print(sys.stderr, e)

        try:
            imdb_stats = self.get_imdb_stats()
            orig.title = imdb_stats[3]
            orig.year = imdb_stats[0]

            # check if director name already exists. if not, create and assign to the movie
            director = None
            try:
                directors = orig.director.__class__.objects.all()
                for d in directors:
                    if (str(d.name) == str(imdb_stats[1])):
                        director = d
                        break
                orig.director = director if director is not None else Director.objects.create(name=imdb_stats[1])
            except:
                orig.director = Director.objects.create(name=imdb_stats[1])

            # check if genre name already exists. if not, create and assign to the movie
            genre = None
            try:
                genres = orig.genre.__class__.objects.all()
                for g in genres:
                    if (str(g.name) == str(imdb_stats[2])):
                        genre = g
                        break
                genre = genre if genre is not None else Genre.objects.create(name=imdb_stats[2])
            except:
                genre = Genre.objects.create(name=imdb_stats[2])
            orig.genre = genre
            # update values only if they are left blank
            if not self.year:
                fields_to_update.append('year')
            if not self.genre:
                fields_to_update.append('genre')
            if not self.title:
                fields_to_update.append('title')
            if not self.director:
                fields_to_update.append('director')
            if not self.summary:
                orig.summary = imdb_stats[4]
                fields_to_update.append('summary')
        except Exception as e:
            print(sys.stderr, e)

        if not self.found_articles:
            orig.found_articles = orig.get_research_articles(self.max_num_find_articles)
            fields_to_update.append('found_articles')

        super(Movie, orig).save(update_fields=fields_to_update)

import uuid  # Required for unique movie instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower

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