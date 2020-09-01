from django.urls import path, re_path  # re_path = regular expression (정규표현식)
from festival.views import *

app_name = 'festival'  # 해당 어플리케이션의 네임스페이스 명

urlpatterns = [
    # Example: /blog/
    path('', FestivalLV.as_view(), name='index'),
    # Example: /blog/post/
    path('festival/', FestivalLV.as_view(), name='index'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', FestivalDV.as_view(), name='detail'),
    path('index/', Festival_indexLV.as_view(), name='index_view'),
    # slug라는 이름의 경로변수를 배정, w - word(알파벳, 숫자), + - 한개 이상 나온다
    # 슬러그라는 환경변수로 공백없이 글자, 숫자, 대시만 허용한다, 마지막은 /로 끝나야 하는 것을 받겠다.
    # ^ - 이걸로 시작한다, $ - 이걸로 끝난다 ?
    # ex)^h - h로 시작한다, s$ - s로 끝난다
    # ex) ^h(.) 글자 하나, ^h(.)* - 글자 하나 이상

    # Example: /blog/add/
    path('add/', FestivalCreateView.as_view(), name="add"),

    # Example: /blog/99/update/
    path('<int:pk>/update/', FestivalUpdateView.as_view(), name="update"),

    # Example: /blog/99/delete/
    path('<int:pk>/delete/', FestivalDeleteView.as_view(), name="delete"),

    # Example: /blog/download/99/
    path('download/<int:id>', download, name='download'),

 ]