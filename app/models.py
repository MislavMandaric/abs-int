# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    image = models.ImageField(upload_to='/avatars', null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Recipe(models.Model):
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to='/photos', null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.IntegerField(default=0, editable=False)
    user = models.ForeignKey(CustomUser, related_name='recipes')

    class Meta:
        ordering = ['likes', 'date']

    def __unicode__(self):
        return self.title

    def like_recipe(recipe, user):
        try:
            UserRecipe.objects.get(user=user, recipe=recipe)
        except:
            # like još ne postoji
            ur = UserRecipe(user=user, recipe=recipe)
            ur.save()

class Discount(models.Model):
    text = models.TextField(blank=False, max_length=200)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(CustomUser, related_name='discounts')

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return self.title

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
        likes = UserRecipe.objects.filter(recipe__id=self.recipe.id)
        rp = Recipe.objects.get(id=self.id)
        rp.likes = likes.count()
        rp.save()
        

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe)
    categorie = models.ForeignKey(Category)

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe)
    tag = models.ForeignKey(Tag)