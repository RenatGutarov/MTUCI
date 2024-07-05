
from django.urls import path
from .views import scraper_home, scrape_view

urlpatterns = [
    path('', scraper_home, name='scraper_home'),
    path('scrape/', scrape_view, name='scrape_view'),
]

