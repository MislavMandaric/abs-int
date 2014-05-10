# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class CustomUser(User):
    image = models.ImageField(upload_to='/avatars', null=True)

    class Meta:
        ordering = ['username']

    def __unicode__(self):
        return self.username

class Recipe(models.Model):
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to='/photos', null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.IntegerField(default=0, editable=False)
    user = models.ForeignKey(CustomUser, related_name='recipes')

    class Meta:
        ordering = ['likes', 'date']

    def __unicode__(self):
        return self.title

class Discount(models.Model):
    text = models.TextField(blank=False, max_length=200)
    date = models.DateTimeField(auto_now_add=True, editable=False)

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
    users = models.ForeignKey(CustomUser)
    recipes = models.ForeignKey(Recipe)

class RecipeCategory(models.Model):
    recipes = models.ForeignKey(Recipe)
    categories = models.ForeignKey(Category)

class RecipeTag(models.Model):
    recipes = models.ForeignKey(Recipe)
    tags = models.ForeignKey(Tag)