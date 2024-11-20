from rest_framework import routers # tworzymy routing
from django.urls import include, path
from .views import VoteViewSet, IdeaViewSet # importujemy nasze widoki aby rozpoznawac z ktorego widoku przyszlo zapytanie


router = routers.DefaultRouter()
router.register(r'ideas', IdeaViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) # namespace aby sie nam nie zduplikowaly nazwy urli
]
