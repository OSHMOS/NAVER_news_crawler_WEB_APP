from .models import Query
from django import forms


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = '__all__'
