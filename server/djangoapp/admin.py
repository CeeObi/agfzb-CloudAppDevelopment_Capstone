from django.contrib import admin
from .models import CarMake, CarModel



# Register your models here.
admin.site.register(CarModel)


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 0

# CarModelAdmin class
# class CarModelAdmin(admin.ModelAdmin):
#     fields = []
    

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines=[CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
