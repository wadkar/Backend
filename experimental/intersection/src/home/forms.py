from django import forms

class ContactForm(forms.Form):

    Name = forms.CharField(required=True)
    ContactNo = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea,required=True)


class enquiryform(forms.Form):
	fullname=forms.CharField(label='Full name')
	email = forms.EmailField(label='Email', required=True)
	mobile= forms.CharField(label='Contact Number',required=False)
	message= forms.CharField(label='Message',widget=forms.Textarea(attrs={'rows':'5'}))
	eventname = forms.CharField(widget=forms.HiddenInput)