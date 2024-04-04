from django.contrib import admin
from .models import Category, News
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'birth_date')
    search_fields = ('username',)
    ordering = ['username']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(News)
admin.site.register(Category)
