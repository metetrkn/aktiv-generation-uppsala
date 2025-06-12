from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('', views.mail_us, name='mail_us'),
    path('reply/<int:message_id>/', views.mail_reply, name='mail_reply'),
] 