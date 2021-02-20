from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path(
        'login/',
        views.CustomLoginView.as_view(template_name="login.html"), name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(), name='logout'
    ),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('confirmar_cadastro/', views.ConfirmarCadastro.as_view(),
         name='confirmar_cadastro')
]
