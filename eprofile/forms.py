import datetime
from django import forms

from eprofile.models import Profile, Education, Experience


MONTHS = [
    ('0', 'Month'),
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]


def get_year_choices(year_from=True):
    year_choices = [('0', 'Year'),]
    start_year = datetime.date.today().year-61
    if year_from:
        for i in range(datetime.date.today().year, start_year, -1):
            year_choices.append((i, i))
    else:
        for i in range(datetime.date.today().year+10, start_year, -1):
            year_choices.append((i, i))

    return year_choices

class ImageUploadForm(forms.Form):
    img_file = forms.ImageField(
        label='Select an image'
    )


class ProfileCardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['card_name', 'card_title', 'card_department', 'card_employer',
                  'card_email', 'card_address1', 'card_address2', 'card_phone', 'card_office']
        labels = {
            'card_name': 'Full name',
            'card_title': 'Current position',
            'card_department': 'Department',
            'card_employer': 'Institution',
            'card_address1': 'Street',
            'card_address2': 'City, ST Zip',
            'card_email': 'Email',
            'card_phone': 'Phone',
            'card_office': 'Office',
        }

        widgets = {
            """'card_name': forms.CharField(required=True, help_text='Full name with salution', widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_title': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_department': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_employer': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_address1': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_address2': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_email': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_phone': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            'card_office': forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})),
            """
        }

    def __init__(self, *args, **kwargs):
        super(ProfileCardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['card_name'].required = True


class ProfileSummaryForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['summary']
        labels ={
            'summary': 'Update Summary',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileSummaryForm, self).__init__(*args, **kwargs)
        self.fields['summary'].required = False
        self.fields['summary'].widget.attrs['class'] = 'form-control'


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'location', 'month_from', 'year_from', 'current', 'month_to',  'year_to', 'graduated', 'degree',
                  'major_field', 'concentrations', 'gpa', 'activities', 'societies', 'description']
        labels= {
            'school': 'College/School *',
            'location': 'Town/City, State',
            'gpa': 'GPA',
            'month_from': 'Month',
            'month_to': 'Month',
            'year_from': 'Year',
            'year_to': 'Year',
        }

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['month_from'] = forms.ChoiceField(choices=MONTHS)
        self.fields['month_to'] = forms.ChoiceField(choices=MONTHS)
        self.fields['year_from'] = forms.ChoiceField(choices=get_year_choices())
        self.fields['year_to'] = forms.ChoiceField(choices=get_year_choices(False))
        self.fields['activities'].widget.attrs['rows'] = 3
        self.fields['societies'].widget.attrs['rows'] = 3
        self.fields['description'].widget.attrs['rows'] = 5


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'location', 'month_from', 'year_from', 'month_to',
                  'year_to', 'title', 'current', 'description']
        labels= {
            'company': 'Company *',
            'location': 'Town/City, State',
            'month_from': 'Month',
            'month_to': 'Month',
            'year_from': 'Year',
            'year_to': 'Year',
            'title': 'Title *',
            'current': 'I currently work here',
        }

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['month_from'] = forms.ChoiceField(choices=MONTHS)
        self.fields['month_to'] = forms.ChoiceField(choices=MONTHS)
        self.fields['year_from'] = forms.ChoiceField(choices=get_year_choices())
        self.fields['year_to'] = forms.ChoiceField(choices=get_year_choices(False))
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['current'].widget.attrs['class'] = ''
