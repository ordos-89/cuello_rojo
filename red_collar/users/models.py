from django.db import models
from django.contrib.auth.models import AbstractUser


class Raider(AbstractUser):
    """Искатель. Необходимая и достаточная информация об Искателе - его позывной.
    Примечание: для аутентификации будут использоваться поля username и password,
    имеющиеся в классе AbstractUser по умолчанию."""

    call_sign = models.CharField(max_length=42, blank=True)

    def __str__(self):
        return self.call_sign if self.call_sign else self.username
