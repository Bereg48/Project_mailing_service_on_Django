from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogEntruCreateView, BlogEntruListView, BlogEntruDetailView, BlogEntruUpdateView, \
    BlogEntruDeleteView, toggle_activity

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogEntruCreateView.as_view(), name='create'),
    path('', BlogEntruListView.as_view(), name='list'),
    path('view/<int:pk>', BlogEntruDetailView.as_view(), name='view'),
    path('edit/<int:pk>', BlogEntruUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', BlogEntruDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>', toggle_activity, name='toggle_activity'),

]
