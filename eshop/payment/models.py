from django.db import models
from users.models import User
from orders.models import Order


# Create your models here.

class Payment(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    NEW = 'new'
    IN_PROCESS = 'in process'
    READY = 'ready'
    STATUS_CHOICES = (
        (NEW, "new"),
        (IN_PROCESS, "in process"),
        (READY, "ready"),
    )
    status = models.CharField(max_length=10, default=NEW, choices=STATUS_CHOICES, null=True, blank=False)

    def __str__(self):
        return f'{self.order}'
