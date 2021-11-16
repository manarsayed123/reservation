from django.urls import path, include
from rest_framework.routers import DefaultRouter

from table.views import TableViewSet
router = DefaultRouter()
router.register('table', TableViewSet, basename='table_crud')
urlpatterns = [
    path('', include(router.urls)),

]