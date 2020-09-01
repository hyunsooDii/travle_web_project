from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from country.models import Country
from django.core.validators import MinValueValidator,MaxValueValidator
from tinymce.models import HTMLField

class Board(models.Model):

    country_index = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='COUNTRY_INDEX', blank=True, null=True)
    city = models.CharField(verbose_name='CITY', max_length= 50, null=True)
    title = models.CharField(verbose_name='TITLE', max_length=50)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)],default=0)
    content = HTMLField('CONTENT')
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE')
    tags = TaggableManager(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True) #작성자

    read_cnt = models.IntegerField(default=0)

    class Meta:  # Content에 대해서 추가정보를 관리하는 정보를 메타정보라고 함
        verbose_name = 'board'  # 단수
        verbose_name_plural = 'boards'  # 복수
        db_table = 'board'  # 테이블명 재정의
        ordering = ('-modify_dt',)  # orderby 절, -이면 내림차순순 <- 저건 튜플 (,) 가 있긴 때문에

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # 현재 데이터의 절대 경로 추출
        return reverse('board:detail', args=(self.pk,))

    def get_previous(self):  # 이젠 데이터 추출
        return self.get_previous_by_modify_dt()

    def get_next(self):  # 다음 데이터 추출
        return self.get_next_by_modify_dt()

    def first_image(self):
        if self.files.all().count() > 0:
            return self.files.all()[0].filename;
        return ''

    @property
    def update_read_cnt(self):
        self.read_cnt = self.read_cnt + 1
        self.save()
        return self.read_cnt


class BoardAttachFile(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="files", verbose_name='Board', blank=True,
                             null=True)

    upload_file = models.FileField(upload_to="%Y/%m/%d", null=True, blank=True, verbose_name='파일')

    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    content_type = models.CharField(max_length=128, null=True, verbose_name='MIME TYPE')

    size = models.IntegerField('파일 크기')

    def __str__(self):

        return self.filename


class Comment(models.Model):

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True) #댓글 작성자
    text = models.TextField()
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE')
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    def __str__(self):
        return self.text

