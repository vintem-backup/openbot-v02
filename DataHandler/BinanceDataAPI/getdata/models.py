from django.db import models

class Pair(models.Model):
    STATE_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )
    pair_name = models.CharField(max_length=8, primary_key=True)
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default='OFF')

    def __str__(self):
        return self.pair_name
