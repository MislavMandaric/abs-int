from datetime import timedelta

from django.core import serializers
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView
from django.views.generic.detail import DetailView

from .models import *
from .forms import SearchForm

class Index(TemplateView):
	template_name = "home.html"

	def render_to_response(self, context, **response_kwargs):
		# recepie_list = Recipe.objects.all().order_by('like', 'date')[:10]
		# context['recepies'] = recepie_list
		return super(Index, self).render_to_response(context, **response_kwargs)

# ----- korisnici -----

class RegistrationView(TemplateView):
	template_name = "registration/registration.html"

class ProfileView(TemplateView):
	template_name = "profile.html"

class LoginView(View):
	def post(self, request, *args, **kwargs):
	# logirati korisnika
		return HttpResponseRedirect(reverse('profile'))

class LogoutView(View):
	def post(self, request, *args, **kwargs):
	# odlogirati korisnika
		return HttpResponseRedirect((reverse('index')))

# ----- recepti -----

class RecipesView(TemplateView):
	template_name = 'recipes.html'

	def get_context_data(self, **kwargs):
		context = super(RecipesView, self).get_context_data(**kwargs)
		context['recipes'] = [i for i in range(20)]
		return context

class RecipeCreateView(CreateView):
	template_name = "recipe_create.html"
	model = Recipe

class RecipeDetailView(DetailView):
	template_name = "recipe_detail.html"
	model = Recipe

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
				filters_categories |= Q(recipe_categories__categorie__name__icontains=cat)	

		filters_tags = Q()
		if tags:
			tags_list = tags.split(', ')
			for tag in tags_list:
				filters_tags |= Q(recipe_tags__tag__name__icontains=tag)

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

class DiscountCreateView(CreateView):
	template_name = "discount_create.html"
	# model = Discount

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

class TagsView(View):
    def get(self, *args, **kwargs):
        tags = Tag.objects.all()
        data = serializers.serialize('json', tags)
        return HttpResponse(data, mimetype='application/json')
