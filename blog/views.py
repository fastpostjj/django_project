from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from blog.models import Blog
from config.settings import EMAIL_HOST_USER


# Create your views here.

class BlogDetailView(generic.DetailView):
    model = Blog
    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        contex_data['title'] = self.get_object()
        contex_data['text'] = self.get_object()
        return contex_data

    # def get_object(self, queryset=None):
    def get(self, request, *args, **kwargs):
        self.object = super().get_object()
        self.object.count_view += 1
        # print("Увеличение счетчика")
        self.object.save()
        context = self.get_context_data(object=self.object)
        if self.object.count_view == 100:

            # Посылаем email, когда счетчик достигнет 100
            subject = f"Вашу статью прочитали {self.object.count_view} раз!"
            message_body = f"Количество просмотров статьи {self.object.title} достигло {self.object.count_view}"
            send_mail(
            subject,
            message_body,
            EMAIL_HOST_USER,
            [EMAIL_HOST_USER],
            fail_silently=False,
            )
        return self.render_to_response(context)

class BlogListView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Наши блог',
        'text': "Наш блог"
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True, is_published=True).order_by("-created_at", "title")
        return queryset

class BlogDraftListView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Черновики статей',
        'text': "Черновики статей"
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True, is_published=False).order_by("-created_at", "title")
        return queryset


class BlogCreateView(generic.CreateView):
    model = Blog
    fields = ('title', 'description', 'preview', 'is_active', 'is_published')
    success_url = reverse_lazy('blog:blogs')


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ('title', 'description', 'preview', 'is_active', 'is_published')
    # success_url = reverse_lazy('blog:blogs')
    def get_success_url(self):
        return reverse('blog:blog', args=[self.object.slug])


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs')


class Toggle_Activity_Blog(View):
    def get(request, *args, slug, **kwargs):
        text = ""
        blogs = get_object_or_404(Blog, slug=slug)
        if blogs.is_active:
            blogs.is_active = False
            subject = "Статья деактивирована"
            message_body = f"Статья {blogs} деактивирована"
        else:
            blogs.is_active = True
            subject = "Статья активирована"
            message_body = f"Статья {blogs} активирована"
        blogs.save()
        send_mail(
            subject,
            message_body,
            EMAIL_HOST_USER ,
            [EMAIL_HOST_USER],
            fail_silently=False,
        )
        return redirect(reverse('blog:blog', args=[blogs.slug]))
