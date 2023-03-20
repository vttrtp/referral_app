from django.db import models

from enum import Enum


class ReferralLevelChoice(models.TextChoices):
    """
    A list of possible referral level choices.
    """

    V1: str = "V1"
    V2: str = "V2"
    V3: str = "V3"
    V4: str = "V4"
    V5: str = "V5"
    V6: str = "V6"


class ReferralUser(models.Model):
    """
    A model to represent a user who has been referred by another user.
    """

    # Override the default ID field with a CharField
    id: str = models.CharField(
        primary_key=True, unique=True, max_length=26)
    LEVEL_CHOICES = [(level.value, level.name)
                     for level in ReferralLevelChoice]
    referrer: "ReferralUser" = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='refs')
    level: ReferralLevelChoice = models.CharField(
        max_length=2, choices=LEVEL_CHOICES, default=ReferralLevelChoice.V1)
    deposit: float = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    bonuses: float = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
