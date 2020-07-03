from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    """Form to allow librarian to renew books"""
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        renewal_date = self.cleaned_data.get('renewal_date')
        
        if renewal_date <datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if renewal_date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks in fuyure'))
        
        return renewal_date
    
