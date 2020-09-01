from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify

from tinymce.models import HTMLField
from country.models import Country
# Create your models here.

class City(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one work for title alias')
    card_content = HTMLField('CONTENT', null=True)
    main_content = HTMLField('CONTENT', null=True)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE')
    tags = TaggableManager(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)
    country_index = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='COUNTRY_INDEX', blank=True, null=True)


    class Meta: # Content에 대해서 추가정보를 관리하는 정보를 메타정보라고 함
        verbose_name = 'city' # 단수
        verbose_name_plural = 'cities' # 복수
        db_table = 'city' # 테이블명 재정의
        ordering = ('-modify_dt',) # orderby 절, -이면 내림차순순 <- 저건 튜플 (,) 가 있긴 때문에

    def __str__(self):
        return self.title

    def get_absolute_url(self): # 현재 데이터의 절대 경로 추출
        return reverse('city:detail', args=(self.slug,))

    def get_previous(self): # 이젠 데이터 추출
        return self.get_previous_by_modify_dt()

    def get_next(self): # 다음 데이터 추출
        return self.get_next_by_modify_dt()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def first_image(self):
        if self.files.all().count() > 0:
            return self.files.all()[0].filename;
        return ''

class CityAttachFile(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="files", verbose_name='City', blank=True, null=True)

    upload_file = models.FileField(upload_to="%Y/%m/%d", null=True, blank=True, verbose_name='파일')

    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    content_type = models.CharField(max_length=128, null=True, verbose_name='MIME TYPE')

    size = models.IntegerField('파일 크기')

    class Meta: # Content에 대해서 추가정보를 관리하는 정보를 메타정보라고 함

        db_table = 'cityattachfile' # 테이블명 재정의

    def __str__(self):
        return self.filename

