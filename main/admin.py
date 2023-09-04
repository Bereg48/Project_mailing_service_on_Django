from django.contrib import admin

# Register your models here.
from django.contrib import admin

from main.models import Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'time_mailing', 'mailing_status', 'client',)
    list_filter = ('client',)
    search_fields = ('client', 'frequency',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_letter', 'body_letter', 'mailing',)
    list_filter = ('mailing',)

