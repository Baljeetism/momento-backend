from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
import logging
from .models import Events
from .serializers import EventSerializer
import traceback
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        try:
            # Assign the current user as the creator
            serializer.save(created_by=self.request.user)
            logger.info(" Event created successfully")
        except Exception as e:
            logger.error(f" Error while creating event: {e}", exc_info=True)
            raise

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(
                {"message": "Event created successfully!", "event": response.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f" Failed to create event: {e}", exc_info=True)
            return Response({"error": f"Failed to create event: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            event = self.get_object()
            event_title = event.title
            self.perform_destroy(event)
            return Response(
                {"message": f"Event '{event_title}' was successfully deleted."},
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            logger.warning(" Event not found for deletion")
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f" Failed to delete event: {e}", exc_info=True)
            traceback.print_exc()
            return Response({"error": f"Failed to delete event: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# from django.shortcuts import render
# from rest_framework import viewsets, permissions, status
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
# import logging
# from .models import Eventsz
# from .serializers import EventSerializer
# import traceback
# from .filters import EventFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from django.core.exceptions import ObjectDoesNotExist

# # ✅ Set up a logger for error tracking
# logger = logging.getLogger(__name__)

# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Eventsz.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.AllowAny]
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = EventFilter

    
#     def perform_create(self, serializer):
#         try:
#             image = self.request.data.get('image', None)
#             image_artist = self.request.data.get('image_artist', None)

#             serializer.save(
#                 image=image,
#                 image_artist=image_artist
#             )
#         except Exception as e:
#             logger.error(f"Failed to create event: {e}", exc_info=True)
#             raise ValueError("Failed to create event due to invalid data or file upload issues.")

    
#     def create(self, request, *args, **kwargs):
#         try:
#             response = super().create(request, *args, **kwargs)
#             event = response.data
#             return Response(
#                 {"message": "Event created successfully!", "event": event},
#                 status=status.HTTP_201_CREATED
#             )
#         except Exception as e:
#             logger.error(f"Error creating event: {e}", exc_info=True)
#             return Response(
#                 {"error": "Failed to create event. Please check your data and try again."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

   
#     def destroy(self, request, *args, **kwargs):
#         try:
#             event = self.get_object()
#             event_title = event.title
#             self.perform_destroy(event)

#             return Response(
#                 {"message": f"Event '{event_title}' was successfully deleted."},
#                 status=status.HTTP_200_OK
#             )

#         except ObjectDoesNotExist:
#             return Response(
#                 {"error": "Event not found."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except Exception as e:
#             logger.error(f"Failed to delete event: {e}", exc_info=True)
#             traceback.print_exc()
#             return Response(
#                 {"error": f"Failed to delete event: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
