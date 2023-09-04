from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import BlogEntru


class BlogEntruCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogEntru
    fields = ('title', 'preview', 'content', 'creation_date',)
    permission_required = 'orm.add_product'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogEntruUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogEntru
    permission_required = 'orm.change_product'
    fields = ('title', 'preview', 'content', 'creation_date',)


    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogEntruListView(ListView):
    model = BlogEntru

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     queryset = queryset.filter(publication_attribute=True)
    #
    #     return queryset


class BlogEntruDetailView(DetailView):
    model = BlogEntru

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()

        return self.object


class BlogEntruDeleteView(DeleteView):
    model = BlogEntru
    success_url = reverse_lazy('blog:list')


def toggle_activity(request, pk):
    blog_item = get_object_or_404(BlogEntru, pk=pk)
    if blog_item.publication_attribute:
        blog_item.publication_attribute = False
    else:
        blog_item.publication_attribute = True

    blog_item.save()

    return redirect(reverse('blog:list'))
