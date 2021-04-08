from django.shortcuts import render

# Create your views here.

from .models import Movie, Director, Genre, Profile

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_movies = Movie.objects.all().count()
    #num_instances = MovieInstance.objects.all().count()
    # Available copies of movies
    #num_instances_available = MovieInstance.objects.filter(status__exact='a').count()
    num_directors = Director.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_movies': num_movies,
                 'num_directors': num_directors,
                 'num_visits': num_visits},
    )

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from catalog.forms import UserRegisterForm, SubscriptionChangeForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        form = SubscriptionChangeForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('profile')
    else:
        user_profile = Profile.objects.get(user=request.user)
        form = SubscriptionChangeForm(initial={'user_type': user_profile.user_type})
    return render(request, 'users/profile.html', {'form': form, 'user_profile': user_profile})

# About us view
def aboutUs(request):
    return render(request, 'aboutUs.html')

def ourPartners(request):
    return render(request, 'ourPartners.html')

def leadership(request):
    return render(request, 'leadership.html')

def contactUs(request):
    return render(request, 'contactUs.html')


from django.views import generic


class MovieListView(generic.ListView):
    """Generic class-based view for a list of movies."""
    model = Movie
    paginate_by = 10


class MovieDetailView(generic.DetailView):
    """Generic class-based detail view for a movie."""
    model = Movie


class DirectorListView(generic.ListView):
    """Generic class-based list view for a list of directors."""
    model = Director
    paginate_by = 10


class DirectorDetailView(generic.DetailView):
    """Generic class-based detail view for an director."""
    model = Director
    
# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Director

class DirectorCreate(PermissionRequiredMixin, CreateView):
    model = Director
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'

class DirectorUpdate(PermissionRequiredMixin, UpdateView):
    model = Director
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = 'catalog.can_mark_returned'


class DirectorDelete(PermissionRequiredMixin, DeleteView):
    model = Director
    success_url = reverse_lazy('directors')
    permission_required = 'catalog.can_mark_returned'

# Classes created for the forms challenge
class MovieCreate(PermissionRequiredMixin, CreateView):
    model = Movie
    fields = ['title', 'director', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class MovieUpdate(PermissionRequiredMixin, UpdateView):
    model = Movie
    fields = ['title', 'director', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class MovieDelete(PermissionRequiredMixin, DeleteView):
    model = Movie
    success_url = reverse_lazy('movies')
    permission_required = 'catalog.can_mark_returned'
