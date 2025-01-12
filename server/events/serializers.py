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
        current_date = current_date.timestamp()

        start_date = data['start']
        end_date = data['end']

        if instance:
            dateDoesNotChangeAtEdition = instance.start == start_date and instance.end == end_date

            if dateDoesNotChangeAtEdition:
                return data
            elif instance.start.timestamp() < current_date and instance.start != start_date:
                raise serializers.ValidationError({"start_period": "Você não pode mais alterar o período inicial, pois a data atual é posterior a ele!"})
            elif instance.end.timestamp() < current_date:
                if instance.end != end_date:
                    raise serializers.ValidationError({"end_period": "Você não pode mais alterar o período final, pois a data atual é posterior a ele!"})
                elif instance.description != data['description']:
                    raise serializers.ValidationError({"description": "Você não pode mais alterar a descrição, pois o período do evento acabou!"})
        
        if start_date.timestamp() <= current_date:
            raise serializers.ValidationError({"start_period": "O período inicial deve ser posterior ao período atual."})
        elif start_date >= end_date:
            raise serializers.ValidationError({"end_period": "O período final deve ser posterior ao período inicial."})
            

        return data
    
