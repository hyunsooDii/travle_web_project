from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from city.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin

from django.views.generic import FormView # forms.py와 짝을 맞춤
from django.db.models import Q

from django.utils import timezone

# from country.forms import PostSearchForm

from django.http import FileResponse
import os
from django.conf import settings
# Create your views here.

class CityLV(ListView):
    model = City
    template_name = 'city/city_all.html' # 템플릿 파일명 변경
    context_object_name = 'cities' # 컨텍스트 객체 이름 변병(object_list)
    paginate_by = 5 # 페이지네이션, 페이지당 문서 건 수

class City_indexLV(ListView):
    model = City
    template_name = 'city/city_index.html' # 템플릿 파일명 변경
    context_object_name = 'cities' # 컨텍스트 객체 이름 변병(object_list)
    paginate_by = 5 # 페이지네이션, 페이지당 문서 건 수


# DetailView
class CityDV(DetailView):
    model = City
    template_name = 'city/city_detail.html'
    context_object_name = 'cities'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.get_object()
        country.save()
        return context

class CityCreateView(LoginRequiredMixin, CreateView):
    model = City
    # fields = ['title', 'slug', 'description', 'content', 'tags'] # 모델 view에서 form으로 저것들을 운영하겠다
    fields = ['title', 'main_content','card_content', 'country_index', 'tags']

    success_url = reverse_lazy('city:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.modify_dt = timezone.now() # 조회수가 올라가면 자동으로 날짜가 변경됨을 방지
        response = super().form_valid(form) # form에 저장

        files = self.request.FILES.getlist("files") # file 다운로드
        for file in files:
            attach_file = CityAttachFile(city= self.object, filename= file.name, size= file.size, content_type= file.content_type, upload_file= file)

            attach_file.save()

        return response

class CityUpdateView(OwnerOnlyMixin, UpdateView):
    model = City

    fields = ['title', 'main_content','card_content', 'country_index', 'tags']

    success_url = reverse_lazy('city:index')

    def form_valid(self, form):
        form.instance.modify_dt = timezone.now()


        #  파일 삭제
        # delete_files = self.request.POST["delete_files"]
        delete_files = self.request.POST.getlist("delete_files")
        for fid in delete_files: # fid는 문자열 타입
            file = CityAttachFile.objects.get(id=int(fid)) # PostAttachFile의 object중 id값을 받아옴
            file_path = os.path.join(settings.MEDIA_ROOT, str(file.upload_file)) # 파일 경로
            os.remove(file_path) # 실제 파일 삭제
            file.delete() # 모델 삭제 (테이블 행 삭제)

        response = super().form_valid(form)
        files = self.request.FILES.getlist("files")  # file 다운로드
        for file in files:

            attach_file = CityAttachFile(city= self.object, filename= file.name, size= file.size, content_type= file.content_type, upload_file= file)

            attach_file.save()

        return response

class CityDeleteView(OwnerOnlyMixin, DeleteView) :
    model = City
    success_url = reverse_lazy('city:index')

def download(request, id): # 함수 기반의 view
    file = CityAttachFile.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.upload_file))

    return FileResponse(open(file_path, 'rb')) # 파일의 경로와, rb(read binary)
