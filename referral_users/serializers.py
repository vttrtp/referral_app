from rest_framework import serializers
from .models import ReferralUser, ReferralLevel


class ReferralLevelSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ReferralLevel model.
    """

    class Meta:
        model = ReferralLevel
        fields = '__all__'


class ReferralUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ReferralUser model.
    Includes a SerializerMethodField to serialize the direct referrals of the user.
    """

    refs = serializers.SerializerMethodField()
    referral_level = ReferralLevelSerializer()

    class Meta:
        model = ReferralUser
        fields = '__all__'

    def get_refs(self, obj):
        """
        Method to serialize the direct referrals of the user as a list of ids.
        """
        if obj.refs.exists():
            return list(obj.refs.values_list('id', flat=True))
        return None
