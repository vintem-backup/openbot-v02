from django.forms import ModelForm
from .models import Pair

class PairForm(ModelForm):
    class Meta:
        model = Pair
        fields = '__all__'