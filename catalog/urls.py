from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('leadership', views.leadership, name='leadership'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
    path('directors/', views.DirectorListView.as_view(), name='directors'),
    path('directors/<int:pk>',
         views.DirectorDetailView.as_view(), name='director-detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
] 

# Add URLConf to create, update, and delete directors
urlpatterns += [
    path('director/create/', views.DirectorCreate.as_view(), name='director-create'),
    path('director/<int:pk>/update/', views.DirectorUpdate.as_view(), name='director-update'),
    path('director/<int:pk>/delete/', views.DirectorDelete.as_view(), name='director-delete'),
]

# Add URLConf to create, update, and delete movies
urlpatterns += [
    path('movie/create/', views.MovieCreate.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', views.MovieUpdate.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', views.MovieDelete.as_view(), name='movie-delete'),
]
