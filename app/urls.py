from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('photos/new/', views.photos_new, name='photos_new'),
    path('photos/<int:pk>/', views.photos_detail, name='photos_detail'),
    path('photos/<int:pk>/delete/', views.photos_delete, name='photos_delete'),
    path('photos/<str:category>/', views.photos_category, name='photos_category'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contact/', views.contact, name='contact'),
    #path('testuser/', views.contact, name='testuser'),
    path('user_information/<int:pk>/', views.UserDetail.as_view(), name='user_information'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('photos/<int:pk>/like/', views.like, name='like'),
    path('user_list/<int:pk>/', views.user_list, name='user_list'),
    path('user_list/<int:pk>/follow/', views.follow, name='follow'),
]
