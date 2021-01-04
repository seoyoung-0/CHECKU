from django.contrib import admin
from .models import User,Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display=(
        'title',
        'author'
    )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=(
        'nickname',
        'kakao_id',
        'email',
        'active'
    )