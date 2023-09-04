from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from main.form import MailingForm, MessageForm, ClientForm
from main.models import Client, Mailing, Message
from main.services import get_cached_subject_for_category


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subject_list'] = get_cached_subject_for_category()
        return context_data


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subject_list'] = get_cached_subject_for_category()
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['subject_list'] = get_cached_subject_for_category()
        return context_data


# class ProductCategoryListView(LoginRequiredMixin, ListView):
#     model = Product
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(category=self.kwargs.get('pk'),
#                                    owner=self.request.user)
#         return queryset
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         products_item = Category.objects.get(pk=self.kwargs.get('pk'))
#         context_data['title'] = f'Продукты из выбранной категории {products_item.name}'
#         return context_data


class MailingCardListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'main/blogentry_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()
        return self.object


class ClientCardListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'main/blogentry_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()
        return self.object


class MailingCreateView(CreateView):
    model = Mailing
    permission_required = 'main.add_mailing'
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing')


class MessageCreateView(CreateView):
    model = Message
    permission_required = 'main.add_message'
    form_class = MessageForm
    success_url = reverse_lazy('main:message')


class ClientCreateView(CreateView):
    model = Client
    permission_required = 'main.add_client'
    form_class = ClientForm
    success_url = reverse_lazy('main:client')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'main.change_message'
    success_url = reverse_lazy('main:message')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    permission_required = 'main.change_mailing'
    success_url = reverse_lazy('main:mailing')


class ClientUpdateView(UpdateView):
    model = Client
    permission_required = 'main.change_client'
    form_class = ClientForm
    success_url = reverse_lazy('main:client_card')

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.owner != self.request.user:
    #         raise Http404
    #
    #     return self.object
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     VersionFormset = inlineformset_factory(Product, Version, fields=['name_version', 'name_current_version', ],
    #                                            extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = VersionFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #
    #     return super().form_valid(form)

# def toggle_activity(request, pk):
#     product_item = get_object_or_404(Message, pk=pk)
#     if product_item.name_current_version:
#         product_item.name_current_version = False
#     else:
#         product_item.name_current_version = True
#
#     product_item.save()
#
#     return redirect(reverse('main:product'))
