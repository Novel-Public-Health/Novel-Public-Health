"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from Users import views as user_views

# Use include() to add URLS from the catalog application and authentication system
from django.urls import include

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('catalog/', include('catalog.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),

]


# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]



#Add Django site authentication urls (for login, logout, password management)
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL_LOCAL, document_root=settings.MEDIA_ROOT_LOCAL)

urlpatterns += [
    url(r'^s3direct/', include('s3direct.urls')),
]