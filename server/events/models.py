import uuid
from django.db import models

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class User(Base):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    # password

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name}"

class Event(Base):
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    creator = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, blank=True)
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"Evento criado por {self.creator.name} com a descrição '{self.description}' para o período {self.start} - {self.end}."
