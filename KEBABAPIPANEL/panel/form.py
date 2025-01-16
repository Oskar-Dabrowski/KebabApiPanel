from django import forms
from api.models import OpeningHour
import json

class OpeningHourForm(forms.ModelForm):
    open_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Open Time")
    close_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label="Close Time")

    def save(self, commit=True):
        # Set default values if open_time or close_time are empty
        if not self.cleaned_data['open_time']:
            self.cleaned_data['open_time'] = "00:00"
        if not self.cleaned_data['close_time']:
            self.cleaned_data['close_time'] = "00:00"

        self.instance.hours = json.dumps({
            "open": self.cleaned_data['open_time'].strftime('%H:%M'),
            "close": self.cleaned_data['close_time'].strftime('%H:%M')
        })
        return super().save(commit)

    class Meta:
        model = OpeningHour
        fields = ['kebab', 'day_of_week', 'open_time', 'close_time']
