from django.urls import path
from .views import RegisterAPIView, LoginAPIView,UpdateAPIView,UserGetViewAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('update/', UpdateAPIView.as_view()),
    path('user/', UserGetViewAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),


]
