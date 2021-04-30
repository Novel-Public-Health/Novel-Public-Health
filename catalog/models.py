from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 

# Imports Django's default User system.
from django.contrib.auth.models import User

# Movie rating imports. Docs: https://django-star-ratings.readthedocs.io/en/latest/?badge=latest/
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

# Amazon AWS S3 import.
from s3direct.fields import S3DirectField

# IMDbPY import. Docs: https://imdbpy.readthedocs.io/en/latest/
import imdb

# Video stats with MoviePy. Docs: https://zulko.github.io/moviepy/index.html
from moviepy.editor import VideoFileClip

# Google Scholar import. Docs: https://scholarly.readthedocs.io/en/latest/?badge=latest
from scholarly import scholarly, ProxyGenerator

# Django taggit import for managing comma-separated tags. Docs: https://django-taggit.readthedocs.io/en/latest/
from taggit.managers import TaggableManager

import sys, re, os, datetime

class Genre(models.Model):
    # Model representing a movie genre (e.g. Science Fiction, Non Fiction).
    name = models.CharField(
        max_length=200,
        help_text="Enter a movie genre (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        # String for representing the Model object (in Admin site etc.)
        return self.name


class Language(models.Model):
    # Model representing a Language (e.g. English, French, Japanese, etc.)
    name = models.CharField(max_length=200,
                            help_text="Enter the movie's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        # String for representing the Model object (in Admin site etc.)
        return self.name


class Movie(models.Model):
    # Model representing a movie (but not a specific copy of a movie).
    title = models.CharField(max_length=200, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id and left blank.')

    imdb_link = models.CharField('IMDB Link', max_length=100, blank=True, null=True, help_text='For example, here is <a target="_blank" '
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
                                                                                                
    tags = TaggableManager(blank=True)

    year = models.CharField(max_length=200, null=True, blank=True, help_text='This field will be overwritten if given a valid IMDB id and left blank.')

    thumbnail = models.CharField('Thumbnail', max_length=500, blank=True, null=True, help_text='This field will be overwritten \
                                                                                                if given a valid IMDB id and left blank.')

    file = S3DirectField(dest='videos', blank=True, null=True)
    
    ads = models.CharField('Google VAMP Ads Link', max_length=1000, blank=True, null=True, help_text="""For example, here is a <a target="_blank"
        href="https://pubads.g.doubleclick.net/gampad/ads?sz=640x480&iu=/124319096/external/ad_rule_samples&ciu_szs=300x250&ad_rule=1&impl=s&gdfp_req=1&env=vp&output=vmap&unviewed_position_start=1&cust_params=deployment%3Ddevsite%26sample_ar%3Dpremidpost&cmsid=496&vid=short_onecue&correlator=">
        Google VAMP example link</a>.""")

    duration = models.CharField(max_length=200)
    fps = models.CharField(max_length=200)
    dimensions = models.CharField(max_length=200)

    max_num_find_articles = models.IntegerField('Max number of research articles', default=5, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Default number is 5.")
    found_articles = models.TextField('Found Research Articles', max_length=5000, null=True, blank=True, help_text="HTML list output of found research \
                                                                                    articles on Google Scholar. Clear the text to find new articles.")
    
    ratings = GenericRelation(Rating, related_query_name='movie-rating')
    
    class Meta:
        ordering = ['title', 'director']

    def display_genre(self):
        # Creates a string for the Genre. This is required to display genre in Admin.
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        # Returns the url to access a particular movie instance.
        return reverse('movie-detail', args=[str(self.id)])

    def __str__(self):
        # String for representing the Model object.
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
            return [movie['year'], movie['directors'][0], movie['genres'][0], movie['title'], movie.get('plot')[0], movie['cover url']]
        else:
            raise Exception(f"No imdb match found for imdb link: {self.imdb_link}")

    def get_research_articles(self, max_num):
        # Search string for Google Scholar to look for. 
        # e.g. "{self.title} {self.director.name}" would equate to "Concussion Peter Landesman" for the movie Concussion.
        search_str = f'{self.title} {self.director.name}'
        output = f""
        try:
            pg = ProxyGenerator()
            ip = os.environ['PROXY_IP']
            pg.SingleProxy(http = ip, https = ip)
            o = scholarly.use_proxy(pg)
            search_query = scholarly.search_pubs(search_str)
            for i in range(0, max_num):
                curr = next(search_query)

                # For debugging purposes, this is how you pretty print the search query's contents.
                #scholarly.pprint(curr)

                # Grab the title of the article.
                title = curr['bib']['title']
                
                # Begin our formatted html output for each found research article.
                output += f"""
                    <li>
                """
                
                # See if a publication url (i.e. curr['pub_url']) exists. If so, add an external link to it.
                if 'pub_url' in curr:
                    output += f"""
                        <a target='_blank' href=\"{curr['pub_url']}\">{title}</a>
                    """
                else:
                    output += f"""
                        {title}
                    """
                
                output += f"""
                    <br>
                """

                # Writes the abstract (i.e.curr['bib']['abstract']) if it exists.
                if 'bib' in curr and 'abstract' in curr['bib']:
                    output += f"""
                        <p>{curr['bib']['abstract']}</p>
                    """

                output += f"""
                </li>
                """
        except Exception as e:
            pass
            # Useful for seeing errors in your terminal. Replace pass with the print statement below.
            #print(sys.stderr, e)
        return output

    def save(self, *args, **kwargs):
        super(Movie, self).save(*args, **kwargs)
        # Uses a custom save to end date any subCases
        
        orig = Movie.objects.get(id=self.id)
        fields_to_update = []

        try:
            specs = self.get_video_stats()
            orig.duration = specs[0]
            orig.fps = specs[1]
            orig.dimensions = specs[2]
            fields_to_update.extend(['duration', 'fps', 'dimensions'])
        except Exception as e:
            pass

        try:
            imdb_stats = self.get_imdb_stats()
            orig.title = imdb_stats[3]
            orig.year = imdb_stats[0]
            orig.thumbnail = imdb_stats[5]

            # Checks if a director name already exists. If not, create and assign to the movie.
            director = None
            try:
                directors = Director.objects.all()
                for d in directors:
                    if (str(d) == str(imdb_stats[1])):
                        director = d
                        break
                orig.director = director if director is not None else Director.objects.create(name=imdb_stats[1])
            except:
                orig.director = Director.objects.create(name=imdb_stats[1])

            # Checks if a genre name already exists. If not, create and assign to the movie.
            genre = None
            try:
                genres = Genre.objects.all()
                for g in genres:
                    if (str(g) == str(imdb_stats[2])):
                        genre = g
                        break
                genre = genre if genre is not None else Genre.objects.create(name=imdb_stats[2])
            except:
                genre = Genre.objects.create(name=imdb_stats[2])
            orig.genre = genre

            # Updates values only if their fields are left blank by the admin.
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
            if not self.thumbnail:
                fields_to_update.append('thumbnail')
        except Exception as e:
            pass

        # Searches for research articles by using a single proxy for a Google Scholar search query.
        if not self.found_articles:
            orig.found_articles = orig.get_research_articles(self.max_num_find_articles)
            fields_to_update.append('found_articles')

        super(Movie, orig).save(update_fields=fields_to_update)

import uuid  # Required for unique movie instances
from datetime import date

class Director(models.Model):
    # Model representing a director.
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        # Returns the url to access a particular director instance.
        return reverse('director-detail', args=[str(self.id)])

    def __str__(self):
        # String for representing the Model object.
        return self.name

from djstripe.models import Customer, Subscription
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    USER_TYPE_CHOICES = (
        (1, 'Free - access independent films and media outlets'),
        (2, 'Low Subscription - access to Hollywood films'),
        (3, 'Premium Subscription - access to A-list movies')
    )
    user_type = models.IntegerField('Subscription Tier', default=1, choices=USER_TYPE_CHOICES)

    # Assigns a Stripe customer and subscription to a User.
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)

    def get_user_type(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type)
    
    def get_user_type_short(self):
        return dict(self.USER_TYPE_CHOICES).get(self.user_type).split()[0]

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body  = models.TextField()
    
    def __str__(self):
        return self.name