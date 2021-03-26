from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.conf import settings

from s3direct.fields import S3DirectField

import imdb
from moviepy.editor import VideoFileClip
import datetime

from scholarly import scholarly, ProxyGenerator

import sys, re

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
    title = models.CharField(max_length=200, help_text='This field will be overwritten if given a valid IMDB id.')

    imdb_link = models.CharField('IMDB Link', max_length=100, blank=True, help_text='For example, here is <a target="_blank" '
                                                                'href="https://www.imdb.com/title/tt3322364/">Concussion\'s link</a>.')

    # Foreign Key used because movie can only have one director, but directors can have multiple movies
    # Director as a string rather than object because it hasn't been declared yet in file.
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id.')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=1000, null=True, blank=True, help_text="Enter a brief description of the movie. If left blank, \
                                                                                        the summary from a valid IMDB link will be used.")

    # Genre class has already been defined so we can specify the object above.
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id.')
    year = models.CharField(max_length=200, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id.')

    file = S3DirectField(dest='videos', blank=True)
    #image = S3DirectField(dest='images', blank=True)
    
    duration = models.CharField(max_length=200)
    fps = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=200)

    found_articles = models.TextField('Found Research Articles', max_length=5000, null=True, blank=True, help_text="HTML list output of found research articles on Google Scholar. Clear the text to find new articles.")
    
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
        reg = re.compile(r'^.*(ch|co|ev|nm|tt)(\d{7})\/?$')
        id_found = reg.match(self.imdb_link)
        if id_found:
            movie = ia.get_movie(id_found.group(2))   
            return [movie['year'], movie['directors'][0], movie['genres'][0], movie['title'], movie.get('plot')[0]]
        else:
            raise Exception(f"No imdb match found for imdb link: {self.imdb_link}")

    def get_research_articles(self, max_num):
        search_str = f'{self.title} movie {self.director.name}'
        try:
            pg = ProxyGenerator()
            ip = 'http://lum-customer-hl_a1431ac1-zone-static:r67n4k2l324c@127.0.0.1:24000'
            #ip = 'http://lum-customer-hl_a1431ac1-zone-static-session-24000_0:r67n4k2l324c@zproxy.lum-superproxy.io:22999'
            #pg.Luminati(usr="lum-customer-hl_a1431ac1-zone-static", passwd ="r67n4k2l324c", proxy_port="24000")
            pg.SingleProxy(http = ip, https = ip)
            o = scholarly.use_proxy(pg)
            search_query = scholarly.search_pubs(search_str)
            output = ''
            for i in range(0, max_num):
                curr = next(search_query)
                scholarly.pprint(curr)
                a = Articles(curr['bib']['title'], curr['pub_url'], curr['bib']['abstract'])
                output += f"<li>\n\t<a target='_blank' href=\"{a.url}\">{a.title}</a>\n\t<br>\n\t<p>{a.abstract}</p>\n</li>\n"
            return output
        except Exception as e:
            raise Exception(f"{e}\nFailed to find results in search query.\nSearched for: \"{search_str}\"")

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
            fields_to_update.extend(['year', 'genre', 'title', 'director'])
            if not self.summary:
                orig.summary = imdb_stats[4]
                fields_to_update.append('summary')
        except Exception as e:
            print(sys.stderr, e)

        if not self.found_articles:
            try:
                orig.found_articles = orig.get_research_articles(5)
                fields_to_update.append('found_articles')
            except Exception as e:
                print(sys.stderr, e)

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

class Articles:
    def __init__(self, title, url, abstract): 
        self.title = title
        self.url = url
        self.abstract = abstract

    def __str__(self):
        return "Title: %s\nUrl: %s\nAbstract: %s\n" % \
     (self.title, self.url, self.abstract)