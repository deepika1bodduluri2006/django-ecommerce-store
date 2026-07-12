from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('Mobiles', 'Mobiles'),
        ('Laptops', 'Laptops'),
        ('Accessories', 'Accessories'),
    ]

    name = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Mobiles'
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name