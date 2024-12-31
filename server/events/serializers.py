from .models import Event

from rest_framework import serializers

from datetime import datetime, timedelta

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
    
    def validate(self, data):
        instance = self.instance

        current_date = datetime.now() - timedelta(hours=3)

        start_date = data['start']
        end_date = data['end']

        if instance:
            dateDoesNotChangeAtEdition = instance.start == start_date and instance.end == end_date

            if dateDoesNotChangeAtEdition:
                return data
        
        if start_date.timestamp() < current_date.timestamp():
            raise serializers.ValidationError({"star_period": "O período inicial deve ser posterior ou igual ao período atual."})
        elif start_date >= end_date:
            raise serializers.ValidationError({"end_period": "O período final deve ser posterior ao período inicial."})
            

        return data
    
