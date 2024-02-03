from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipe
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from django.shortcuts import render
from django.http import JsonResponse
import requests
# Create your views here.


class Recipe_list(LoginRequiredMixin,ListView):
    model = Recipe
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = context['recipes'].filter(user=self.request.user)
        return context


class Recipe_detail(LoginRequiredMixin,DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe_list_base/recipe_detail.html'


class Recipe_create(LoginRequiredMixin,CreateView):
    model = Recipe
    fields = ['title', 'comments', 'time_needed']
    success_url = reverse_lazy('Recipes')

    def form_valid(self, form):
        form.instance.user = self.request.user

        query = form.cleaned_data['title']
        api_url = f'https://api.api-ninjas.com/v1/recipe?query={query}'
        headers = {'X-Api-Key': 'zGKQ2YkpGrjgPf2P/1jrEw==pZaNKj9JEPhitfdg'}
        response = requests.get(api_url, headers=headers)
        api_url2 = f'https://www.themealdb.com/api/json/v1/1/search.php?s={query}'
        response2 = requests.get(api_url2)

        if response.status_code == 200:
            recipes_data = response.json()

            if response2.status_code == 200:
                recipes_data2 = response2.json()

                if recipes_data2 and 'meals' in recipes_data2 and recipes_data2['meals']:
                    first_recipe2 = recipes_data2['meals'][0]
                    picture = first_recipe2.get('strMealThumb')
                    if picture is not None:
                        form.instance.picture_url = picture
                    else:
                        image_path = r'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
                        form.instance.picture_url = image_path
                else:
                    image_path = r'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
                    form.instance.picture_url = image_path
            else:
                print("Error:", response.status_code, response.text)

            if recipes_data and isinstance(recipes_data, list):
                first_recipe = recipes_data[0]
                ingredients = first_recipe.get('ingredients', 'No ingredients')
                instructions = first_recipe.get('instructions', 'No instructions')
                description = f"Ingredients: {ingredients} <br> <br> Instructions: {instructions}"

                form.instance.description = description

                return super(Recipe_create, self).form_valid(form)
            else:
                return render(self.request, 'recipe_list_base/recipe_list.html', {'error': 'No recipe found.'})
        else:
            return render(self.request, 'recipe_list_base/recipe_list.html', {'error': 'API Error'})


class Recipe_edit(LoginRequiredMixin,UpdateView):
    model = Recipe
    fields = ['title', 'comments', 'time_needed']
    success_url = reverse_lazy('Recipes')

    def form_valid(self, form):
        form.instance.user = self.request.user

        query = form.cleaned_data['title']
        api_url = f'https://api.api-ninjas.com/v1/recipe?query={query}'
        headers = {'X-Api-Key': 'zGKQ2YkpGrjgPf2P/1jrEw==pZaNKj9JEPhitfdg'}
        response = requests.get(api_url, headers=headers)
        api_url2 = f'https://www.themealdb.com/api/json/v1/1/search.php?s={query}'
        response2 = requests.get(api_url2)

        if response.status_code == 200:
            recipes_data = response.json()

            if response2.status_code == 200:
                recipes_data2 = response2.json()

                if recipes_data2 and 'meals' in recipes_data2 and recipes_data2['meals']:
                    first_recipe2 = recipes_data2['meals'][0]
                    picture = first_recipe2.get('strMealThumb')
                    if picture is not None:
                        form.instance.picture_url = picture
                    else:
                        image_path = r'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
                        form.instance.picture_url = image_path
                else:
                    image_path = r'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
                    form.instance.picture_url = image_path
            else:
                print("Error:", response.status_code, response.text)

            if recipes_data and isinstance(recipes_data, list):
                first_recipe = recipes_data[0]
                ingredients = first_recipe.get('ingredients', 'No ingredients')
                instructions = first_recipe.get('instructions', 'No instructions')
                description = f"Ingredients: {ingredients} <br> <br> Instructions: {instructions}"

                form.instance.description = description

                return super(Recipe_edit, self).form_valid(form)
            else:
                return render(self.request, 'recipe_list_base/recipe_list.html', {'error': 'No recipe found.'})
        else:
            return render(self.request, 'recipe_list_base/recipe_list.html', {'error': 'API Error'})


class Recipe_delete(LoginRequiredMixin,DeleteView):
    model = Recipe
    context_object_name = 'recipe'
    success_url = reverse_lazy('Recipes')


class Recipe_login(LoginView):
    template_name = "recipe_list_base/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('Recipes')


class Recipe_signup(FormView):
    template_name = "recipe_list_base/signup.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('Recipes')
    form_class = UserCreationForm

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
            return super(Recipe_signup, self).form_valid(form)

