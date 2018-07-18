from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'call_record_details.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^record/', include('call_record.urls')),
    url(r'^telephone_bill/', include('telephone_bill.urls'))
]
