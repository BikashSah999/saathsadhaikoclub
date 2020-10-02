from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('participate/<str:name>', views.participate, name='participate'),
    path('winner_select', views.winner_select, name='winner_select'),
    path('currentwinner', views.currentwinner, name="currentwinner" ),
    path('overallwinner', views.overallwinner, name='overallwinner')
]