# from django.shortcuts import render
from rest_framework import generics
from .models import ReferralUser
from .serializers import ReferralUserSerializer


class ReferralUserDetail(generics.RetrieveAPIView):
    """
    This view is used to retrieve a single ReferralUser instance by its ID.
    """

    queryset = ReferralUser.objects.all()
    serializer_class = ReferralUserSerializer

    def get_object(self):
        """
        Retrieve the `ReferralUser` instance with the ID specified in the URL.
        """
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, id=self.kwargs["id"])
        return obj
