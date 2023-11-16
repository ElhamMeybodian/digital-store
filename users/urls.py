from django.urls import path

from .api.views.login import LoginApiView
from .api.views.logout import LogoutView
from .api.views.register import UserCreateView, ActivateAccountView, SendAgainActivateCodeView
from .views import RegisterView, GetTokenView

app_name = "users"

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('get-token/', GetTokenView.as_view()),

    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/activate/<str:username>/', ActivateAccountView.as_view(), name='activate-user'),
    path('api/send-activate-code/<str:username>/', SendAgainActivateCodeView.as_view(), name='send-activate-code'),

    path('api/login/', LoginApiView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

]
