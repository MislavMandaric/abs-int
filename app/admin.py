from django.contrib import admin

from .models import *

admin.site.register(CustomUser)
admin.site.register(Recipe)
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(UserRecipe)
admin.site.register(RecipeCategory)
admin.site.register(RecipeTag)
