from django.urls import path,include
from .views import LandingPageView,AboutPageView,HelpPageView,PortalPageView,RegistrationPageView

urlpatterns = [
   path('', LandingPageView.as_view(),name = 'home'),
   path('about/', AboutPageView.as_view(),name = 'about'),
   path('help/', HelpPageView.as_view(),name = 'help'),
   path('portalpage/', PortalPageView.as_view(),name = 'portalpage'),
   path('registeration/', RegistrationPageView.as_view(),name = 'registeration'),
]
