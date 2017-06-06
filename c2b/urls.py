from django.conf.urls import url

from . import views
from views import MpesaValidation

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^validation/$', views.validation, name='validation'),
    url(r'^validate/$',
        MpesaValidation.as_view(),
        name="validate"),
]
