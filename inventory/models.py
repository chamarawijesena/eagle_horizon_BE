from django.db import models

class Hardware(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.IntegerField()

    def __str__(self):
        return self.name