from django import forms

class ScrapeForm(forms.Form):
    query = forms.CharField(label='Название', max_length=100, required=True)
    min_salary = forms.IntegerField(label='Минимальная зарплата', required=False)
    skills = forms.CharField(label='Навыки', max_length=200, required=False)
