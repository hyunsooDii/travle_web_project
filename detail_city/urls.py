from django.urls import path, re_path  # re_path = regular expression (정규표현식)
from detail_city.views import *

app_name = 'detail_city'  # 해당 어플리케이션의 네임스페이스 명

urlpatterns = [
    # Example: /blog/
    path('', Detail_cityLV.as_view(), name='index'),
    # Example: /blog/post/
    path('detail_city/', Detail_cityLV.as_view(), name='index'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', Detail_cityDV.as_view(), name='detail'),
    path('<pk>', Detail_city_merge_LV.as_view(), name='country_detail'),
    path('index/', Detail_cityindexLV.as_view(), name='index_view'),
    # slug라는 이름의 경로변수를 배정, w - word(알파벳, 숫자), + - 한개 이상 나온다
    # 슬러그라는 환경변수로 공백없이 글자, 숫자, 대시만 허용한다, 마지막은 /로 끝나야 하는 것을 받겠다.
    # ^ - 이걸로 시작한다, $ - 이걸로 끝난다 ?
    # ex)^h - h로 시작한다, s$ - s로 끝난다
    # ex) ^h(.) 글자 하나, ^h(.)* - 글자 하나 이상

    # Example: /blog/add/
    path('add/', Detail_cityCreateView.as_view(), name="add"),

    # Example: /blog/99/update/
    path('<int:pk>/update/', Detail_cityUpdateView.as_view(), name="update"),

    # Example: /blog/99/delete/
    path('<int:pk>/delete/', Detail_cityDeleteView.as_view(), name="delete"),

    # Example: /blog/download/99/
    path('download/<int:id>', download, name='download'),

 ]