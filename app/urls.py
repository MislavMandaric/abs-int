from django.conf.urls import patterns, include, url

from .views import Index, RegistrationView, ProfileView, LoginView, LogoutView, RecipeCreateView, RecipeDetailViewv, RecipeSearchView, DiscountCreateView, DiscountListView

urlpatterns = patterns('',
	 url(r'^', Index.as_view(), name="index"),
	 url(r'^registracija/', RegistrationView.as_view(), name="registration"),
	 url(r'^profil/', ProfileView.as_view(), name="profile"),
	 url(r'^prijava/', LoginView.as_view(), name="login"),
	 url(r'^odjava', LogoutView.as_view(), name="logout"),
	 
	 url(r'^recepti/stvaranje', RecipeCreateView.as_view(), name="recipe_create"),
	 url(r'^recepti/pretraga', RecipeSearchView.as_view(), name="recipe_search"),
	 url(r'^recepti/(?P<id>[0-9]+)/$', RecipeDetailViewv.as_view(), name="recipe_detail"),
	 
	 url(r'^akcije/popis', DiscountListView.as_view(), name="discount_list"),
	 url(r'^akcije/(?P<id>[0-9]+)/$', DiscountCreateView.as_view(), name="discount_create"),
)
