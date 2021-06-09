from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
STATE_CHOICE = (
    ('Andaman & Nicobar ISlands' , 'Andaman & Nicobar Island'),
    ('Andhra Pradesh' , 'Andra Pradesh'),
    ('Arunachal Pradesh' , 'Arunachal Pradesh'),
    ('Assam' , 'Assam'),
    ('Bihar' , 'Bihar'),
    ('Chandisgrah' , 'Chandigrah'),
    ('Chattisgrah','Chattisgrah'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and diu' , 'Daman and diu'),
    ('Delhi' , 'Delhi'),
    ('Goa' , 'Goa'),
    ('Gujarat' , 'Gujarat'),
    ('Haryana' , 'Haryana'),
    ('Himachal Pradesh' , 'Himachal Pradesh'),
    ('Jammu & Kashmir' , 'Jammu & Kashmir'),
    ('Karnataka' , 'Karnataka'),
    ('Kerala' , 'Kerala'),
    ('Lakshadweep' , 'Lakshadweep'),
    ('Madya Pradesh' , 'Madya Pradesh'),
    ('Maharastra' , 'Maharastra'),
    ('Manipur' , 'Manipur'),
    ('Meghalaya' , 'Meghalaya'),
    ('Mizoram' , 'Mizoram'),
    ('Nagaland' , 'Nagaland'),
    ('Odisha' , 'Odisha'),
    ('Punducherry' , 'Punducherry'),
    ('Punjab' , 'Punjab'),
    ('Rajasthan' , 'Rajasthan'),
    ('Sikkim' , 'Sikkim'),
    ('Tamil Nadu' , 'Tamil Nadu'),
    ('Telangana' , 'Telangana'),
    ('Tripura' , 'Tripura'),
    ('Uttarakhand' , 'UttaraKhand'),
    ('Uttar Pradesh' , 'Uttar Pradesh'),
    ('West Bengal' , 'West Bengal'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE,max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICE = (
    ('L' , 'Laptop'),
    ('M' , 'Mobile'),
    ('TW' , 'Top Wear'),
    ('BW' , 'Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORY_CHOICE,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICE = (
    ('Accepted' , 'Accepted'),
    ('Packed' , 'Packed'),
    ('On The Way' , 'On The Way'),
    ('Delivered' , 'Delivered'),
    ('Cancel' ,'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=50, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


