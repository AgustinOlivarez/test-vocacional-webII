from django.urls import path
from . import views
from .views import SolicitudesView, panel_solicitudes, login_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('api/solicitudes/', SolicitudesView.as_view(), name='solicitudes'),
    path('panel/', panel_solicitudes, name='panel_solicitudes'),

    # Autenticación
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', views.register_view, name='register'),
]