"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from snippets import views

RT = routers.DefaultRouter()
# RT.register(r'^snippets/$', views.SnippetList.as_view())
# RT.register(r'^api/users/', views.UserList.as_view())

urlpatterns = [
    url(r'^api/', include(RT.urls)),
    url(r'^api/', include('snippets.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
]
