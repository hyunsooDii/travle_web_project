# 템플릿 파일만 관리하는 기능
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, CreateView, ArchiveIndexView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import auth
from country.models import Country
from board.models import Board

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # 모델 인스턴스 얻기
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)

# TemplateView

def register(request):
    # register으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == "GET":
        return render(request,'registration/register.html')
    elif request.method == "POST":
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        email = request.POST.get('email', None)
        nickname = request.POST.get('nickname',None)
        re_password  = request.POST.get('re_password', None)
        res_data={}
        if not(username and password and re_password):
            res_data['error'] = "모든 값을 입력해야합니다."
        elif password != re_password:
            res_data['error'] = "비밀번호가 다릅니다."
        else:
            accounts = User(
                username=username,
                password=make_password(password),
                first_name = nickname,
                email = email,
            )
            accounts.save()
            return redirect('login')
        return render(request, 'registration/register.html/',res_data)

def login(request):
    if request.method == "GET":
        return render(request, 'registration/login.html/')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password = password)
        res_data = {}
        if user is not None:
                auth.login(request,user)
                return redirect('/')
        else:
                res_data['error'] = "아이디 혹은 비밀번호가 틀렸습니다."
                return render(request,'registration/login.html/',res_data)
    return render(request,'registration/login.html/')

def logout(request):
    if request.method == "GET":
        auth.logout(request)
        return redirect('/')

class PasswordReset(auth_views.PasswordResetView):
    template_name='registration/password_reset.html/'

class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name='registration/password_reset_done.html/'

class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name='registration/password_reset_confirm.html/'

class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name='registration/password_reset_complete.html/'

class HomeView(TemplateView):
    template_name = 'main.html'
    date_field = 'modify_dt'
    allow_empty = True  # 내용이 없어도 허용하겠다, 즉 오늘날짜 기사가 없어서 Home이 안나오는걸 방지

    def get_context_data(self, **kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        country = Country.objects.all()
        board = Board.objects.all()
        context['countries'] = country
        context['boards'] = board
        return context


class UserCreateView(CreateView):
    template_name = 'registration/register_test.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

    nickname = forms.CharField(required=True)
    email = forms.EmailField(label=("Email address"), required=True,help_text=("Required."))

    class Meta:
        fields = ("username", "email", "password1", "password2",)


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'
    allow_empty = True # 내용이 없어도 허용하겠다, 즉 오늘날짜 기사가 없어서 Home이 안나오는걸 방지

    date_field = 'modify_dt'
    allow_empty = True  # 내용이 없어도 허용하겠다, 즉 오늘날짜 기사가 없어서 Home이 안나오는걸 방지
    def get_context_data(self, **kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        country = Country.objects.all()
        board = Board.objects.all()
        context['countries'] = country
        context['boards'] = board
        return context

    allow_empty = True # 내용이 없어도 허용하겠다, 즉 오늘날짜 기사가 없어서 Home이 안나오는걸 방지

