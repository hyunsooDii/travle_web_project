from django.urls import path, re_path  # re_path = regular expression (정규표현식)
from food.views import *

app_name = 'food'  # 해당 어플리케이션의 네임스페이스 명

urlpatterns = [
    # Example: /country/
    path('', FoodLV.as_view(), name='index'),
    # Example: /country/post/
    path('food/', FoodLV.as_view(), name='index'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', FoodDV.as_view(), name='detail'),

    path('index/', Food_indexLV.as_view(), name='index_view'),

    # Example: /country/add/
    path('add/', FoodCreateView.as_view(), name="add"),

    # Example: /country/99/update/
    path('<int:pk>/update/', FoodUpdateView.as_view(), name="update"),

    # Example: /country/99/delete/
    path('<int:pk>/delete/', FoodDeleteView.as_view(), name="delete"),

    # Example: /country/download/99/
    path('download/<int:id>', download, name='download'),

 ]