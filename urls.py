from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home.html', include('wegeheld.urls')),
    url(r'^admin/', admin.site.urls),
]
