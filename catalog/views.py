from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

# Create your views here.

from .models import Movie, Director, Genre, Profile, Contact, Transaction, Invoice

from django.views import generic

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from catalog.forms import UserRegisterForm, SubscriptionChangeForm

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Director

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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

def profile(request, transaction=None):
    if request.method == 'POST':
        form = SubscriptionChangeForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            request.session['new_type'] = profile.user_type
            request.session['subscription_plan'] = request.POST.get('plans')
            # redirect to paypal page after clicking change subscription button
            return redirect('process_subscription')
    else:
        user_profile = Profile.objects.get(user=request.user)
        form = SubscriptionChangeForm(initial={'user_type': user_profile.user_type})
    return render(request, 'users/profile.html', {'form': form, 'user_profile': user_profile})

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

def process_subscription(request):
    new_type = request.session['new_type']
    """if new_type == 1: # free account so no need to go through PayPal
        profile = Profile.objects.get(user=request.user)
        profile.user_type = new_type
        profile.save()
        return redirect('profile')"""
    
    # Purchasing a subscription through PayPal
    host = request.get_host()

    transaction, created = Transaction.objects.get_or_create(user=request.user, subscription=new_type)
    invoice = Invoice.objects.create(invoice_no=transaction.increment_invoice_number())

    subscription_plan = request.session.get('subscription_plan')
    host = request.get_host()

    price = transaction.get_amount()
    if subscription_plan == '1-month':
        billing_cycle = 1
        billing_cycle_unit = "M"
    elif subscription_plan == '6-month':
        billing_cycle = 6
        billing_cycle_unit = "M"
    else:
        billing_cycle = 1
        billing_cycle_unit = "Y"

    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,  # monthly price
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "currency_code": "USD",
        "item_name": 'Example item',
        "invoice": invoice.invoice_no,
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'paypal_form.html', {'transaction': transaction, 'form': form})

@csrf_exempt
def payment_done(request):
    messages.success(request, f'Thank you for your order.')
    transaction = Transaction.objects.get(user=request.user)
    
    profile = Profile.objects.get(user=request.user)
    profile.user_type = transaction.subscription
    profile.save()

    return redirect('profile')

@csrf_exempt
def payment_canceled(request):
    messages.success(request, f'Payment cancelled.')
    return redirect('profile')