from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from .models import DownloadTarget
from .views import track_download
from .utils import create_download_click


class TrackDownloadAPIView(APIView):
    """ An API View to track a download for a DownloadTarget """

    @ratelimit(key='ip', rate=lambda r, g: getattr(settings, 'CLICKIFY_RATE_LIMIT', '5/m'), block=True)
    def post(self, request, slug, format=None):
        """ Tracks a download for the given slug """
        target = get_object_or_404(DownloadTarget, slug=slug)

        # Use the helper function with the underlying Django request
        create_download_click(target=target, request=request._request)

        return Response(
            {"message": "Download tracked successfully",
                "target_url": target.target_url},
            status=status.HTTP_200_OK
        )

    def throttled(self, request, wait):
        """ 
        Custom handler for when a request is rat-limited 
        Note: This is for DRF's own throttling, not django-ratelimit.
        """

        return Response(
            {"error": "Rate limit exceeded. Please try again later"},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
