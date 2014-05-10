from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView
from django.views.generic.detail import DetailView

from .models import *

class Index(TemplateView):
	template_name = "home.html"

	def render_to_response(self, context, **response_kwargs):
		# recepie_list = Recipe.objects.all().order_by('like', 'date')[:10]
		# context['recepies'] = recepie_list
		return super(Index, self).render_to_response(context, **response_kwargs)

# ----- korisnici -----

class RegistrationView(TemplateView):
	template_name = "registration.html"

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
		context['proba'] = [i for i in range(20)]
		return context


class RecipeCreateView(CreateView):
	template_name = "recipe_create.html"
	# model = Recipe

class RecipeDetailViewv(DetailView):
	template_name = "recipe_detail.html"
	# model = Recipe

class RecipeSearchView(ListView):
	template_name = "recipe_search.html"
	object_list = range(20)
	# model = Recipe

# ----- akcije -----

class DiscountCreateView(CreateView):
	template_name = "discount_create.html"
	# model = Discount

class DiscountListView(ListView):
	template_name = "discount_list.html"
	# model = Discount

