from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'backend'

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('gameover/<int:winner>/<int:pk>', views.MatchOver.as_view()),
    path('matches/new/schedule', views.MatchList.as_view()),
    path('browse/city', views.CityList.as_view()),
    path('browse/venue', views.VenueList.as_view()),
    path('users/auth/register/', views.Register.as_view()),
    path('users/auth/login/', views.Login.as_view()),
    path('users/auth/logout/', views.Logout.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
