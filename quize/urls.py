from django.urls import path
from .views import *



urlpatterns = [
    path('register/', user_register, name='register_page'),
    path('login/', user_login, name='login_page'),
    path('logout/', user_logout, name='logout_page'),

    path('profile/', profile, name='profile'),
    path('update-profile/', profiel_update, name='profiel_update'),
    path('', dashboard, name='dashboard'),
    
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('result/<int:quiz_id>/', result_view, name='result'),
    path('add-quiz/', add_quiz, name='add_quiz'),
]
