from django.conf.urls import include, url
from django.contrib import admin
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from rest_framework import urls as drf_urls

from prepyme import api_v1
from prepyme.views import (MyAccountApiView, LoginView, LogoutView, PinlessProcessView, ProceedToPayView)
from rest_framework.authtoken import views
from django.conf import settings

urlpatterns = []

# if settings.DEBUG:
#     urlpatterns = [
#         url(r'(?P<filetype>(service-worker|sw-toolbox))(?P<buildhash>(-\w*)?)\.js$', service_worker_view),
#         url(r'^(?P<filename>(crossdomain\.xml|manifest\.appcache|robots\.txt))$', root_files_view),
#     ]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# current_account = MyAccountApiView.as_view()

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^api/v1/', include(api_v1)),
    url(r'^api/v1/', include(api_v1)),
    url(r'^api/v1/', include(drf_urls)),

    url(r'^api/v1/login/', LoginView.as_view()),
    url(r'^api/v1/logout/', LogoutView.as_view()),
    # url(r'^api/v1/process/pinless', PinlessProcessView.as_view()),
    url(r'^api/v1/proceed/', ProceedToPayView.as_view()),
    # url(r'^api/v1/validators/(?P<number>[0-9]+)/(?P<iso>.+)/(?P<prefix>[0-9]+)/$', phone_val),
    url(r'^backend/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^api/v1/auth-token/', views.obtain_auth_token),
    url(r'^api/v1/accounts/', MyAccountApiView.as_view()),
    # url(r'^api/v1/data', PrepyDocView.as_view()),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)


# from rest_framework.urlpatterns import format_suffix_patterns
# urlpatterns = format_suffix_patterns(urlpatterns)
