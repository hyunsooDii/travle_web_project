from django.urls import path, re_path  # re_path = regular expression (정규표현식)
from board.views import *

app_name = 'board'  # 해당 어플리케이션의 네임스페이스 명

urlpatterns = [
    # Example: /board/
    path('', BoardListLV.as_view(), name='index'),
    # Example: /board/post/
    path('board/', BoardListLV.as_view(), name='index'),

    #path('board/board_list',BoardList.as_view(), name = 'board_list'),
    re_path(r'^post/(?P<pk>[-\w]+)/$', BoardDV.as_view(), name='detail'),

    re_path('comment/', add_comment_to_board, name='add_comment_to_board'),

    # slug라는 이름의 경로변수를 배정, w - word(알파벳, 숫자), + - 한개 이상 나온다
    # 슬러그라는 환경변수로 공백없이 글자, 숫자, 대시만 허용한다, 마지막은 /로 끝나야 하는 것을 받겠다.
    # ^ - 이걸로 시작한다, $ - 이걸로 끝난다 ?
    # ex)^h - h로 시작한다, s$ - s로 끝난다
    # ex) ^h(.) 글자 하나, ^h(.)* - 글자 하나 이상

    # Example: /blog/tag/
    path('tag/', TagCloudTV.as_view(), name='tag_cloud'),


    # Example : /blog/tag/tagname
    path('tag/<str:tag>/', TaggedObjectLV.as_view(),name='tagged_object_list'),

    # Example: /blog/search
    path('search/', SearchFormView.as_view(), name='search'),


    # Example: /blog/add/
    path('add/', BoardCreateView.as_view(), name="add"),

    # Example: /blog/99/update/
    path('<int:pk>/update/', BoardUpdateView.as_view(), name="update"),

    # Example: /blog/99/delete/
    path('<int:pk>/delete/', BoardDeleteView.as_view(), name="delete"),

    # Example: /blog/download/99/
    path('download/<int:id>', download, name='download'),

 ]