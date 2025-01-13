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
        else:
            """
            Mesmo se nenhum dos casos acima acontecerem, ainda há a possibilidade de acontecer um caso que exige lançamento de exceção, pois o usuário pode tentar agendar um evento para um período de tempo para o qual já há um evento agendado.

            Existem 3 situações nas quais isto pode acontecer. Nos comentários abaixo, é explicado melhor quais são estas situações.
            """

            # Situação 01: O período inicial do evento que será agendado está entre o período inicial e o período final de algum dos eventos já agendados. Para esta situação, independe qual o período final.
            events = Event.objects.filter(
                start__lte=start_date,
                end__gte=start_date
            )

            if instance:
                events = events.exclude(id__exact=instance.id)

            if events:
                raise serializers.ValidationError({"start_period": "O período inicial não pode estar entre o período inicial e final de outro evento! Tente novamente."})
            else:
                # Situação 02: Se chegou aqui, o período inicial do evento que será agendado não está entre o período inicial e o período final de algum dos eventos já agendados. Porém, o período final do mesmo pode está e o período inicial está antes do período inicial do mesmo evento agendado.
                events = Event.objects.filter(
                    start__lte=end_date,
                    end__gte=end_date
                )
                

                if instance:
                    events = events.exclude(id__exact=instance.id)

                if events:
                    raise serializers.ValidationError({"end_period": "O período final não pode estar entre o período inicial e final de outro evento! Tente novamente."})
                else:
                    # Situação 03: Se chegou aqui, ainda existe a possibilidade de que algum dos eventos esteja entre o período do evento que será agendado. Por exemplo, o evento que será agendado é de 10/02/2025 às 10:20 - 17/02/2025 às 17:30 e tem um evento já agendado que é 13/02/2025 às 09:20 - 15/02/2025 às 14:30.
                    events = Event.objects.filter(
                        start__gt=start_date,
                        end__lt=end_date
                    )

                    if instance:
                        events = events.exclude(id__exact=instance.id)

                    if events:
                        raise serializers.ValidationError({"complete_period": "Um ou mais eventos iniciam e terminam entre o período inicial e final deste evento, isto é inválido! Tente novamente."})
            

        return data
    
