from django.urls import (
    path,
    include,
)

from users import views

urlpatterns = [
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('login/<int:redirected>', views.Login.as_view(), name='login'),
]
