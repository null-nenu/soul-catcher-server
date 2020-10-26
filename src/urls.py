"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from src.api.wechat import views as wechat_view
from src.api.scale import views as evaluation_view

# router of Django REST Framework
router = routers.DefaultRouter()
router.register(r'wechat', wechat_view.WechatViewSet, basename="wechat")
router.register(r'evaluation', evaluation_view.EvaluationViewSet)
router.register(r'evaluation_rate', evaluation_view.EvaluationRateViewSet)
router.register(r'question', evaluation_view.QuestionViewSet)
router.register(r'option', evaluation_view.OptionViewSet)
router.register(r'evaluation_record', evaluation_view.EvaluationRecordViewSet)
router.register(r'evaluation_detail', evaluation_view.EvaluationDetailViewSet)
router.register(r'story', evaluation_view.StoryViewSet)


urlpatterns = [
    path('', include(router.urls)),     # add Django REST Framework's URL to Django
    path('admin/', admin.site.urls),
]

