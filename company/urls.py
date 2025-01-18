from django.urls import path, include
from rest_framework import routers
from company.views.company_view import CompanyView
from company.views.holiday_view import HolidayView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'company', CompanyView)
router.register(r'holiday', HolidayView)

urlpatterns = [
    path('', include(router.urls)),
]
