
from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'leads', LeadsViewSet)
router.register(r'services', ServicesProvidedViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='homepage'),
    path('contact/', ContactPage.as_view(), name='contactpage'),
    path('about/', AboutPage.as_view(), name='aboutpage'),
    path('api/', include(router.urls)),

]