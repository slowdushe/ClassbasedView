from random import randint

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from app_news.forms import CustomUserForm
from app_news.models import News, Category
from config.settings import  EMAIL_HOST_USER


class AddNewsView(LoginRequiredMixin, CreateView):
    template_name = 'news/add_news.html'
    model = News
    success_url = reverse_lazy('list_news')
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class AddCategoryView(LoginRequiredMixin, CreateView):
    template_name = 'news/add_category.html'
    model = Category
    success_url = reverse_lazy('home')
    fields = '__all__'


class ListNewsView(ListView):
    template_name = 'news/list_news.html'
    model = News
    paginate_by = 1

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            return (
                    News.objects.filter(news_title__icontains=self.request.GET['keyword']) |
                    News.objects.filter(news_description__icontains=self.request.GET['keyword']) |
                    News.objects.filter(news_content__icontains=self.request.GET['keyword']))
        return News.objects.all()


class DetailNewsView(DetailView):
    template_name = 'news/detail_news.html'
    model = News


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'news/edit_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_content', 'news_category']
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().news_author


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    template_name = 'news/delete_news.html'
    model = News
    success_url = reverse_lazy('home')


def register_view(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserForm()
    return render(request, 'registration/register.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {"form": form})


def sendmail(request):
    if request.method == 'POST':
        try:
            send_mail(
                subject=request.POST['subject'],
                message=request.POST['message'],
                from_email=EMAIL_HOST_USER,
                recipient_list=[request.POST['to_mail']]
            )
            return HttpResponse("<h1>Hello ! What's up bro</h1>")
        except Exception as e:
            return HttpResponse(f'<h1>Somthong went wrong</h1><p>{e}</p>', status=500)
    return render(request, 'registration/sendmail.html')
