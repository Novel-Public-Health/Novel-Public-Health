from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm, UserUpdateForm


# Create your views here.

from .models import Movie, Director, Genre, Profile, Contact

from django.views import generic

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from catalog.forms import UserRegisterForm

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Director

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from taggit.models import Tag

# Stripe imports
import stripe
import djstripe
import json
from djstripe.models import Product
import os

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_movies = Movie.objects.all().count()
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

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user,initial={'email': request.user.email, 'username': request.user.username})
        if u_form.is_valid():
            u_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user.profile, initial={'email': request.user.email, 'username': request.user.username})

    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'user_profile': user_profile, 'u_form': u_form})

# contact form
def contactUs(request):
    if request.method== "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # print("Form is saved")
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            messages.success(request, f'Thanks for submitting a message!')
            return redirect('contactUs')
            
    else:
        form = ContactForm()
    return render(request, 'contactUs.html', {'form': form})

# About us view
def aboutUs(request):
    return render(request, 'aboutUs.html')

def ourPartners(request):
    return render(request, 'ourPartners.html')

def leadership(request):
    return render(request, 'leadership.html')

class MovieListView(generic.ListView):
    """Generic class-based view for a list of movies."""
    model = Movie
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context['sort'] = self.request.GET.get("sort", "title")
        user_genre = self.request.GET.get("genre")
        try:
            Genre.objects.get(name=user_genre)
        except:
            user_genre = None
        context['genre'] = user_genre
        context['genres'] = Genre.objects.all()

        selected_tags = self.request.GET.get("tags")
        if selected_tags:
            context['tags'] = ",".join(selected_tags.split(","))
        context['allTags'] = Tag.objects.all()

        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        selected_genre = self.request.GET.get("genre")
        selected_sort = self.request.GET.get("sort")
        selected_tags = self.request.GET.get("tags")
        if selected_tags:
            selected_tags = selected_tags.split(",")

        movie_qs = None
        try:
            # Filter if the genre exists in the user query
            genre_obj = Genre.objects.get(name=selected_genre)
            movie_qs = Movie.objects.filter(
                genre=genre_obj
            ).order_by(selected_sort).distinct()
        except:
            pass
        
        tag_qs = None
        try:
            # Filter if using any tags
            tag_names_exists = []
            for tag_name in selected_tags:
                try:
                    t = Tag.objects.get(slug=tag_name)
                    tag_names_exists.append(t.name)
                except:
                    pass
            
            if len(tag_names_exists) > 0:
                tag_qs = Movie.objects.filter( tags__name__in=tag_names_exists ).distinct()

        except:
            pass

        if movie_qs and tag_qs:
            qs = movie_qs & tag_qs
        elif movie_qs:
            qs = movie_qs
        elif tag_qs:
            qs = tag_qs

        try:
            qs = qs.order_by(selected_sort)
        except:
            selected_sort = "title"
            qs = qs.order_by(selected_sort)
        
        return qs

class MovieDetailView(generic.DetailView):
    # Generic class-based detail view for a movie.
    model = Movie

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user=self.request.user)
            context['is_user'] = True
        except:
            context['is_user'] = False
        return context

class DirectorListView(generic.ListView):
    """Generic class-based list view for a list of directors."""
    model = Director
    paginate_by = 10


class DirectorDetailView(generic.DetailView):
    """Generic class-based detail view for an director."""
    model = Director

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

@login_required
def process_subscription(request):
    products = Product.objects.all()
    stripe_pub_key = os.environ.get('STRIPE_TEST_PUBLIC_KEY')
    return render(request, 'subscription_form.html', {"products": products, "stripe_pub_key": stripe_pub_key})

@login_required
def create_sub(request):
    if request.method == 'POST':
        # Reads application/json and returns a response
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)

            profile = Profile.objects.get(user=request.user)
            profile.customer = djstripe_customer

            # Subscribe the user to the subscription created
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=["latest_invoice.payment_intent"]
            )
            
            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)
            profile.subscription = djstripe_subscription

            ### IMPORTANT: Change Strings based on the name of the subscription product on STRIPE ###
            if data["plan_id"] == 'Premium Subscription':
                profile.user_type = 3
            elif data["plan_id"] == 'Low Subscription':
                profile.user_type = 2

            profile.save()
            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status =403)
    else:
        return HttpResponse("request method not allowed")

@login_required
def complete(request):
  return render(request, "subscription_success.html")

@login_required
def cancel(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        sub_id = profile.subscription.id

        profile.user_type = 1 # free subscription
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        
        try:
            stripe.Subscription.delete(sub_id)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status =403)
        
        profile.save()
        return redirect("profile")