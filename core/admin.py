from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django import forms
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import Food, Ingredient, FoodIngredient, MyFood


# Custom filter for ingredients not in MyFood
class NotInMyFoodFilter(admin.SimpleListFilter):
    title = 'MyFood Association'
    parameter_name = 'myfood_status'

    def lookups(self, request, model_admin):
        return (
            ('not_associated', 'Not in any MyFood'),
            ('associated', 'In MyFood'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'not_associated':
            return queryset.filter(myfood__isnull=True).distinct()
        if self.value() == 'associated':
            return queryset.filter(myfood__isnull=False).distinct()
        return queryset


# Register Ingredient with search capabilities  
@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ("id", "name", "is_in_myfood")
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = (NotInMyFoodFilter,)

    def is_in_myfood(self, obj):
        return obj.myfood_set.exists()

    is_in_myfood.boolean = True
    is_in_myfood.short_description = "In MyFood"


# Custom widget with inline search
class SearchableCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        original_html = super().render(name, value, attrs, renderer)
        search_html = f'''
        <div style="margin-bottom: 15px;">
            <input type="text" 
                   id="{attrs.get('id', name)}_search" 
                   placeholder="Search ingredients..." 
                   style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;"
                   onkeyup="filterCheckboxes('{attrs.get('id', name)}', this.value)">
        </div>
        <div id="{attrs.get('id', name)}_list" style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 4px;">
            {original_html}
        </div>
        <script>
        function filterCheckboxes(fieldId, searchTerm) {{
            var listDiv = document.getElementById(fieldId + '_list');
            var labels = listDiv.getElementsByTagName('label');
            searchTerm = searchTerm.toLowerCase();
            
            for (var i = 0; i < labels.length; i++) {{
                var text = labels[i].textContent.toLowerCase();
                labels[i].style.display = text.includes(searchTerm) ? '' : 'none';
            }}
        }}
        </script>
        '''
        return mark_safe(search_html)


# Custom form for MyFood
class MyFoodForm(forms.ModelForm):
    class Meta:
        model = MyFood
        fields = '__all__'
        widgets = {
            'ingredients': SearchableCheckboxSelectMultiple,
        }


@admin.register(MyFood)
class MyFoodAdmin(ModelAdmin):
    form = MyFoodForm
    list_display = ("id", "food_id", "ingredient_count")
    search_fields = ("food_id",)
    list_filter = ("ingredients",)
    
    def ingredient_count(self, obj):
        return obj.ingredients.count()
    ingredient_count.short_description = "Ingredients"
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "ingredients":
            # Show only ingredients not already in any MyFood
            kwargs["queryset"] = Ingredient.objects.filter(myfood__isnull=True).distinct()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# Unregister the default User and Group admin
admin.site.unregister(User)
admin.site.unregister(Group)


# Register User with Unfold styling
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


# Register Group with Unfold styling
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
