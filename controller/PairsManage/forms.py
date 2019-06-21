from django.forms import ModelForm
from .models import BinancePair

class PairForm(ModelForm):
    class Meta:
        model = BinancePair
        fields = '__all__'