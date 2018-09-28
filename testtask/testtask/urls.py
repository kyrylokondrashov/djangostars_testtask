"""testtask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from bookstore import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls , ),
    re_path(r'^main$', views.BookList.as_view(), name="bookstore-main"),
    re_path(r'^book/(?P<pk>[0-9]+)$', views.BookDetails.as_view(extra_context={'title': 'Book Info'}), name='bookstore-bookinfo'),
    re_path(r'^book/add$', views.AddBook.as_view(extra_context={'title': 'Create new book'}), name='bookstore-addBook'),
    re_path(r'^book/(?P<pk>[0-9]+)/edit$', views.EditBook.as_view(extra_context={'title': 'Edit book information'}), name='bookstore-editBook'),
    re_path(r'^author/(?P<pk>[0-9]+)$', views.AuthorDetails.as_view(extra_context={'title': 'Author Info'}), name='bookstore-authorinfo'),
    re_path(r'^author/add$', views.AddAuthor.as_view(extra_context={'title': 'Create new author'}), name='bookstore-addAuthor'),
    re_path(r'^author/(?P<pk>[0-9]+)/edit$', views.EditAuthor.as_view(extra_context={'title': 'Edit author information'}), name='bookstore-editAuthor'),
    re_path(r'^accounts/login/$', auth_views.login,  {'template_name': 'login.html'}, name='login'),
    re_path(r'^accounts/logout/$', auth_views.logout, {'next_page': '/accounts/login'}, name='logout'),
    re_path(r'^requests/$', views.RequestInfo.as_view(extra_context={'title': 'Requests'}), name='request'),
]
