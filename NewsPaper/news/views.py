from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-created_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'separate_news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'separate_news'

class PostSearch(ListView):
    model = Post
    ordering = '-created_date'
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# Представление для создания новости
class NewsCreate(CreateView):
    # Разработанная форма
    form_class = PostForm
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'news_create.html'