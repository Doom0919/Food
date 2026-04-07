from itertools import count

from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context

class CustomDashboardView(TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "total_users": User.objects.count(),
            "daily_sales": 1500.50,  # Жишээ дата
            "new_orders": 12,        # Жишээ дата
            "title": "Миний Dashboard",
        })
        return context





class FoodIngredientsBulk(APIView):
    def post(self, request):
        data = request.data

        for item in data:
            food_name = item.get("food_name")
            direction = item.get("direction")
            description = item.get("description")
            ingredients = item.get("ingredients", [])

            if not food_name:
                continue
            food, _ = Food.objects.get_or_create(name=food_name, directions=direction, description=description)

            for ingredient in ingredients:
                ingredient_name = ingredient.get("name")
                weight = ingredient.get("weight", 0)

                if not ingredient_name:
                    continue

                ingredient_obj, _ = Ingredient.objects.get_or_create(
                    name=ingredient_name
                )

                FoodIngredient.objects.get_or_create(
                    food=food,
                    ingredient=ingredient_obj,
                    weight=weight
                )

        return Response({"status": "ok"})



class getFoodIngredientsBulk(APIView):
    def get(self, request):
        # Get all ingredients that are NOT associated with any MyFood
        final_ingredients = Ingredient.objects.filter(myfood__isnull=True).distinct()
        
        # Serialize the data
        ingredients_data = [
            {"id": ingredient.id, "name": ingredient.name}
            for ingredient in final_ingredients
        ]
        
        return Response(ingredients_data)



