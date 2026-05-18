from django.db import models


class Person(models.Model):
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    passport_num = models.CharField(max_length=20)
    passport_code = models.CharField(max_length=10)
    passport_otd = models.CharField(max_length=255)
    passport_date = models.DateField()
    inn_fiz = models.CharField(max_length=20, blank=True, null=True)
    snils = models.CharField(max_length=20, blank=True, null=True)
    oms = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
