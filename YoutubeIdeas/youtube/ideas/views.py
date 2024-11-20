from .models import Idea, Vote
from rest_framework import viewsets # import widoku z parametryzacja
from .serializer import IdeaSerializer, VoteSerializer # importujemy nasze serializery

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all() # pobeira wszystkie pomysły
    serializer_class = IdeaSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
