from django.contrib import admin
from .models import Read
from .models import Section
from .models import Recipe
from .models import Watering
# Register your models here.
admin.site.register(Read)
admin.site.register(Section)
admin.site.register(Recipe)
admin.site.register(Watering)