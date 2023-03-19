import secrets
from django.test import TestCase
from .models import ReferralLevel, ReferralUser, ReferralLevelChoice
from .utils import *


def create_new_user(level: ReferralLevelChoice, referral_user: ReferralUser) -> ReferralUser:
    """
    Create and return a new ReferralUser object with the given level and referral user.
    """

    id = secrets.token_hex(13).upper()
    level = ReferralLevel.objects.create(level=level)
    user = ReferralUser.objects.create(
        referrer=referral_user, referral_level=level, id=id)
    return user


class ReferralUserTest(TestCase):
    """
    Unit tests for ReferralUser model and utils functions.
    """

    def test_top_up_balance_1(self):
        """
        Test top_up_balance function for 3 ReferralUser objects at different levels.
        """
        user1V2 = create_new_user(ReferralLevelChoice.V2, None)
        user2V1 = create_new_user(ReferralLevelChoice.V1, user1V2)
        user3V1 = create_new_user(ReferralLevelChoice.V1, user2V1)

        top_up_120_balance(user1V2)
        top_up_120_balance(user2V1)
        top_up_120_balance(user3V1)

        # deposit for user1V2
        # 120 + 40 + 10 = 170
        self.assertEqual(user1V2.deposit, 170)

        # deposit_for_user2V1
        # 120 + 10 = 130
        self.assertEqual(user2V1.deposit, 130)

        # deposit_for_user3V1
        # 120
        self.assertEqual(user3V1.deposit, 120)

    def test_calculate_referrals_level(self):
        """
        Test calculate_referrals_level function for 3 ReferralUser objects at different levels.
        """
        user1V2 = create_new_user(ReferralLevelChoice.V2, None)
        for i in range(0, 6):
            create_new_user(ReferralLevelChoice.V1, user1V2)
        user2V1 = create_new_user(ReferralLevelChoice.V1, user1V2)
        for i in range(0, 7):
            create_new_user(ReferralLevelChoice.V1, user2V1)
        user3V1 = create_new_user(ReferralLevelChoice.V1, user2V1)
        for i in range(0, 8):
            create_new_user(ReferralLevelChoice.V1, user3V1)

        calculate_referrals_level(user3V1)
        calculate_referrals_level(user2V1)
        calculate_referrals_level(user1V2)

        # user1V2
        self.assertEqual(user1V2.referral_level.level, ReferralLevelChoice.V2)
        self.assertEqual(user1V2.referral_level.team_size, 23)
        self.assertEqual(user1V2.referral_level.count_direct_refs, 7)
        self.assertEqual(user1V2.referral_level.count_level2_refs, 0)
        self.assertEqual(user1V2.referral_level.count_level3_refs, 0)
        self.assertEqual(user1V2.referral_level.count_level4_refs, 0)
        self.assertEqual(user1V2.referral_level.count_level5_refs, 0)

        # user2V1
        self.assertEqual(user2V1.referral_level.level, ReferralLevelChoice.V1)
        self.assertEqual(user2V1.referral_level.team_size, 16)
        self.assertEqual(user2V1.referral_level.count_direct_refs, 8)

        # user3V1
        self.assertEqual(user3V1.referral_level.level, ReferralLevelChoice.V1)
        self.assertEqual(user3V1.referral_level.team_size, 8)
        self.assertEqual(user3V1.referral_level.count_direct_refs, 8)
