# from django.shortcuts import render
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
# import logging
# from .models import Events
# from .serializers import EventSerializer
# import traceback
# from django_filters.rest_framework import DjangoFilterBackend
# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework.decorators import api_view
# from rest_framework.pagination import PageNumberPagination



# logger = logging.getLogger(__name__)




# class EventViewSet(viewsets.ModelViewSet):
#     from .permission import IsSuperUserOrEventAdminOrCreator
#     queryset = Events.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsSuperUserOrEventAdminOrCreator]
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["created_by",'artist', 'location', 'date']


#     def perform_create(self, serializer):
#         """Restrict event creation to users with `is_admin=True` or `is_superuser=True`."""
#         user = self.request.user
#         # print("hi",user)

#         # if not (user.is_superuser or getattr(user, "is_admin", False)):  # Ensure `is_admin` exists
#         #     logger.warning(f"Unauthorized event creation attempt by {user}")
#         #     raise permissions.PermissionDenied("Only administrators or superusers can create events.")

#         try:
#             serializer.save(created_by=user)
#             logger.info(f"Event '{serializer.instance.title}' created by {user}")
#         except Exception as e:
#             logger.error(f"Error while creating event: {e}", exc_info=True)
#             raise

#     def update(self, request, *args, **kwargs):
#         """Ensure only the creator or a superuser can update the event."""
#         event = self.get_object()
#         if not (request.user.is_superuser or event.created_by == request.user):
#             return Response(
#                 {"error": "Only the event creator or superusers can update this event."},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         return super().update(request, *args, **kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         """Ensure only the creator or a superuser can partially update the event."""
#         event = self.get_object()
#         if not (request.user.is_superuser or event.created_by == request.user):
#             return Response(
#                 {"error": "Only the event creator or superusers can update this event."},
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         return super().partial_update(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         """Ensure only the event creator or a superuser can delete an event."""
#         event = self.get_object()

#         if not (request.user.is_superuser or event.created_by == request.user):
#             return Response(
#                 {"error": "Only the event creator or superusers can delete this event."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         self.perform_destroy(event)
#         return Response(
#             {"message": f"Event '{event.title}' was successfully deleted."},
#             status=status.HTTP_200_OK
#         )


