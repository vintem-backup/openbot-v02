from django.db import models

class Pair(models.Model):
    STATUS_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )
    HISTORICAL_CHOICES=(
        ('absent','absent'),
        ('building','building'),
        ('full','full'),
        )
    pair_name = models.CharField(max_length=8, primary_key=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='OFF')
    historical = models.CharField(max_length=8, choices=HISTORICAL_CHOICES, default='absent')
    def __str__(self):
        return self.pair_name
