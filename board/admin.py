from django.contrib import admin

from board.models import Board


# Register your models here.
#
# @admin.register(Board)
# class BoardAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'modify_dt', 'tag_list')
#     list_filter = ('modify_dt',)
#     search_fields = ('title', 'content')
#     prepopulated_fields = {'slug' : ('title',)} # title컬럼의 값으로써 slug 문자열을 만들어내는 명령어
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('tags')
#     # 쿼리셋(post.objects.all())을 받아 관련있는 쿼리셋의 tag를 return
#
#     def tag_list(self, obj):
#         return ', '.join(o.name for o in obj.tags.all())
#     # tags에 있는 모든 아이템에 있어서 o.name을 받아 ,로 구분하여 return
