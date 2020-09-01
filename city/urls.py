from django.urls import path, re_path  # re_path = regular expression (정규표현식)
from city.views import *


app_name = 'city'  # 해당 어플리케이션의 네임스페이스 명

urlpatterns = [
    # Example: /city/
    path('', CityLV.as_view(), name='index'),
    # Example: /city/post/
    path('city/', CityLV.as_view(), name='index'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', CityDV.as_view(), name='detail'),

    path('index/', City_indexLV.as_view(), name='index_view'),

    # Example: /city/add/
    path('add/', CityCreateView.as_view(), name="add"),

    # Example: /city/99/update/
    path('<int:pk>/update/', CityUpdateView.as_view(), name="update"),

    # Example: /city/99/delete/
    path('<int:pk>/delete/', CityDeleteView.as_view(), name="delete"),

    # Example: /city/download/99/
    path('download/<int:id>', download, name='download'),

 ]