from django.db import models

IDEA_STATUS = (
    ('pending', 'Waiting for review'),
    ('accepted', 'Accepted'),
    ('done', 'Done'),
    ('rejected', 'Rejected'),
)

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    youtube_url = models.URLField(null=True, blank=True) #ustawienie na niewymagane pole i po tej zmianie trzeba znowu migracje
    status = models.CharField(choices=IDEA_STATUS, max_length=30, default="pending")

    def __str__(self): # metoda zwroci nam czytelna nazwe obiektu
        return self.title

class Vote(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return f"id {self.id}" # zwracamy id aby pozbyc sie nazw obiektow
