from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'django_ecommerce.views.home', name='home'),
    # url(r'^django_ecommerce/', include('django_ecommerce.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index', name='home'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^contact/', 'contact.views.contact', name='contact'),
)