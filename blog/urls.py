"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from blog_app import views
# from django.views.generic import RedirectView # RedirectView.as_view(url='/m_10000/')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(login|reg|logout|change|edit|artdel|web|linux|python|other)*$', views.all_articles, name='all'),
    url(r'^m_([0-9]+)/(login|reg|logout|change|edit|artdel)*$', views.index, name='index'),
    url(r'^m_([0-9]+)/article/(\d*)/(login|reg|logout|change|comment|delcom|edit|artdel)*$', views.article),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
