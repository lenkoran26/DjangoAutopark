from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name="Имя")
    lastname = models.CharField(max_length=30, verbose_name="Фамилия")
    birthday = models.DateField(verbose_name="Дата рождения")
    age = models.IntegerField(verbose_name="Возраст", editable=False)
    phone = models.CharField(verbose_name="Номер телефона", max_length=20)


    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural="Клиенты"

    def __str__(self):
        return " ".join([self.name, self.lastname])



