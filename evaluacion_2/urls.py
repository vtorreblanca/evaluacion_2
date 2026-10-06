from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/valorar/', views.agregar_valoracion, name='agregar_valoracion'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq, name='faq'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
