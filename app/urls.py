from django.conf.urls import patterns, include, url
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
	url(r'^profil', login_required(ProfileView.as_view()), name="profile"),
	url(r'^registracija', RegistrationView.as_view(), name="registration"),
	url(r'^prijava', 'django.contrib.auth.views.login',{'authentication_form': CustomAuthenticationForm}, name = "login" ),
	url(r'^odjava', 'django.contrib.auth.views.logout', {'next_page': '/'}, name = "logout"),

	url(r'^recepti/(?P<pk>\d+)/$', RecipeDetailView.as_view(), name="recipe_detail"),
	url(r'^recepti/dodaj-novi', login_required(RecipeCreateView.as_view()), name="recipe_create"),
	url(r'^recepti', RecipesView.as_view(), name="recipes"),
	
	url(r'^pretraga', RecipeSearchView.as_view(), name="recipe_search"),
	
	url(r'^akcije/dodaj-novu', login_required(DiscountCreateView.as_view()), name="discount_create"),
	url(r'^akcije', DiscountListView.as_view(), name="discount_list"),
	
	url(r'^vise-recepata', MoreRecipesView.as_view(), name="more_recipes"),

	url(r'^tagovi', TagsView.as_view(), name="tagovi"),
	url(r'^like', LikeView.as_view(), name="like"),
	url(r'^$', Index.as_view(), name="index"),
)
