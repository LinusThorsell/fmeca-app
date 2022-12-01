# """backend URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from api.views import *
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'post-projects', ProjectPostViewSet)
router.register(r'nodes', NodeViewSet)
router.register(r'proccessors', CPUViewSet)
router.register(r'partitions', PartitionViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'application-instances', ApplicationInstanceViewSet)
router.register(r'connections', ConnectionViewSet)
router.register(r'threads', ThreadViewSet)
router.register(r'domain-borders', DomainBorderViewSet)
router.register(r'comments', CommentsViewSet)
urlpatterns = router.urls