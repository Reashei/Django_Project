from .models import Vote, Idea
from rest_framework import serializers

class IdeaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: # przyjęcie w django, że zazwyczaj wewnętrzne klasy mają nazwe meta
        model = Idea
        fields = ['id', 'title', 'description', 'youtube_url', 'status'] # dodajemy nasze fieldy


class VoteSerializer(serializers.HyperlinkedModelSerializer): # nazwaklasynaszej i serializer przyjmujemy
    class Meta:
        model = Vote
        fields = ['idea', 'reason']


# MVT model - view - template
# view - widok odpowiada za odebranie żadania i kontakt z modelami w celu odebrania itneresujacych
# danych i zwrocenie uzytkownikowi