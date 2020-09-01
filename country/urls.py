from django.urls import path, re_path  # re_path = regular expression (정규표현식)
from country.views import *

app_name = 'country'  # 해당 어플리케이션의 네임스페이스 명

urlpatterns = [
    # Example: /country/
    path('', CountryLV.as_view(), name='index'),
    # Example: /country/post/
    path('country/', CountryLV.as_view(), name='index'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', CountryDV.as_view(), name='detail'),
    re_path(r'^(?P<pk>\d+)/$', Country_merge_LV.as_view(), name='country_detail'),
    path('index/', Country_index_LV.as_view(), name='index_view'),

    # Example: /country/add/
    path('add/', CountryCreateView.as_view(), name="add"),

    # Example: /country/99/update/
    path('<int:pk>/update/', CountryUpdateView.as_view(), name="update"),

    # Example: /country/99/delete/
    path('<int:pk>/delete/', CountryDeleteView.as_view(), name="delete"),

    # Example: /country/download/99/
    path('download/<int:id>', download, name='download'),

 ]