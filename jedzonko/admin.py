from django.contrib import admin
from jedzonko.models import (
    Recipe,
    Plan,
    RecipePlan,
    DayName,
    Page,
    Ingredient,
    RecipeIngredients,
)
# Register your models here.


'''Dzięki zarejestrowaniu naszego modelu oraz stworzeniu superużytkownika poprzez manage.py (komenda createsuperuser)
możemy w łatwy sposób zarządzać modelami w bazie danych (dodawać, usuwać). Robimy to poprzez odpalenie aplikacji i przejście
na podstronę /admin. Tam wpisujemy login i hasło utworzone przy tworzeniu superużytkownika i jesteśmy w bazie :).'''
admin.site.register({
    Recipe,
    Plan,
    RecipePlan,
    DayName,
    Page,
    Ingredient,
    RecipeIngredients,
})
