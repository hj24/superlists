"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from lists import views as list_views
from lists import urls as list_urls
from accounts import views as accounts_views
from accounts import urls as accounts_urls


# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
"""
url(regex, view, kwargs=None, name=None) 
This function is an alias to django.urls.re_path(). 
It’s likely to be deprecated in a future release.
"""
urlpatterns = [
	url(r'^$', list_views.home_page, name='home'),	#  path 不用正则表达式
	# path('lists/new', views.new_list, name='new_list'),
	# url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
	# url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item')
	url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(accounts_urls)),
]
