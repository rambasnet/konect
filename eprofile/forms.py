from django import forms

from eprofile.models import Profile, Education


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
        fields = ['school', 'address', 'month_from', 'month_to',  'year_from', 'year_to', 'graduated', 'degree',
                  'major_field', 'conentrations', 'gpa', 'activities', 'societies', 'description']
        labels= {
            'address': 'Town/City, State',
        }

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
