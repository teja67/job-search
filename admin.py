from django.contrib import admin
from .models import City
from .models import Location

# Register your models here.

admin.site.register(City)
admin.site.register(Location)