from django.db import models

# Create your models here.



class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    directions = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name




class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class FoodIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.FloatField(blank=True, null=True)



class MyFood(models.Model):
    id = models.AutoField(primary_key=True)
    food_id = models.IntegerField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return f"MyFood {self.id}" if not self.food_id else f"MyFood {self.food_id}"


# MyFoodIngredient устгана - through table хэрэггүй




