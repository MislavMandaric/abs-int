# -*- coding: utf-8 -*-

from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView, FormView
from django.views.generic.detail import DetailView

from .models import *
from .forms import SearchForm, RegistrationForm, RecipeForm, DiscountForm

class Index(TemplateView):
	template_name = "home.html"

	def render_to_response(self, context, **response_kwargs):
		# recepie_list = Recipe.objects.all().order_by('like', 'date')[:10]
		# context['recepies'] = recepie_list
		return super(Index, self).render_to_response(context, **response_kwargs)

# ----- korisnici -----

class RegistrationView(FormView):
	template_name = "registration/registration.html"
	form_class = RegistrationForm
	success_url = '/'

	def form_valid(self, form):
		data = form.cleaned_data
		username = data['username']
		mail = data['email']
		password = data['password']
		password2 = data['password2']
		if password != password2:
			return self.render_to_response(self.get_context_data(form=form))
		image = data['image']
		user = User.objects.create_user(username, mail, password)
		custom_user = CustomUser(user=user, image=image)
		custom_user.save()
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return HttpResponseRedirect(self.get_success_url())

	def post(self, request, *args, **kwargs):
		self.request = request
		return super(RegistrationView, self).post(request, *args, **kwargs)


class ProfileView(DetailView):
	template_name = "profile.html"
	model = CustomUser

	def get_object(self, queryset=None):
		self.user = CustomUser.objects.get(user=self.request.user)
		return self.user

	def get_context_data(self, **kwargs):
		context = super(ProfileView, self).get_context_data(**kwargs)
		context['users_recipes'] = self.user.recipes.order_by('-date')
		context['users_discounts'] = self.user.discounts.order_by('-date')
		return context

# ----- recepti -----

class RecipesView(TemplateView):
	template_name = 'recipes.html'

	def get_context_data(self, **kwargs):
		context = super(RecipesView, self).get_context_data(**kwargs)
		limit = 3
		recepies = Recipe.objects.all().order_by('-date')
		if recepies.count() > limit:
			more = True
		else:
			more = False

		context['recipes'] = recepies[:limit]
		context['more'] = more
		return context

class RecipeCreateView(FormView):
	template_name = "recipe_create.html"
	form_class = RecipeForm
	success_url = '/recepti'

	def form_valid(self, form):
		data = form.cleaned_data
		print data
		title = data['title']
		text = data['text']
		image = data['image']
		user = self.request.user
		custom_user = CustomUser.objects.get(user=user)
		rp = Recipe(title=title, text=text, image=image, user=custom_user)
		rp.save()
		# tagovi
		tags = data['tags']
		tags = tags.split(',')
		for t in tags:
			try:
				tag = Tag.objects.get(name=t)
			except:
				# taga nema, stvori novi
				tag = Tag(name=t)
				tag.save()
			rt = RecipeTag(recipe=rp, tag=tag)
			rt.save()

		# kategorije
		categories = data['categories']
		for c in categories:
			try:
				cat = Category.objects.get(name=c)
				rc = RecipeCategory(recipe=rp, categorie=cat)
				rc.save()
			except:
				pass

		return HttpResponseRedirect(self.get_success_url())

	def post(self, request, *args, **kwargs):
		self.request = request
		return super(RecipeCreateView, self).post(request, *args, **kwargs)

class RecipeDetailView(DetailView):
	template_name = "recipe_detail.html"
	model = Recipe

	def get_context_data(self, **kwargs):
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		pk = self.kwargs['pk']
		tags = Tag.objects.filter(tag_recipes__recipe=pk)
		context['tags'] = tags
		categories = Category.objects.filter(category_recipes__recipe=pk)
		context['categories'] = categories

		cu = CustomUser.objects.filter(user=self.request.user)
		rp = Recipe.objects.get(id=pk)
		if cu.exists():
			if cu[0] == rp.user:
				is_liked = True
			else:
				if UserRecipe.objects.filter(user=cu[0], recipes__pk=pk).exists():
					is_liked = True
				else:
					is_liked = False
		else:	
			is_liked = False

		context['is_liked'] = is_liked
		return context


class RecipeSearchView(ListView):
	template_name = "recipe_search.html"
	model = Recipe
	
	def get_queryset(self):
		queryset = []
		filters_categories = Q()

		categories = self.request.GET.getlist('categories', [])
		tags = self.request.GET.get('tags', '')

		self.result = False
		if categories == [] and tags == '':
			return []

		for cat in categories:
			if cat != 'none':
				filters_categories |= Q(recipe_categories__categorie__name=cat)	

		filters_tags = Q()
		if tags:
			tags_list = tags.split(', ')
			for tag in tags_list:
				filters_tags |= Q(recipe_tags__tag__name=tag)

		queryset = Recipe.objects.filter(filters_tags, filters_categories).distinct().order_by('-date')

		if queryset.count() != 0:
			self.result = True
	
		return queryset

	def get_context_data(self, **kwargs):
		context = super(RecipeSearchView, self).get_context_data(**kwargs)
		context['form'] = SearchForm()
		context['result'] = self.result
		return context

# ----- akcije -----

class DiscountCreateView(FormView):
	template_name = "discount_create.html"
	form_class = DiscountForm
	success_url = '/akcije'

	def form_valid(self, form):
		data = form.cleaned_data
		text = data['text']

		user = self.request.user
		custom_user = CustomUser.objects.get(user=user)
		d = Discount(text=text, user=custom_user)
		d.save()

		return HttpResponseRedirect(self.get_success_url())

	def post(self, request, *args, **kwargs):
		self.request = request
		return super(DiscountCreateView, self).post(request, *args, **kwargs)

class DiscountListView(ListView):
	template_name = "discount_list.html"
	model = Discount

	def get_queryset(self):
		limit = datetime.datetime.now() - timedelta(days=7)
		queryset = Discount.objects.filter(date__gte=limit).order_by('-date')
		return queryset

	def get_context_data(self, **kwargs):
		context = super(DiscountListView, self).get_context_data(**kwargs)
		context['discounts'] = [i for i in range(20)]
		return context

# ----- ostalo -----

class TagsView(View):
	def get(self, *args, **kwargs):
		tags = Tag.objects.all()
		data = serializers.serialize('json', tags)
		return HttpResponse(data, mimetype='application/json')

class MoreRecipesView(TemplateView):
	template_name = "more_recipes.html"

	def get_context_data(self, **kwargs):
		current_page = int(self.request.GET.get('page', 1))

		context = super(MoreRecipesView, self).get_context_data(**kwargs)
		recepies = Recipe.objects.all().order_by('-date')

		limit = 3
		more = 3
		limit_from = limit + more * (current_page - 1)
		limit_to = limit_from + more

		if recepies.count() > limit_to:
			more = True
		else:
			more = False

		context['recipes'] = recepies[limit_from:limit_to]
		context['more'] = more
		context['page'] = current_page + 1
		return context

class LikeView(View):
	def get(self, *args, **kwargs):
		user = self.request.user
		custom_user = CustomUser.objects.get(user=user)
		rp_id = self.request.GET.get('id', '')
		rp = Recipe.objects.get(id=rp_id)
		if rp.user != custom_user:
			rp.like_recipe(custom_user)

		return HttpResponse("")
