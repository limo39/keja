from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    
    # Property URLs
    path('property/<int:pk>/', views.property_detail, name="property_detail"),
    path('add-property/', views.add_property, name="add_property"),
    path('edit-property/<int:pk>/', views.edit_property, name="edit_property"),
    path('my-properties/', views.my_properties, name="my_properties"),
    path('delete-property/<int:pk>/', views.delete_property, name="delete_property"),
    
    # Legacy room URLs (keeping for backward compatibility)
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]