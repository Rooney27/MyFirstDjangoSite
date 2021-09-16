from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', ItemsListView.as_view()),
    path('<int:pk>', ItemsDetailView.as_view()),
    path('order/', OrderFormView.as_view()),
    path('cart/', Cart.as_view())
]