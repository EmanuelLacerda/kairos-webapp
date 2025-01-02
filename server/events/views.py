from .models import Event
from .serializers import EventSerializer

from rest_framework import status, viewsets
from rest_framework.response import Response

from datetime import datetime, timedelta


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def destroy(self, request, pk=None):
        try:
            event = self.get_queryset().get(id=pk)

            current_date = datetime.now() - timedelta(hours=3)
            current_date = current_date.timestamp()

            if event.end.timestamp() <= current_date:
                return Response({"message": "Eventos que já terminaram não podem ser removidos"}, status=status.HTTP_400_BAD_REQUEST)


            event.delete()
            return Response({"message": "Evento removido com sucesso"}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist:
            return Response({"message": "Evento não encontrado"}, status=status.HTTP_404_NOT_FOUND)