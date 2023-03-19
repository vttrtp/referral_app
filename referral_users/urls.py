from django.urls import path
from .views import ReferralUserDetail
urlpatterns = [
    path('referral-users/<str:id>/', ReferralUserDetail.as_view()),
]
