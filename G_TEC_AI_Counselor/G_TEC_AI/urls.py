from django.urls import path
from .views import chat_view, home,about,faq, register_view, login_view, logout_view


urlpatterns = [
   path('counselor/', chat_view, name='chat'),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
# ]
]