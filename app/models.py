# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime

class CustomUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    image = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Recipe(models.Model):
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to='photos', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.IntegerField(default=0, editable=False)
    user = models.ForeignKey(CustomUser, related_name='recipes')

    class Meta:
        ordering = ['likes', 'date']

    def __unicode__(self):
        return self.title

    def like_recipe(self, user):
        try:
            UserRecipe.objects.get(user=user, recipes=self)
        except:
            # like još ne postoji
            ur = UserRecipe(user=user, recipes=self)
            ur.save()

class Discount(models.Model):
    text = models.TextField(blank=False, max_length=200)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(CustomUser, related_name='discounts')

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return self.text

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class UserRecipe(models.Model):
    user = models.ForeignKey(CustomUser)
    recipes = models.ForeignKey(Recipe)

    def save(self, *args, **kwargs):
        super(UserRecipe, self).save(*args, **kwargs)
        # update broja glasova u modelu Recipe
        likes = UserRecipe.objects.filter(recipes__id=self.recipes.id)
        self.recipes.likes = likes.count()
        self.recipes.save()
        

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_categories')
    categorie = models.ForeignKey(Category, related_name='category_recipes')

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_tags')
    tag = models.ForeignKey(Tag, related_name='tag_recipes')