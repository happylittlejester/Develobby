from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path("coming-soon/", views.coming_soon, name="coming_soon"),

    path('faq/', views.faq, name='faq'),

    path('store/', views.store, name='store'),

    path('hobby_panel/', views.hobby_panel, name='hobby_panel'),
    
    path("add-hobby/<int:detail_id>/", views.add_hobby_choice, name="add_hobby_choice"),
    path("remove-hobby/<int:detail_id>/", views.remove_hobby_choice, name="remove_hobby_choice"),

    path('hobbies/', views.hobbies, name='hobbies'),
    path("hobby/<int:detail_id>/", views.hobby_detail, name="hobby_detail"),

    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile/', views.profile, name='profile'),


    path('challenge/done/<int:challenge_id>/', views.challenge_done, name='challenge_done'),
    path('challenge/collect/<int:challenge_id>/', views.challenge_collect, name='challenge_collect'),
]

