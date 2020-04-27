from django import forms

from corona_app.models import CoronaApp, MedicalMap

class MedicalMapForm(forms.ModelForm):
	class Meta:
		model = MedicalMap
		fields = ['age', 'height', 'weight', 'diabetes', 'kidney', 'heart', 'lungs', 'stroke', 'hypertension', 'hiv', 'transplant', 'fever', 'cough', 'breathlessness', 'fatigue', 'joint_pain', 'loss_of_taste_and_smell', 'sore_throat', 'nasal_congestion', 'headache', 'chills', 'nausea_or_vomiting', 'diarrhea', 'conjunctival_congestion', 'symptoms_improvement', 'domestic_flight', 'domestic_train', 'domestic_auto', 'domestic_cab', 'domestic_airport_from', 'domestic_airport_to', 'current_state', 'international_mode', 'country_travelled']
