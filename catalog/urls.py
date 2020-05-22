from django.conf.urls import url
from catalog.views import IndexView
urlpatterns = [
    url('', IndexView.as_view(), name='index')
]
