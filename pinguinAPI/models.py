from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Stock(models.Model):
    """
    Eigene Stock-Klasse (Model).
    Enthält den Bestand und kann später erweitert werden (Reservierungen, History, etc.).
    """
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"Stock({self.amount})"

class Product(models.Model):
    product_id = models.IntegerField(blank=True, null=True, unique=True)
    product_name = models.CharField(max_length=25,blank=False,null=False)
    short_description = models.CharField(max_length=200,blank=False,null=False)
    product_description = models.CharField(max_length=200,blank=False,null=False)
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE, related_name="product",blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.product_id} - {self.product_name}"


