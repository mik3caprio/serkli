from django import forms
from choices_member import *


CIRCLE_MAX_SIZE = 8
CIRCLE_MIN_SIZE = 4


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


class NetworkForm(forms.Form):
    count = CIRCLE_MAX_SIZE
    contact_range_str = ""

    while count != 1:
        contact_range_str = contact_range_str + str(count)
        count = count - 1

    # Reverse the string of numbers
    contact_range_str = contact_range_str[::-1]

    context = {'num_range_str':contact_range_str}

    # A minimum of 3 names and 3 contact fields must be entered


    # Validate all contact fields


    ethnicity = forms.ChoiceField(choices=ETHNICITY_CHOICES, label="ethnicity", widget=forms.Select, required=True)
