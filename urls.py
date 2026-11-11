from .analytics_views import analytics_dashboard
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import MobileLoginForm

urlpatterns = [
    path('analytics/', analytics_dashboard, name='analytics'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=MobileLoginForm,
        ),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout',
    ),

    path('add-student/', views.register_student, name='add_student'),
    path('edit-student/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:pk>/', views.delete_student, name='delete_student'),
]
