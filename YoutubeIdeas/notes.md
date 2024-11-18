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