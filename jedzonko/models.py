from django.db import models
from enum import Enum


class Ingredient(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    description = models.TextField()
    how_to_prepare = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    preparation_time = models.SmallIntegerField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64)


class Plan(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')

    def __str__(self):
        return self.name


class DayNames(Enum):
    MON = 'Poniedziałek'
    TUE = 'Wtorek'
    WED = 'Środa'
    THU = 'Czwartek'
    FRI = 'Piątek'
    SAT = 'Sobota'
    SUN = 'Niedziela'


class DayName(models.Model):
    day = models.CharField(max_length=32, choices=[(tag.name, tag.value) for tag in DayNames])
    order = models.SmallIntegerField(unique=True)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=32)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(unique=True)
