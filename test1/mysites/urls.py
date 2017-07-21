"""mysites URL Configuration

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
from mysites import views as myview
from manager import views as manageview
import django.contrib.auth.views as pv2
from subcribers import views as subcribersview
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pandas_graph/', myview.Pandas_Geaph,name='pandas_graph'),
    # url(r'^$', myview.HomeView.as_view(),name='home'),
    url(r'^main/', myview.MainView,name='main'),
    url(r'^$', myview.mainhomeView,name='mainhome'),
    url(r'^login/', pv2.login,name='login'),
    url(r'^logout/',pv2.logout,name='logout'),
    url(r'^accounts/profile/',myview.mainhomeView,name='mainhome'),
    url(r'^CompanyGuide/',manageview.CompanyGuide,name='CompanyGuide'),
    url(r'^usa/',manageview.usa,name='usa'),
    url(r'^newsview/',manageview.newsview,name='newsview'),
    url(r'^plan/',manageview.plans,name='plan1'),
    url(r'^plan2/',manageview.plans2,name='plan2'),
    url(r'^signup/$',subcribersview.subscriber_new,name='signup'),
    url(r'^email/$',manageview.email,name='email'),
    url(r'^viewplan/',manageview.viewplan,name='viewplan'),
]
