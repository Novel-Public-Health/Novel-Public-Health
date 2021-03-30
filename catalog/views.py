from django.shortcuts import render

# Create your views here.

from .models import Movie, Director, Genre


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

def register(request):
    return render(request, 'register.html')

# About us view
def aboutUs(request):
    return render(request, 'aboutUs.html')

def ourPartners(request):
    return render(request, 'ourPartners.html')

def leadership(request):
    return render(request, 'leadership.html')


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


from django.contrib.auth.mixins import LoginRequiredMixin

"""
class LoanedMoviesByUserListView(LoginRequiredMixin, generic.ListView):
    Generic class-based view listing movies on loan to current user.
    model = MovieInstance
    template_name = 'catalog/movieinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return MovieInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
"""

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin

"""
class LoanedMoviesAllListView(PermissionRequiredMixin, generic.ListView):
    #Generic class-based view listing all movies on loan. Only visible to users with can_mark_returned permission.
    model = MovieInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/movieinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return MovieInstance.objects.filter(status__exact='o').order_by('due_back')
"""


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

# from .forms import RenewMovieForm
from catalog.forms import RenewMovieForm


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_movie_librarian(request, pk):
    """View function for renewing a specific MovieInstance by librarian."""
    movie_instance = get_object_or_404(MovieInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewMovieForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            movie_instance.due_back = form.cleaned_data['renewal_date']
            movie_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewMovieForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'movie_instance': movie_instance,
    }

    return render(request, 'catalog/movie_renew_librarian.html', context)


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
