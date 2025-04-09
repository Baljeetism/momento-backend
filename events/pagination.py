from .models import Events
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .serializers import EventSerializer
from rest_framework.response import Response


class EventPagination(PageNumberPagination):
    page_size = 6  
    page_size_query_param = "page_size"
    max_page_size = 20  

    @api_view(["GET"])
    def event_list(request):
        events = Events.objects.all()

        artist = request.GET.get("artist", "")
        location = request.GET.get("location", "")
        date = request.GET.get("date", "")

        if artist:
            events = events.filter(artist__icontains=artist)
        if location:
            events = events.filter(location__icontains=location)
        if date:
            events = events.filter(date=date)  # Ensure format is correct

        paginator = EventPagination()
        result_page = paginator.paginate_queryset(events, request)

        if result_page is not None:
            serializer = EventSerializer(result_page, many=True, context={"request": request})
            return paginator.get_paginated_response(serializer.data)

        serializer = EventSerializer(events, many=True, context={"request": request})
        return Response(serializer.data)
