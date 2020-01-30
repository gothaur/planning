from django.core.paginator import Paginator
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
)
from django.utils.decorators import method_decorator
from django.views import View
import random
from jedzonko.models import (
    Recipe,
    Plan,
    DayName,
    RecipePlan,
    Page,
    Ingredient,
    RecipeIngredients,
    DayNames,
)
import json
from django.http import JsonResponse


def redirect_to_last(model_to_find):
    last_item_id = model_to_find.objects.last().pk
    model_name = model_to_find.__name__.lower()
    return redirect(f"/{model_name}/{last_item_id}/")


class InputFilter(View):

    def get(self, request):
        ingredients = serializers.serialize('json', Ingredient.objects.all())
        data = {'data': json.loads(ingredients)}
        return JsonResponse(data)

    def post(self, request):
        json_data = json.loads(request.body)['inputValue']
        ingredients = Ingredient.objects.only('name').filter(name__startswith=json_data).order_by('name')
        ing_json = json.loads(serializers.serialize('json', ingredients))
        data = {'data': ing_json}
        return JsonResponse(data)


class IndexView(View):

    @staticmethod
    def create_days():
        i = 0
        for data in DayNames:
            DayName.objects.create(order=i, day=data.value)
            i += 1

    @staticmethod
    def create_initial_ingredients():
        starting_ingredients = [
            'brukselka', 'ziemniaki', 'fix knorr', 'cebula', 'ząbki czosnku', 'śmietana 18%', 'tymianek',
            'masło', 'cukier', 'mąka', 'jajka', 'płatki owsiane', 'brzoskwinia', 'banan', 'sok pomarańczowy', 'jogurt naturalny',
            'czerwona cebula', 'kasza jaglana', 'sezam', 'sól', 'pieprz', 'pomidor', 'ryż', 'mleko'
        ]
        for item in starting_ingredients:
            Ingredient.objects.create(name=item)

    @staticmethod
    def create_initial_recipes():
        example_recipes = [
            {
                'name': 'Zapiekanka z ziemniakami i brukselką',
                'description': 'Mamusina najlepsza zapiekanka pod słońcem. Można ją podać jako główne danie albo jako kolację. Zgodnie z zalecanimi Makłowicza, podawać z dobrze dobranym winkiem ;)',
                'how_to_prepare': ''' Obierz ziemniaki, a następnie pokrój w plastry. Usuń uszkodzone zewnętrzne liście z brukselki. Następnie umyj brukselkę i osusz. 
                Przekrój brukselki na pół i umieść w misce z ziemniakami.Obierz cebulę i drobno posiekaj. Wymieszaj z tymiankiem, gałką muszkatołową, 
                solą i pieprzem dodaj do brukselki i ziemniaków. Ponownie wymieszaj. Nasmaruj naczynie do pieczenia i napełnij warzywami.
                Ubij śmietanę, mleko, jajka i parmezan. Dopraw solą i pieprzem. Polej tą mieszaniną warzywa. Posyp tartym serem.
                Piecz zapiekankę przez 45 minut w piekarniku rozgrzanym do 170°C. Aby nie spiec za mocno sera, można naczynie okryć folią aluminiową i 
                zdjąć na 5-7 minut przed końcem pieczenia. ''',
                'preparation_time': 45,
                'votes': 18
            },
            {
                'name': 'Ciasteczka Owsiane',
                'description': 'Przepyszne ciasteczka owsiane, podawać z owocami i winkiem',
                'how_to_prepare': '''Masło roztopić. Do czystej miski wsypać płatki owsiane, mąkę, cukier, proszek do pieczenia i ziarna.
                Wlać roztopione masło i wymieszać. Dodać jajka oraz miód jeśli używamy i wymieszać. Jeśli mamy czas, dobrze jest odstawić masę na ok. 1/2 - 1 godzinę.
                Piekarnik nagrzać do 180 stopni C. Blachę wyłożyć papierem do pieczenia. Nabierać łyżkę stołową masy i nakładać na blaszkę formując okręgi i delikatnie je płaszczając.
                Piec przez ok. 15 minut na złoty kolor.''',
                'preparation_time': 45,
                'votes': 12
            },
            {
                'name': 'Koktajl brzoskwiniowy',
                'description': 'Śniadaniowy shake z brzoskwinią i płatkami owsianymi',
                'how_to_prepare': '''Płatki owsiane zalać małą ilością gorącej wody, odstawić na około 10 minut. Namoczone płatki zmiksować z 
                brzoskwinią, obranym bananem, sokiem i jogurtem.''',
                'preparation_time': 15,
                'votes': 24
            },
            {
                'name': 'Burgery buraczane',
                'ingredients': '1 czerwona cebula, 2 duże ząbki czosnku, 1 szklanka kaszy jaglanej, 3 łyżki ziaren sezamu, sól, pieprz',
                'description': 'Burgery buraczane nie tylko dla wegan',
                'how_to_prepare': '''Obierz buraki. Ugotuj kaszę jaglaną - dokładnie wypłucz kaszę pod bieżącą wodę, żeby pozbyć się saponin (inaczej kasza będzie gorzka). Wrzuć do lekko osolonego wrzątku (2,5 szklanki wody na 1 szklankę kaszy).
                Na małym ogniu gotuj ok. 15 minut, aż kasza wchłonie całą wodę. Przestudź.
                Piekarnik nagrzej do 200 stopni Celsjusza.
                Buraki zetrzyj na tarce o grubych oczkach. Cebulę posiekaj naprawdę drobno. Pokrój drobno natkę pietruszki. Czosnek posiekaj bardzo drobno lub zetrzyj na tarce. Na suchej patelni podpraż ziarna słonecznika.
                Wszystkie składniki przełóż do dużej miski i wymieszaj dokładnie. Warto użyć rękawiczek, bo burak bardzo barwi ręce.
                Formuj zgrabne burgery i układaj na blasze wyłożonej papierem do pieczenia. Możesz je dodatkowo posypać odrobiną sezamu.
                Piecz ok. 30-40 minut (grzanie góra-dół, bez termoobiegu). Następnie delikatnie przewróć na drugą stronę i podpiecz jeszcze ok. 10 minut lub 5 minut z funkcją grill.
                Podawaj z podpieczonymi bułkami oraz warzywami i sosami, jakimi lubisz najbardziej :)
                ''',
                'preparation_time': 15,
                'votes': 24
            },
        ]

        for recipe in example_recipes:
            Recipe.objects.create(name=recipe['name'],
                                  description=recipe['description'],
                                  how_to_prepare=recipe['how_to_prepare'],
                                  preparation_time=recipe['preparation_time'],
                                  votes=recipe['votes'])
        return example_recipes

    @staticmethod
    def create_initial_ingredients_for_recipes():
        ingredients = Ingredient.objects.all()
        recipes = Recipe.objects.all()
        for i in range(len(recipes)):
            for ing in range(i*6, 6+i*6):
                RecipeIngredients.objects.create(
                    name=ingredients[ing],
                    quantity=random.randint(3, 40),
                    recipe=recipes[i]
                )

    @staticmethod
    def create_initial_plans():
        for i in range(4):
            Plan.objects.create(name=f"Plan nr {i}", description=f"Opis planu nr {i}")
        last_plan = Plan.objects.last()
        for i in range(10):
            RecipePlan.objects.create(meal_name=f"Nazwa posiłku",
                                      order=i,
                                      recipe=Recipe.objects.order_by('?').first(),
                                      plan=last_plan,
                                      day_name=DayName.objects.order_by('?').first(),
                                      )

    def create_initial_state(self):
        recipes = list(Recipe.objects.all())
        ingredients_for_recipes = RecipeIngredients.objects.all()
        if not recipes:
            self.create_days()
            self.create_initial_recipes()
            self.create_initial_ingredients()
            self.create_initial_plans()
            return self.create_initial_state()
        elif recipes and not ingredients_for_recipes:
            self.create_initial_ingredients_for_recipes()
        return recipes

    def get(self, request):
        recipes = self.create_initial_state()
        random.shuffle(recipes)
        first_active_recipe = recipes[0]
        other_recipes = recipes[1:3]
        context = {
            'first_active_recipe': first_active_recipe,
            'other_recipes': other_recipes,
        }
        return render(request, 'index.html', context)


class RecipeLists(View):

    def get(self, request):
        recipe_name = request.GET.get('recipe_name', "")

        if recipe_name != "":
            recipes_list = Recipe.objects.filter(name__icontains=recipe_name).order_by('-votes', '-created')
        else:
            recipes_list = Recipe.objects.order_by('-votes', '-created')

        paginator = Paginator(recipes_list, 4)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        context = {
            'recipes': recipes,
            'num_pages': range(paginator.num_pages),
        }
        return render(request, 'app-recipes.html', context)


class Dashboard(View):

    def get(self, request):
        plans_number = Plan.objects.count()
        recipes_number = Recipe.objects.count()
        last_added_plan = Plan.objects.all().order_by('-created').first()
        plan_recipes = ""
        if last_added_plan is not None:
            plan_recipes = RecipePlan.objects.filter(plan_id=last_added_plan.id).order_by('day_name__order', 'order')
        context = {
            'plans_number': plans_number,
            'recipes_number': recipes_number,
            'last_added_plan': last_added_plan,
            'plan_recipes': plan_recipes,
        }
        return render(request, 'dashboard.html', context)


class RecipeDetails(View):

    def get(self, request, recipe_id):

        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        except Recipe.DoesNotExist:
            return redirect_to_last(Recipe)
        context = {
            'recipe': recipe,
            'recipe_ingredients': recipe_ingredients,
        }

        return render(request, 'app-recipe-details.html', context)

    def post(self, request, recipe_id):
        username = request.session.get('username', 'default')
        if f"{username}_vas_voted" in request.session and f"{recipe_id}" in request.session:
            messages.add_message(request, messages.ERROR, "Już głosowałaś/głosowałeś")
            return redirect('recipe-details', recipe_id)

        request.session[f"{username}_vas_voted"] = True
        request.session[f"{recipe_id}"] = True
        recipe = Recipe.objects.get(pk=recipe_id)

        if request.POST.get('form') == 'up_vote':
            recipe.votes += 1  # w tym miejscy sa dwie instrukcje if, a nie if..else aby miec
        if request.POST.get('form') == 'down_vote':  # pewnosc ze bedziemy dodawac/odejmowac glosy tylko
            recipe.votes -= 1  # po przycisnieciu odpowiedniego przycisku

        recipe.save()
        return redirect('recipe-details', recipe_id)


class AddRecipe(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        ingredient_list = json.loads(request.POST.get('ingredient_list'))
        name = request.POST.get('recipe_name')
        description = request.POST.get('recipe_description')
        preparation_time = request.POST.get("preparation_time")
        how_to_prepare = request.POST.get("how_to_prepare")
        for key, value in request.POST.items():
            if value == '':
                messages.add_message(request, messages.ERROR, "Wszystkie pola muszą zostać uzupelnione")
                return redirect('add-recipe')

        recipe = Recipe.objects.create(name=name,
                                       description=description,
                                       preparation_time=preparation_time,
                                       how_to_prepare=how_to_prepare)
        self.create_ingredients(ingredient_list, recipe)
        return redirect('recipes')

    def create_ingredients(self, ing_list, recipe):
        for ingredient in ing_list:
            name = ingredient['name'].lower()
            quantity = ingredient['quantity']
            try:
                ing_name_model = Ingredient.objects.get(name=name)
            except Ingredient.DoesNotExist:
                ing_name_model = Ingredient.objects.create(name=name)
            RecipeIngredients.objects.create(
                name=ing_name_model,
                quantity=quantity,
                recipe=recipe,
            )


class ModifyRecipe(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return render(request, 'app-page-not-found.html')
        recipe_ingredients = RecipeIngredients.objects.filter(recipe_id=recipe_id)
        context = {
            'recipe': recipe,
            'recipe_ingredients': recipe_ingredients,
        }
        return render(request, 'app-edit-recipe.html', context)

    def post(self, request, recipe_id):
        ingredient_list = json.loads(request.POST.get('json_value'))
        for key, value in request.POST.items():
            if value.strip() == "" or len(ingredient_list) == 0:
                return self.give_error(request, recipe_id)

        saved_recipe = self.save_recipe(request, recipe_id)
        # w tej tablicy znajdować się będą wszystkie id obiektów do usunięcia z bazy
        ids_to_delete = list(RecipeIngredients.objects.filter(recipe=saved_recipe).values_list('id', flat=True))
        for ingredient in ingredient_list:
            name = ingredient['name']
            quantity = ingredient['quantity']
            if name == "" or quantity == "":
                return self.give_error(request, recipe_id)
            # jeżeli przesłany z formularza id istnieje w bazie to zostaje usunięty z tablicy wyżej
            if int(ingredient['id']) in ids_to_delete:
                ids_to_delete.remove(int(ingredient['id']))
                ingredient_obj = self.give_ingredient(name)
                current_ing_rec = RecipeIngredients.objects.get(id=ingredient['id'])
                current_ing_rec.name = ingredient_obj
                current_ing_rec.quantity = quantity
                current_ing_rec.save()
            # jeżeli został przesłany ID, którego nie ma w bazie to tworzymy nową obiekt zależności
            else:
                ingredient_obj = self.give_ingredient(name)
                RecipeIngredients.objects.create(name=ingredient_obj, quantity=quantity, recipe=saved_recipe)
            # kasujemy te, które zostały w tablicy
        for el_id in ids_to_delete:
            RecipeIngredients.objects.get(id=el_id).delete()
        return redirect('recipe-details', saved_recipe.id)

    def give_error(self, request, recipe_id):
        messages.add_message(request, messages.ERROR, "Wszystkie pola muszą zostać uzupelnione")
        return redirect('modify-recipe', recipe_id)

    def give_ingredient(self, name):
        try:
            ingredient_obj = Ingredient.objects.get(name=name)
        except Ingredient.DoesNotExist:
            ingredient_obj = Ingredient.objects.create(name=name)
        return ingredient_obj

    def save_recipe(self, request, recipe_id):
        name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        how_to_prepare = request.POST.get('how_to_prepare')
        save_type = request.POST.get('save_type')

        # jeśli użytkownik tylko edytuje obecny model
        if save_type == 'save':
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.name = name
            recipe.description = description
            recipe.preparation_time = preparation_time
            recipe.how_to_prepare = how_to_prepare
        else:
            recipe = Recipe.objects.create(name=name,
                                           description=description,
                                           preparation_time=preparation_time,
                                           how_to_prepare=how_to_prepare)
        return recipe


class PlanDetails(View):

    def get(self, request, plan_id):
        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return redirect_to_last(Plan)
        recipe_plans = RecipePlan.objects.filter(plan_id=plan_id).order_by('day_name__order', 'order')
        context = {
            'recipe_plans': recipe_plans,
            'plan': plan,
        }
        return render(request, 'app-details-schedules.html', context)

    def post(self, request, plan_id):
        recipe_plan = RecipePlan.objects.get(pk=int(request.POST.get('recipe_plan_id')))
        recipe_plan.delete()
        return redirect('plan-details', plan_id)


class AddPlan(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        # jezeli ktorekolwiek pole w formularzu nie zostanie uzupelnione
        # tworzymy komunikat do wyswietlenia bledu
        if request.POST.get('name') == "" or request.POST.get('description') == "":
            # w tym miejscu dodajemy komunikatey do obiektu messages
            messages.add_message(request, messages.ERROR, "Wszystkie pola musza zostać uzupełnione")
            return redirect('add-plan')

        name = request.POST.get('name')
        description = request.POST.get('description')
        # tworzymy nowy obiekt klasy Plan i dodajemy go do naszej bazy danych
        plan = Plan.objects.create(name=name, description=description)
        # metoda redirect sluzy do prekierowywania na odpowiednie strony
        # (dlatego w urlsach stosujemy atrybut name)
        return redirect('plan-details', plan.id)


class AddRecipeToPlan(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request, plan_id=0, recipe_id=0):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        context = {
            'plans': plans,
            'recipes': recipes,
            'days': days,
            'plan_id': plan_id,
            'recipe_id': recipe_id,
        }
        return render(request, 'app-schedules-meal-recipe.html', context)

    def post(self, request, plan_id=0, recipe_id=0):
        for key, value in request.POST.items():
            if value == '':
                messages.add_message(request, messages.ERROR, "Wszystkie pola muszą zostać uzupelnione")
                return redirect('add-recipe-to-plan')
        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order')
        recipe = Recipe.objects.get(pk=int(request.POST.get('recipe')))
        plan = Plan.objects.get(pk=int(request.POST.get('plan')))
        day_name = DayName.objects.get(day=request.POST.get('day_name'))
        RecipePlan.objects.create(meal_name=meal_name, recipe=recipe, plan=plan,
                                  order=order, day_name=day_name)
        return redirect('plan-details', plan.id)


class PlanLists(View):

    def get(self, request):
        plan_lists = Plan.objects.order_by('name')
        paginator = Paginator(plan_lists, 50)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        context = {
            'plans': plans,
            'num_pages': range(paginator.num_pages),
        }
        return render(request, 'app-schedules.html', context)


class DeletePlanFromPlanList(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request, plan_id):
        try:
            plan = Plan.objects.get(pk=plan_id)
            plan.delete()
        except Plan.DoesNotExist:
            return render(request, 'app-page-not-found.html')
        return redirect('plans')


class DeleteRecipe(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            recipe.delete()
        except Recipe.DoesNotExist:
            return render(request, 'app-page-not-found.html')
        return redirect('recipes')


class SlugPage(View):

    def get(self, request, title=""):
        try:
            slug = Page.objects.get(slug=title)
            context = {
                'slug': slug,
            }
            return render(request, 'slug_page.html', context)
        except Page.DoesNotExist:
            return redirect(f"/#{title}")


class ModifyPlan(View):

    @method_decorator(login_required(login_url='/users/login/1'))
    def get(self, request, plan_id):
        try:
            plan = Plan.objects.get(pk=plan_id)
        except Plan.DoesNotExist:
            return render(request, 'app-page-not-found.html')
        context = {
            'plan': plan,
        }
        return render(request, 'app-edit-schedules.html', context)

    def post(self, request, plan_id):
        name = request.POST.get('plan_name', "")
        description = request.POST.get('plan_description', '')
        save_type = request.POST.get('save_type')
        if name == '' or description == '':
            messages.add_message(request, messages.ERROR, "Wszystkie pola muszą zostać uzupelnione")
            return redirect('edit-plan', plan_id)

        plan = Plan.objects.get(id=plan_id)
        if save_type == 'save':
            plan.name = name
            plan.description = description
            plan.save()
        else:
            plan = Plan.objects.create(name=name, description=description)
        return redirect('plan-details', plan.id)


class PageNotFound(View):

    def get(self, request):
        return render(request, 'app-page-not-found.html')
