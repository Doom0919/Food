
from django.urls import path
from .views import *

urlpatterns = [
    path('FoodIngredientsBulk/', FoodIngredientsBulk.as_view()),
]