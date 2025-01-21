from django.urls import path, include
from rest_framework import routers
from company.views.company_view import CompanyView
from company.views.holiday_view import HolidayView
from company.views.payment_view import PaymentView
from company.views.billing_view import BillingView
from company.views.shift_time_view import ShiftTimeView
from company.views.address_view import AddressView

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'company', CompanyView)
router.register(r'holiday', HolidayView)
router.register(r'payment', PaymentView)
router.register(r'billing', BillingView)
router.register(r'shift', ShiftTimeView)
router.register(r'address', AddressView)

urlpatterns = [
    path('', include(router.urls)),
]
