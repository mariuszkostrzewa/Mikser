from django.db import models

# Create your models here.
class Read(models.Model):
    ec=models.DecimalField(max_digits=4, decimal_places=3)
    ph=models.DecimalField(max_digits=4, decimal_places=3)
    temp=models.DecimalField(max_digits=5, decimal_places=3)
    pub_date = models.DateTimeField('date published', null=False)
    
    def __str__(self):
        return (self.pub_date.__str__()+' temp: '+self.temp.__str__()+' ec: '+self.ec.__str__()+' ph: '+self.ph.__str__())
    
class Section(models.Model):
    valve=models.IntegerField(unique=True, null=False)
    description=models.CharField(max_length=64)
    
    def __str__(self):
        return (self.description+' to zacisk: '+self.valve.__str__())
    
class Recipe(models.Model):
    acid=models.ForeignKey(Section, on_delete=models.CASCADE, related_name='acidBarrel', null=False)
    fertilizerI=models.ForeignKey(Section, on_delete=models.CASCADE, related_name='fert1', null=False)
    fertilizerII=models.ForeignKey(Section, on_delete=models.CASCADE, related_name='fert2')
    proportion=models.IntegerField()
    ec=models.DecimalField(max_digits=4, decimal_places=3, null=False)
    ph=models.DecimalField(max_digits=4, decimal_places=3, null=False)
    description=models.CharField(max_length=64)
    
    def __str__(self):
        return self.description
    
class Watering(models.Model):
    time=models.TimeField(unique=True)
    duration=models.DurationField(null=False)
    recipe=models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False)
    section=models.ForeignKey(Section, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return (self.section.__str__()+' '+self.time.__str__()+' '+self.duration.__str__())

    