from django.urls import path

from .views import (
    AddNewsView,
    AddCategoryView,
    ListNewsView,
    DetailNewsView,
    UpdateNewsView,
    DeleteNewsView,
    register_view,
    logout_view,
    login_view,
    sendmail
)

urlpatterns = [
    path('add/', AddNewsView.as_view(), name='add_news'),
    path('<int:pk>/', DetailNewsView.as_view(), name='detail_news'),
    path('add-cat/', AddCategoryView.as_view(), name='add_categories'),
    path('', ListNewsView.as_view(), name='list_news'),
    path('delete/<int:pk>/', DeleteNewsView.as_view(), name='delete_news'),
    path('edit/<int:pk>/', UpdateNewsView.as_view(), name='edit_news'),
    # registration
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('send-mail/', sendmail, name='send_mail'),
]
