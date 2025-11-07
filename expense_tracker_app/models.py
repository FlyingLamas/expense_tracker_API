from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Expense(models.Model):
    
    CATEGORY_CHOICES = [("F", "FOOD"), ("T", "TRAVEL"), ("R", "RENT"), ("S", "SHOPPING"), ("O", "OTHERS"),]
    
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    
    title = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.CharField(max_length = 10, choices = CATEGORY_CHOICES, default = "O")
    description = models.TextField(null = True, blank = True)
    expense_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
   
    def __str__(self):
        return self.title


