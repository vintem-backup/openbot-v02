from django.db import models

class BinancePair (models.Model):

    class Meta:

        db_table = 'binance_pairs'
    
    STATUS_CHOICES=(
        ('ON','on'),
        ('OFF','off'),
        )

    name = models.CharField(max_length=8, primary_key=True)
    get_data = models.CharField(max_length=3, choices=STATUS_CHOICES, default='OFF')
    status = models.CharField(max_length=8, default='absent')
    last_stored_candle = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_change_by_PID = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name