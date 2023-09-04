from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import ClientListView, MessageListView, MailingListView, MailingCardListView, MessageCreateView, \
    ClientCreateView, ClientUpdateView, MailingCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(ClientListView.as_view()), name='client'),
    path('message/', cache_page(60)(MessageListView.as_view()), name='message'),
    path('mailing/', cache_page(60)(MailingListView.as_view()), name='mailing'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('<int:pk>/main/mailing_card/', cache_page(10)(MailingCardListView.as_view()), name='mailing_card'),
    path('<int:pk>/main/client_card/', cache_page(10)(ClientListView.as_view()), name='client_card'),
    path('<int:pk>/main/client_update/', cache_page(10)(ClientUpdateView.as_view()), name='client_update'),

]
