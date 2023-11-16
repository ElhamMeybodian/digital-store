from django.urls import path

from subscriptions.views import PackageView, SubscriptionView


urlpatterns = [
    path('package/', PackageView.as_view()),
    path('subscriptions/', SubscriptionView.as_view()),
]
