from django.contrib import admin

# Register your models here.

from .models import Director, Genre, Movie, Language, Profile, Contact

"""Minimal registration of Models.
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(MovieInstance)
admin.site.register(Genre)
admin.site.register(Language)
"""

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Contact)

class MoviesInline(admin.TabularInline):
    """Defines format of inline movie insertion (used in DirectorAdmin)"""
    model = Movie

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    """Administration object for Director models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of movies in director view (inlines)
    """
    list_display = ('name', 'date_of_birth', 'date_of_death')
    fields = ['name', ('date_of_birth', 'date_of_death')]
    inlines = [MoviesInline]

class MovieAdmin(admin.ModelAdmin):
    """Administration object for Movie models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of movie instances in movie view (inlines)
    """
    list_display = ('title', 'director')
    exclude = ('duration', 'fps', 'dimensions')
    #inlines = [MoviesInstanceInline]

admin.site.register(Movie, MovieAdmin)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, user_type=int(1))
    else:
        instance.profile.save()

# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)