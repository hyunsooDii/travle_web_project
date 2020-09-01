from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from board.models import *
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, \
    DayArchiveView, TodayArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin

from django.views.generic import FormView  # forms.py와 짝을 맞춤
from django.db.models import Q

from django.utils import timezone

from board.forms import BoardSearchForm

from django.http import FileResponse
import os
from django.conf import settings
from board.forms import *


# Create your views here.

# ListView
class BoardLV(ListView):
    model = Board
    template_name = 'board/board_all.html'  # 템플릿 파일명 변경
    context_object_name = 'boards'  # 컨텍스트 객체 이름 변병(object_list)
    paginate_by = 5  # 페이지네이션, 페이지당 문서 건 수


class BoardListLV(ListView):
    model = Board
    template_name = 'board/board_list.html'
    context_object_name = 'boards'


# DetailView
class BoardDV(DetailView):
    model = Board
    template_name = 'board/board_detail.html'
    context_object_name = 'boards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board = self.get_object()
        board.read_cnt += 1
        board.save()
        return context


# ArchiveView
class BoardAV(ArchiveIndexView):
    model = Board
    date_field = 'modify_dt'


class BoardYAV(YearArchiveView):
    model = Board
    date_field = 'modify_dt'
    make_object_list = True


class BoardMAV(MonthArchiveView):
    model = Board
    date_field = 'modify_dt'
    month_format = '%m'  # 숫자로 쓰기 위해 바꿈, 기본은 january, 등으로 나옴


class BoardDAV(DayArchiveView):
    model = Board
    date_field = 'modify_dt'
    month_format = '%m'


class BoardTAV(TodayArchiveView):
    model = Board
    date_field = 'modify_dt'
    month_format = '%m'


# Tag view

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Board

    def get_queryset(self):
        return Board.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']

        return context


# FormView

class SearchFormView(FormView):
    form_class = BoardSearchForm
    template_name = 'board/board_search.html'

    def form_valid(self, form):  # 유효성 검사를 통과했을 때 매개변수 form은 forms.py의 search_word
        searchWord = form.cleaned_data['search_word']
        board_list = Board.objects.filter(  # where 절을 쓰고싶을때 filter를 사용
            Q(title__icontains=searchWord) |  # title like 'searchword' 뜻 Q는 Query의 약자
            Q(description__icontains=searchWord) |
            Q(content__icontains=searchWord)
        ).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = board_list

        return render(self.request, self.template_name, context)


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board

    fields = ['country_index', 'title', 'content', 'star']

    success_url = reverse_lazy('board:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.modify_dt = timezone.now()  # 조회수가 올라가면 자동으로 날짜가 변경됨을 방지
        response = super().form_valid(form)  # form에 저장

        files = self.request.FILES.getlist("files")  # file 다운로드
        for file in files:
            attach_file = BoardAttachFile(board=self.object, filename=file.name, size=file.size,
                                          content_type=file.content_type, upload_file=file)

            attach_file.save()

        return response


class BoardUpdateView(OwnerOnlyMixin, UpdateView):
    model = Board
    fields = ['country_index', 'title', 'content', 'star']
    success_url = reverse_lazy('board:index')

    def form_valid(self, form):
        form.instance.modify_dt = timezone.now()
        delete_files = self.request.POST.getlist("delete_files")
        for fid in delete_files:  # fid는 문자열 타입
            file = BoardAttachFile.objects.get(id=int(fid))  # PostAttachFile의 object중 id값을 받아옴
            file_path = os.path.join(settings.MEDIA_ROOT, str(file.upload_file))  # 파일 경로
            os.remove(file_path)  # 실제 파일 삭제
            file.delete()  # 모델 삭제 (테이블 행 삭제)

        response = super().form_valid(form)
        files = self.request.FILES.getlist("files")  # file 다운로드
        for file in files:
            attach_file = BoardAttachFile(post=self.object, filename=file.name, size=file.size,
                                          content_type=file.content_type, upload_file=file)

            attach_file.save()

        return response


class BoardDeleteView(OwnerOnlyMixin, DeleteView):
    model = Board
    success_url = reverse_lazy('board:index')


def download(request, id):  # 함수 기반의 view
    file = BoardAttachFile.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.upload_file))

    return FileResponse(open(file_path, 'rb'))  # 파일의 경로와, rb(read binary)


def add_comment_to_board(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.save()
            return redirect('board:detail', pk=board_id)
    else:
        form = CommentForm()
    return render(request, 'board/add_comment_to_board.html', {'form': form})
