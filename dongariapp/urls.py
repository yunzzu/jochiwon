from django.urls import path
from . import views

app_name = 'dongariapp'


urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
    #path('<int:pk>/', views.single_post_page),
    #path('', views.index),

]