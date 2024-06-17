from apps.authenticatie.managers import GebruikerManager
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.forms.models import model_to_dict
from django.utils.html import mark_safe


class Gebruiker(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    telefoonnummer = models.CharField(max_length=17, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = GebruikerManager()

    def __str__(self):
        if self.first_name:
            return f"{self.first_name}{' ' if self.last_name else ''}{self.last_name}"
        return self.email

    def rechten_verbose(self):
        return mark_safe(
            f"rechten: <strong>{self.groups.all().first().name if self.groups.all() else '- geen rechten - '}</strong>"
        )

    @property
    def rechtengroep(self):
        return mark_safe(
            f"{self.groups.all().first().name if self.groups.all() else ''}"
        )

    def serialized_instance(self):
        if not self.is_authenticated:
            return None
        dict_instance = model_to_dict(
            self, fields=["email", "first_name", "last_name", "telefoonnummer"]
        )
        dict_instance.update(
            {
                "naam": self.__str__(),
                "rechten": (
                    self.groups.all().first().name if self.groups.all() else None
                ),
            }
        )

        return dict_instance
