from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
     path('category/<str:category>/<str:sub_category>/', views.event_list_by_category, name='event_list_by_category'),
    path('event/create/', views.event_create, name='event_create'),  
    path('logout/', views.user_logout, name='logout'),
    path('events/', views.event_list, name='event_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('sifremi-unuttum/', views.password_reset, name='password_reset'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'), 
    path('profile/update/<str:username>/', views.profile_update, name='profile_update'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),  
    path('event/<int:id>/join/', views.join_event, name='join_event'),   
     path('category/<int:category_id>/', views.category_events, name='category_events'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
