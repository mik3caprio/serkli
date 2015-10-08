from django import forms
from choices_member import *


class NameForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)


class FlowForm(forms.Form):
    chromosome = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.Select, required=True)
    age = forms.ChoiceField(choices=AGE_RANGE_CHOICES, widget=forms.Select, required=True)
    ethnicity = forms.ChoiceField(choices=ETHNICITY_CHOICES, label="ethnicity", widget=forms.Select, required=True)
    drink = forms.ChoiceField(choices=DRINK_CHOICES, widget=forms.Select, required=True)
    smoke = forms.ChoiceField(choices=SMOKE_CHOICES, widget=forms.Select, required=True)
    exercise = forms.ChoiceField(choices=EXERCISE_CHOICES, widget=forms.Select, required=True)
    bmi = forms.ChoiceField(choices=BMI_CHOICES, widget=forms.Select, required=True)
    relatives = forms.ChoiceField(choices=RELATIVE_CHOICES, widget=forms.Select, required=True)
    invite = forms.BooleanField(widget=forms.HiddenInput(), required=False)
