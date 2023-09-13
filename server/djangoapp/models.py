from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def __str__(self):
        return f"The car created is {self.name}"    


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN="sedan"
    SUV = "suv"
    WAGON = "wagon"
    CHOICE=[(SEDAN,"Sedan"),(SUV,"SUV"),(WAGON,"WAGON")]
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=200)
    model=models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)        
    bodytype = models.CharField(max_length=200,choices=CHOICE)
    year = models.DateField(default=now)
    def __str__(self):
        return f"{self.model}"



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
