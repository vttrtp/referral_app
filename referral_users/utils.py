from typing import List
from .models import ReferralUser, ReferralLevelChoice


class ReferralLevelData():
    """
    Helper class for user level calculation
    """

    team_size = 0
    count_direct_refs = 0
    count_level2_refs = 0
    count_level3_refs = 0
    count_level4_refs = 0
    count_level5_refs = 0


def calculate_referrals_level(user: ReferralUser, refs:  List[ReferralUser] = None, team_size: int = -1) -> None:
    """
    Calculates the referral level for a given ReferralUser object based on the number of referrals they have
    and the referral levels of their referrals.
    """

    level = ReferralLevelData()

    if team_size != -1:
        level.team_size = team_size

    if refs == None:
        refs: List[ReferralUser] = user.refs.all()

    for ref in refs:
        if team_size == -1:
            level.team_size += 1 + len(ref.refs.all())
        level.count_direct_refs += 1
        if ref.level == ReferralLevelChoice.V2:
            level.count_level2_refs += 1
        elif ref.level == ReferralLevelChoice.V3:
            level.count_level3_refs += 1
        elif ref.level == ReferralLevelChoice.V4:
            level.count_level4_refs += 1
        elif ref.level == ReferralLevelChoice.V5:
            level.count_level5_refs += 1

    if level.team_size >= 1500 and \
       level.count_direct_refs >= 20 and \
       level.count_level5_refs >= 3:
        user.level = ReferralLevelChoice.V6
    elif level.team_size >= 800 and \
            level.count_direct_refs >= 12 and \
            level.count_level4_refs >= 3:
        user.level = ReferralLevelChoice.V5
    elif level.team_size >= 300 and \
            level.count_direct_refs >= 8 and \
            level.count_level3_refs >= 3:
        user.level = ReferralLevelChoice.V4
    elif level.team_size >= 100 and \
            level.count_direct_refs >= 5 and \
            level.count_level2_refs >= 3:
        user.level = ReferralLevelChoice.V3
    elif level.team_size >= 20 and \
            level.count_direct_refs >= 3:
        user.level = ReferralLevelChoice.V2
    else:
        user.level = ReferralLevelChoice.V1


def top_up_120_balance(user: ReferralUser) -> None:
    """
    Tops up the deposit balance of a given ReferralUser object by 120, and then distributes referral bonuses
    to the user's referrers based on their referral levels.
    """
    ref: ReferralUser = user.referrer
    child = user
    user.deposit += 120

    for i in range(0, 2):
        if not ref:
            break
        spend_bonuses = 0
        if ref.level == ReferralLevelChoice.V1 \
                and user.level == ReferralLevelChoice.V1 \
                and user.referrer == ref:
            spend_bonuses = 10
        elif ref.level == ReferralLevelChoice.V2:
            if user.referrer == ref:
                spend_bonuses = 40
            elif user.referrer.level == ReferralLevelChoice.V1:
                spend_bonuses = 10
        elif ref.level >= ReferralLevelChoice.V3 \
                and child.level >= ref.level:
            pass
        elif ref.level == ReferralLevelChoice.V3:
            if user.referrer == ref:
                spend_bonuses = 50
            else:
                if user.referrer.level == ReferralLevelChoice.V1:
                    spend_bonuses = 20
                elif user.referrer.level == ReferralLevelChoice.V2:
                    spend_bonuses = 10
        elif ref.level == ReferralLevelChoice.V4:
            if user.referrer == ref:
                spend_bonuses = 60
            else:
                if user.referrer.level == ReferralLevelChoice.V1:
                    spend_bonuses = 30
                elif user.referrer.level == ReferralLevelChoice.V2:
                    spend_bonuses = 20
                elif user.referrer.level == ReferralLevelChoice.V3:
                    spend_bonuses = 10
        elif ref.level == ReferralLevelChoice.V5:
            if user.referrer == ref:
                spend_bonuses = 65
            else:
                if user.referrer.level == ReferralLevelChoice.V1:
                    spend_bonuses = 35
                elif user.referrer.level == ReferralLevelChoice.V2:
                    spend_bonuses = 25
                elif user.referrer.level == ReferralLevelChoice.V3:
                    spend_bonuses = 15
                elif user.referrer.level == ReferralLevelChoice.V4:
                    spend_bonuses = 5
        elif ref.level == ReferralLevelChoice.V6:
            if user.referrer == ref:
                spend_bonuses = 70
            else:
                if user.referrer.level == ReferralLevelChoice.V1:
                    spend_bonuses = 40
                elif user.referrer.level == ReferralLevelChoice.V2:
                    spend_bonuses = 30
                elif user.referrer.level == ReferralLevelChoice.V3:
                    spend_bonuses = 20
                elif user.referrer.level == ReferralLevelChoice.V4:
                    spend_bonuses = 10
                elif user.referrer.level == ReferralLevelChoice.V5:
                    spend_bonuses = 5

        ref.bonuses += spend_bonuses
        user.deposit -= spend_bonuses
        child = ref
        ref = ref.referrer
