from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^validation/$', views.validation, name='validation'),
    url(r'^payment_mock/$', views.payment_request_mock_url, name='payment_mock'),
    url(r'^payment_mock2/$', views.payment_response_mock_url, name='payment_mock2'),

]
