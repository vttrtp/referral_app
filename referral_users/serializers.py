from rest_framework import serializers
from .models import ReferralUser


class ReferralUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ReferralUser model.
    Includes a SerializerMethodField to serialize the direct referrals of the user.
    """

    refs = serializers.SerializerMethodField()

    class Meta:
        model = ReferralUser
        fields = '__all__'

    def get_refs(self, obj):
        """
        Method to serialize the direct referrals of the user as a list of ids.
        """
        if obj.refs.exists():
            return list(obj.refs.values_list('id', flat=True))
        return []