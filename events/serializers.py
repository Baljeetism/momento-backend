from rest_framework import serializers
from .models import  Events



class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')
    class Meta:
        model = Events
        fields = '__all__'




# from rest_framework import serializers
# from .models import  Eventsz



# class EventSerializer(serializers.ModelSerializer):
#     created_by = serializers.ReadOnlyField(source='created_by.email')
#     class Meta:
#         model = Eventsz
#         fields = '__all__'


