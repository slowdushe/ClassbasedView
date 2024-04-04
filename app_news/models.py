from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriyalar Nomi')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        db_table = 'categories'


class News(models.Model):
    news_title = models.CharField(max_length=255, unique=True, verbose_name='Yangilik sarlavhasi')
    news_description = models.CharField(max_length=400, verbose_name='Yangilikning qisqa tavsifi')
    news_image = models.ImageField()
    news_content = models.TextField(verbose_name='Yangilik matni')
    news_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Yangilik kategoriyasi')
    news_pub_date = models.DateTimeField(auto_now_add=True)
    news_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.news_title}, {self.news_category}"

    class Meta:
        verbose_name_plural = 'News'
        verbose_name = 'News'
        db_table = 'news'


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='guruhlar',
        blank=True,
        related_name='custom_users_groups'  # Unikal related_name ni tanlang
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='foydalanuvchi ruxsatlari',
        blank=True,
        related_name='custom_users_permissions'  # Unikal related_name ni tanlang
    )

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
