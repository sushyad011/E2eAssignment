from rest_framework import serializers
from .models import Bed, Patient

class BedStatusSerializers(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Bed
        fields = ['status','type','patient']

    def get_patient(self, obj):
        if obj.status == 'full':
            return obj.patient_set.get(active=True).name
        return None

class GetPatientsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['id','name']

class GetBedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['bed_id','type','status']