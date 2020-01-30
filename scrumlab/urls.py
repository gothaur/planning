from django.contrib import admin
from django.urls import (
    path,
    include,
    re_path,
)
from jedzonko import views


urlpatterns = [
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('inputFilter/', views.InputFilter.as_view(), name='inputFilter'),
    path('', views.IndexView.as_view(), name='index'),
    path('recipe/list/', views.RecipeLists.as_view(), name='recipes'),
    path('main/', views.Dashboard.as_view(), name='dashboard'),
    path('plan/list/', views.PlanLists.as_view(), name='plans'),
    path('recipe/<int:recipe_id>/', views.RecipeDetails.as_view(), name='recipe-details'),
    path('recipe/add/', views.AddRecipe.as_view(), name='add-recipe'),
    path('recipe/modify/<int:recipe_id>/', views.ModifyRecipe.as_view(), name='modify-recipe'),
    path('plan/<int:plan_id>/', views.PlanDetails.as_view(), name='plan-details'),
    path('plan/add/', views.AddPlan.as_view(), name='add-plan'),
    path('plan/add-recipe/', views.AddRecipeToPlan.as_view(), name='add-recipe-to-plan'),
    path('plan/add-recipe/<int:plan_id>/<int:recipe_id>/', views.AddRecipeToPlan.as_view(), name='add-recipe-to-plan'),
    path('<slug:title>/', views.SlugPage.as_view(), name='slug_page'),
    path('plan/edit/<int:plan_id>', views.ModifyPlan.as_view(), name='edit-plan'),
    path('plan/delete/<int:plan_id>/', views.DeletePlanFromPlanList.as_view(), name='delete-plan'),
    path('recipe/delete/<int:recipe_id>/', views.DeleteRecipe.as_view(), name='delete-recipe'),
    re_path(r'^.+', views.PageNotFound.as_view(), name='404-not-found'),
]
