Instalacja django

```commandline
pip install django
```

Tworzy strukturę do zarządzania projektem
```
django-admin startproject nazwa_projektu
```

Tworzy strukturę pojedynczej aplikacji
```commandline
python manage.py startapp ideas
```

1 model to jedna tabela w bazie danych w uproszczeniu

Migracja - możemy sobie przewidzieć liste poleceń, które mają się stać z nasza bazą danych, i będą zaaplikowane na tej bazie danych u wszystkich
Należy dodać scieżkę w installed apps w settings.py: "ideas.apps.IdeasConfig",
oraz dodać atrybut max_length w naszym modelu: status = models.CharField(choices=IDEA_STATUS, max_length=30, default="pending")
```commandline
python manage.py makemigrations ideas
```
Następnie wykonujemy migrację:
```commandline
python manage.py migrate
```
Aplikuje wszystkie migracje na naszej bazie danych.

Pózniej np. w dbeaverze dodajemy naszą bazke kopiując absolute path

Póżniej uruchamiamy serwer deweloperski poleceniem
```commandline
python manage.py runserver
```

wypluwa nam adres naszego serwera: http://127.0.0.1:8000/
i do admina dostajemy się dodając sluga http://127.0.0.1:8000/admin

Wchodzimy do naszego folderu aplikacji (youtube) i komenda: python manage.py createsuperuser
tworzymy admina
login: michal
has: mojehaslowiadomojakie

W admin.py, aby zarejestrować nasze modele do panelu admina
```commandline
from django.contrib import admin
from .models import Idea, Vote

# Register your models here.
admin.site.register(Idea)
admin.site.register(Vote)
```

Kolejno zmieniamy rejestrację na postać klasową w admin.py, aby czytelnie manipulować tabelą admina

```commandline

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin): # dziedziczymy po klase z django model.admin
    list_display = ['title', 'status', 'description'] # muszą się zgadzać z zadeklarowanymi polami z models

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'idea','reason'] # zmieni nam nazwy w panelu admina tj. doda tabele z naglowkami id i reason
```

Do wyświetlenia czytelnie nazwy idea, trzeba dodać metodę w models.py
```commandline
# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    youtube_url = models.URLField(null=True, blank=True) #ustawienie na niewymagane pole i po tej zmianie trzeba znowu migracje
    status = models.CharField(choices=IDEA_STATUS, max_length=30, default="pending")

    def __str__(self): # metoda zwroci nam czytelna nazwe obiektu
        return self.title

```

Dodajemy dodatkowe funkcjonalnosci zgodnie z opisem:
```commandline
from django.contrib import admin
from django.utils.html import format_html # importujemy, aby uzyskac tylko link htmlowy
from .models import Idea, Vote

class VoteInline(admin.StackedInline): # pokaze nam voty w zakladce idea
    model = Vote # deklarujemy nazwe modelu, ktory chcemy pokazac


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin): # dziedziczymy po klase z django model.admin
    search_fields = ['title'] # wyszukiwarka search bar
    list_display = ['title', 'status', 'show_youtube_url'] # muszą się zgadzać z zadeklarowanymi polami z models
    list_filter = ['status'] # wlacza liste filtrowania po statusie
    inlines = [VoteInline]

    def show_youtube_url(self, obj):
        if obj.youtube_url is not None:
            return format_html(f'<a href="{obj.youtube_url}" target="_blank">{obj.youtube_url}</a>')
            # target="_blank" uruchomi nam link w nowej karcie
        else:
            return ""

    show_youtube_url.short_description = "Youtube URL" # to nam zmieni nazwe nagłówka na krótszą

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'idea','reason'] # zmieni nam nazwy w panelu admina tj. doda tabele z naglowkami id i reason
    list_filter = ['idea'] # dodajemy filtr wbudowany z django po nagłówki idea
```

Oraz reprezentację nazwy w Vote
```commandline
class Vote(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"id {self.id}" # zwracamy id aby pozbyc sie nazw obiektow
```

REST API

Instalujemy biblioteki django rest api
```commandline
pip install djangorestframework
```

Tworzymy serializer - coś co serializuje nam dane - proces który zamienia nam obiekt na dane np. json
Tworzymy plik serializer.py

```commandline
from models import Vote, Idea
from rest_framework import serializers

class IdeaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: # przyjęcie w django, że zazwyczaj wewnętrzne klasy mają nazwe meta
        model = Idea
        fields = ['id', 'title', 'descirption', 'youtube_url', 'status'] # dodajemy nasze fieldy


class VoteSerializer(serializers.HyperlinkedModelSerializer): # nazwaklasynaszej i serializer przyjmujemy
    class Meta:
        model = Vote
        fields = ['idea', 'reason']


# MVT model - view - template
# view - widok odpowiada za odebranie żadania i kontakt z modelami w celu odebrania itneresujacych
# danych i zwrocenie uzytkownikowi
```

Tworzymy widoki we views.py

```commandline
from .models import Idea, Vote
from rest_framework import viewsets # import widoku z parametryzacja
from .serializer import IdeaSerializer, VoteSerializer # importujemy nasze serializery

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all() # pobeira wszystkie pomysły
    serializer_class = IdeaSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
```

Tworzymy plik urls.py w ideas dla naszych endpointów do API


Dorzucamy rest_framework do installed apps w settings.py
```commandline
INSTALLED_APPS = [
    "rest_framework",
```

Stawianie dockera!!

Budujemy na nowo nasz projekt i przenosimy wszystkie zależności.
Wchodzimy cd youtube
Tworzymy plik requirement.txt, a zależności pobieramy poleceniem
```commandline
pip freeze > requirements.txt
```

Tworzymy plik z intrukcjami dla dockera (dockerfiles)
Dockerfile w katalogu youtube głownym tworzymy
```commandline
FROM python:3 # python wersja 3
WORKDIR /code # wskazujemy folder na którym bedziemy pracować
COPY requirements.txt /code/ # kopiujemy nasz plik do naszego kontenera
RUN pip install -r requirements.txt # instalujemy wszystkie zależności
COPY . /code/ # skopiuj zawartosc calego folderu i wrzuć do folderu code
```

Obrazy możemy pobierac z dockerhuba

Tworzymy plik docker-compose.yml, będzie zawierał informacje o tym jakie będziemy potrzebować usługi
```commandline
version: "3.9"

services:
  db: # pierwsza baza danych
    image: postgres # to ma byc obraz ktory ma byc postgresem
    environment: # uwierzytelnianie bazy
      - POSTGRES_DB=youtube
      - POSTGRES_USER=youtube
      - POSTGRES_PASSWORD=youtube123
    ports:
      - "5432:5432"
  web: # baza odpowiadajaca za strone internetowa
    build: youtube # budujemy nasz docker file
    command: python manage.py runserver 0.0.0.0:8000 # nasluchuj na dowolnym IP na porcie 8000
    volumes:
      - .:/code/ # podpinamy nasz projektowy folder do folderu code aby moc go edytowac na biezaco
    ports:
      - "8000:8000" # prziekierowanie z portu local host na kontenerowy 8000
    depends_on:
      - db # uruchamiamy web dopiero po wstaniu db
```

Uruchamiamy poleceniem
```commandline
docker-compose up
```

Konfigurujemy postgresa w youtube/settings.py

Podmieniamy database, kopiuj wklej ze stronki tam wylistowanej:
I zmieniamy konfiguracje na taka jak ustawilismy w docker-compose; port domyslny

```commandline
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "youtube",
        "USER": "youtube",
        "PASSWORD": "youtube123",
        "HOST": "db",
        "PORT": "5432",
    }
}
```

Pózniej sprawdzamy procesy dockera poleceniem
```commandline
docker ps
```

Bierzemy id naszej webowki tj.
480565.. i poleceniem
```
docker exec -it 480 bash
```

I instalujemy tutaj brakującą bibliotekę:
```commandline
pip install psycopg2
```

I restart dockera
ctrl c i docker-compose up

Dodajemy w requirements.txt:
psycopg2==2.8.6

Pozniej docker-compose build web i docker-compose up

Na dzialajacym kontenerze drugi terminal i robimy znowu:
docker exec -it 420 i robimy migracje python manage.py migrate

I teraz powinna nam działać stronka i możemy zrobić super usera:
```commandline
python manage.py createsuperuser
```
dane:
login: michal
password: michal123

```commandline
#DEV do readme ( co bylo wykonane )
1. Listing available containters:
docker ps
2. To enter container:
docker exec -it {id} bash
3. To rebuild container:
docker-compose build {nazwa}
4. Start projects containers:
docker-compose up
```