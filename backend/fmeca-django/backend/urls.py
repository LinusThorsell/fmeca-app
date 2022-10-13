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
router.register(r'projects', ProjectViewSet, basename="project")
router.register(r'nodes', NodeViewSet, basename="node")
router.register(r'nodes-fc', NodeFCViewSet, basename="node-fc")
router.register(r'nodes-mc', NodeMCViewSet, basename="node-mc")
router.register(r'proccessors', CPUViewSet, basename="cpu")
router.register(r'partitions', PartitionViewSet, basename="parition")
router.register(r'applications', ApplicationViewSet, basename="application")
# router.register(r'nodes-failure', NodeFailureViewSet, basename="node-failure")
# router.register(r'partitions-failure', PartitionFailureViewSet, basename="partition-failure")
# router.register(r'material-groups', MaterialGroupViewSet, basename="materal-group")
urlpatterns = router.urls

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('/', include('router.urls'))
#     # path('api/', include('api.urls'))
# ]
