from django import forms
from . models import Aquarium, FreshWaterParameterLogEntry
from core.widgets import ShoelaceInput, ShoelaceTextArea, ShoelaceSelect
from . import choices

class AquariumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = ShoelaceInput(attrs={'placeholder': 'Name', 'label': 'Name', 'required': True, 'clearable': True, 'maxlength': '35'})
        self.fields['description'].widget = ShoelaceTextArea(attrs={'placeholder': 'Description', 'label': 'Description', 'maxlength': '250'})

    class Meta:
        model = Aquarium
        fields = ['name', 'description']


class FreshWaterParamaterLogEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].widget = ShoelaceTextArea(attrs={'placeholder': 'Notes', 'label': 'Notes', 'maxlength': '250'})

    ph = forms.ChoiceField(choices=choices.PHChoices.choices, initial=choices.PHChoices.NA, widget=ShoelaceSelect(attrs={'label': 'pH'}))
    high_range_ph = forms.ChoiceField(choices=choices.HighRangePHChoices.choices, initial=choices.HighRangePHChoices.NA, widget=ShoelaceSelect(attrs={'label': 'High Range pH'}))
    ammonia = forms.ChoiceField(choices=choices.AmmoniaChoices.choices, initial=choices.AmmoniaChoices.NA, widget=ShoelaceSelect(attrs={'label': 'Ammonia'}))
    nitrite = forms.ChoiceField(choices=choices.NitriteChoices.choices, initial=choices.NitriteChoices.NA, widget=ShoelaceSelect(attrs={'label': 'Nitrite'}))
    nitrate = forms.ChoiceField(choices=choices.NitrateChoices.choices, initial=choices.NitrateChoices.NA, widget=ShoelaceSelect(attrs={'label': 'Nitrate'}))
    
    class Meta:
        model = FreshWaterParameterLogEntry
        fields = ['ph', 'high_range_ph', 'ammonia', 'nitrite', 'nitrate', 'notes']