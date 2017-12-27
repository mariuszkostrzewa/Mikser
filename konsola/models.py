from django.db import models

# Create your models here.
class Pomiar(models.Model):
    ec=models.DecimalField(max_digits=4, decimal_places=3)
    ph=models.DecimalField(max_digits=4, decimal_places=3)
    temp=models.DecimalField(max_digits=5, decimal_places=3)
    pub_date = models.DateTimeField('date published')