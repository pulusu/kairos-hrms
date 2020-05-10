from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
# Create your models here.


class Sliders(models.Model):
    img = models.FileField(upload_to='sliders/')
    published = models.BooleanField(default=False)


CATEGORY_CHOICES = (
    ('W', 'Watches'),
    ('C', 'Cameras'),
    ('M', 'Mobiles'),
    ('TV', "Tv's"),
    ('L', "Laptops")
)


LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(unique=True, blank=True, null=True)
    # stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50, blank=True, null=True)
    description_long = models.TextField()
    img = models.FileField(upload_to='items/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        return reverse('details', kwargs={'slug': self.slug, 'pk': self.id, })

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="product_re")
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def TotalPrice(self):
        price_total = self.quantity * self.product.discount_price
        return price_total


class Transaction(models.Model):
    made_by = models.ForeignKey(
        User, related_name='transactions', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)
