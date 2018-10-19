from django.urls import path, include
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^getBaseData.html$', views.get_base_data, name='get_base_data'),
    url(r'^home.html$', views.home, name='home'),
    url(r'^index.html$', views.index, name='index'),
    url(r'^oamt.html$', views.oamt, name='oamt'),
    url(r'^sendReport.html$', views.sendReport, name='sendReport'),
    url(r'^index.php$', views.home, name='home'),
    url(r'^getMarkers.html$', views.get_markers, name='get_markers'),
    url(r'^getMarkerSum.html$', views.get_markersum, name='get_markersum'),
    url(r'^getOffenses.html$', views.get_offenses, name='get_offenses'),
    url(r'^getOffices.html$', views.get_offices, name='get_offices'),
    url(r'^getMailtext.html$', views.get_mailtext, name='get_mailtext'),
    url(r'^getObstructions.html$', views.get_obstructions, name='get_obstructions'),
    url(r'^upload.html$', views.uploadfile, name='uploadfile'),
    url(r'^createReporter.html$', views.createReporter, name='createreporter'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
]
urlpatterns += staticfiles_urlpatterns()
