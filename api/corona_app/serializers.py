from rest_framework import serializers
from corona_app.models import CoronaApp, MedicalMap


class CoronaAppSerializer(serializers.Serializer):

    timeslot = serializers.CharField(max_length=100, default='00.00.01.01.2020')
    uuid = serializers.CharField(max_length=100, default='a')
    degree = serializers.IntegerField(default=-1)
    
    latitude= serializers.FloatField(default=0)
    longitude= serializers.FloatField(default=0)
    
    #required=True, 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return CoronaApp.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.timeslot = validated_data.get('name', instance.timeslot)
    #     instance.uuid = validated_data.get('name', instance.uuid)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.latitude = validated_data.get('latitude', instance.latitude)
    #     instance.longitude = validated_data.get('longitude', instance.longitude)
        
    #     instance.save()
    #     return instance


class MedicalMapSerializer(serializers.Serializer):
    med_uuid = serializers.CharField(max_length=1000, default='a')
    age = serializers.IntegerField(default=0)

    # GENDER, AGE, HEIGHT, WEIGHT
    # self_else = np.random.randint(0,2)
    # gender = np.random.randint(0,2)
    #gender = np.where(gender==0, -1, gender)
    height = serializers.IntegerField(default=0)
    weight = serializers.IntegerField(default=0)


    #Prev Conditions
    #Diabetes
    diabetes = serializers.BooleanField(default=False)

    #Kidney
    kidney = serializers.BooleanField(default=False)
    #Heart
    heart = serializers.BooleanField(default=False)
    #Lungs
    lungs = serializers.BooleanField(default=False)
    #Stroke
    stroke = serializers.BooleanField(default=False)
    #Hypertension
    hypertension =  serializers.BooleanField(default=False)

    #Immunocompromised
    #HIV
    hiv = serializers.BooleanField(default=False)
    #Transplant
    transplant = serializers.BooleanField(default=False)


    #Symptoms

    fever = serializers.IntegerField(default=0)
    cough = serializers.IntegerField(default=0)

    #Shortness of breadth
    breathlessness  = serializers.BooleanField(default=False)

    #Fatigue
    fatigue = serializers.BooleanField(default=False)

    #Joint/Muscle pain
    joint_pain = serializers.BooleanField(default=False)

    #Loss of taste/smell          #Rare Case
    loss_of_taste_and_smell = serializers.BooleanField(default=False)

    # #Other Symptoms
    sore_throat = serializers.BooleanField(default=False)
    nasal_congestion = serializers.BooleanField(default=False)
    headache = serializers.BooleanField(default=False)
    chills = serializers.BooleanField(default=False)
    nausea_or_vomiting = serializers.BooleanField(default=False)
    diarrhea = serializers.BooleanField(default=False)
    conjunctival_congestion = serializers.BooleanField(default=False)


    symptoms_improvement = serializers.IntegerField(default=0)




    ####### TRAVEL DATA

    domestic_flight = serializers.BooleanField(default=False)
    domestic_train = serializers.BooleanField(default=False)
    domestic_auto = serializers.BooleanField(default=False)
    domestic_cab = serializers.BooleanField(default=False)

    domestic_airport_from = serializers.CharField(max_length=1000, default=' ')
    domestic_airport_to = serializers.CharField(max_length=1000, default=' ')
    current_state = serializers.CharField(max_length=1000, default=' ')


    international_mode = serializers.BooleanField(default=False)
    country_travelled = serializers.CharField(max_length=1000, default=' ')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return MedicalMap.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.domestic_flight = validated_data.get('domestic_flight', instance.domestic_flight)
        instance.domestic_train = validated_data.get('domestic_train', instance.domestic_train)
        instance.domestic_auto = validated_data.get('domestic_auto', instance.domestic_auto)
        instance.domestic_cab = validated_data.get('domestic_flight', instance.domestic_cab)

        instance.domestic_airport_from = validated_data.get('domestic_airport_from', instance.domestic_airport_from)
        instance.domestic_airport_to = validated_data.get('domestic_airport_to', instance.domestic_airport_to)
        instance.current_state = validated_data.get('current_state', instance.current_state)
        
        instance.international_mode = validated_data.get('international_mode', instance.international_mode)
        instance.country_travelled = validated_data.get('country_travelled', instance.country_travelled)
        
        instance.save()
        return instance


