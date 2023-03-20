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
        # deposit = 120 + 40 + 10
        self.assertEqual(user1V2.deposit, 120)
        self.assertEqual(user1V2.bonuses, 50)

        # deposit_for_user2V1
        # 120 + 10 - 40
        self.assertEqual(user2V1.deposit, 80)
        self.assertEqual(user2V1.bonuses, 10)

        # deposit_for_user3V1
        # 120 - 20
        self.assertEqual(user3V1.deposit, 100)
        self.assertEqual(user3V1.bonuses, 0)

    def test_top_up_balance_2(self):
        """
        Test top_up_balance function for 5 ReferralUser objects at different levels.
        """
        user1 = create_new_user(ReferralLevelChoice.V4, None)
        user2 = create_new_user(ReferralLevelChoice.V3, user1)
        user3 = create_new_user(ReferralLevelChoice.V2, user2)
        user4 = create_new_user(ReferralLevelChoice.V1, user3)
        user5 = create_new_user(ReferralLevelChoice.V2, user2)

        top_up_120_balance(user1)
        top_up_120_balance(user2)
        top_up_120_balance(user3)
        top_up_120_balance(user4)
        top_up_120_balance(user5)

        # user1 = 120 + 60 + 10 * 2
        self.assertEqual(user1.deposit, 120)
        self.assertEqual(user1.bonuses, 80)

        # user2 = 120 + 50 * 2 + 10 - 60
        self.assertEqual(user2.deposit, 60)
        self.assertEqual(user2.bonuses, 110)

        # user3 = 120 + 40 - 50 - 10
        self.assertEqual(user3.deposit, 60)
        self.assertEqual(user3.bonuses, 40)

        # user4  = 120 -40 -10
        self.assertEqual(user4.deposit, 70)
        self.assertEqual(user4.bonuses, 0)

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
        user3V1.referral_level.save()
        calculate_referrals_level(user2V1)
        user2V1.referral_level.save()
        calculate_referrals_level(user1V2)
        user1V2.referral_level.save()
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
