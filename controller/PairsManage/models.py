from django.db import models

class BinancePair (models.Model):

    class Meta:

<<<<<<< HEAD
        db_table = 'binance_pairs'
=======
        db_table = '"binance_pairs"'
>>>>>>> gitlab/dev_nl
    
    STATUS_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )

    name = models.CharField(max_length=8, primary_key=True)
    get_data = models.CharField(max_length=3, choices=STATUS_CHOICES, default='OFF')
    status = models.CharField(max_length=8, default='absent')
    last_change_by_pid = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name