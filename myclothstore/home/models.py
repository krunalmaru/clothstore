from django.db import models
import uuid
# Create your models here.
class Basemodel(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(Basemodel):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class SubCategory(Basemodel):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name