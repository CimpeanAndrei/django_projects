from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^title/', views.titleSearch),
    url(r'^year/', views.yearSearch),
    url(r'^keyword/', views.keywordSearch),
    url(r'^genre/', views.genreSearch),
]
