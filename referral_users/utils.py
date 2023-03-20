from typing import List
from .models import ReferralLevel, ReferralUser, ReferralLevelChoice


def reset_level(level: ReferralLevel) -> None:
    """
    Resets the referral level data for a given ReferralLevel object.

    Parameters:
    level (ReferralLevel): The ReferralLevel object to reset.

    Returns:
    None
    """
    level.level = ReferralLevelChoice.V1
    level.team_size = 0
    level.count_direct_refs = 0
    level.count_level2_refs = 0
    level.count_level3_refs = 0
    level.count_level3_refs = 0
    level.count_level4_refs = 0
    level.count_level5_refs = 0


def calculate_referrals_level(user: ReferralUser, level : ReferralLevel = None, refs:  List[ReferralUser] = None) -> None:
    """
    Calculates the referral level for a given ReferralUser object based on the number of referrals they have
    and the referral levels of their referrals.
    """
    if not level:
        level: ReferralLevel = user.referral_level
    reset_level(level)

    if not refs: 
        refs: List[ReferralUser] = user.refs.all()
    for ref in refs:
        level.team_size += ref.referral_level.team_size + 1
        level.count_direct_refs += 1
        if ref.referral_level.level == ReferralLevelChoice.V2:
            level.count_level2_refs += 1
        elif ref.referral_level.level == ReferralLevelChoice.V3:
            level.count_level3_refs += 1
        elif ref.referral_level.level == ReferralLevelChoice.V4:
            level.count_level4_refs += 1
        elif ref.referral_level.level == ReferralLevelChoice.V5:
            level.count_level5_refs += 1
    if level.team_size >= 1500 and \
       level.count_direct_refs >= 20 and \
       level.count_level5_refs >= 3:
        level.level = ReferralLevelChoice.V6
    elif level.team_size >= 800 and \
            level.count_direct_refs >= 12 and \
            level.count_level4_refs >= 3:
        level.level = ReferralLevelChoice.V5
    elif level.team_size >= 300 and \
            level.count_direct_refs >= 8 and \
            level.count_level3_refs >= 3:
        level.level = ReferralLevelChoice.V4
    elif level.team_size >= 100 and \
            level.count_direct_refs >= 5 and \
            level.count_level2_refs >= 3:
        level.level = ReferralLevelChoice.V3
    elif level.team_size >= 20 and \
            level.count_direct_refs >= 3:
        level.level = ReferralLevelChoice.V2



def top_up_120_balance(user: ReferralUser) -> None:
    """
    Tops up the deposit balance of a given ReferralUser object by 120, and then distributes referral bonuses
    to the user's referrers based on their referral levels.
    """
    ref: ReferralUser = user.referrer
    user.deposit += 120
    while ref:
        if ref.referral_level.level == ReferralLevelChoice.V1 \
                and user.referral_level.level == ReferralLevelChoice.V1 \
                and user.referrer == ref:
            ref.deposit += 10
        elif ref.referral_level.level == ReferralLevelChoice.V2:
            if user.referrer == ref:
                ref.deposit += 40
            elif user.referrer.referral_level.level == ReferralLevelChoice.V1:
                ref.deposit += 10
        elif ref.referral_level.level >= ReferralLevelChoice.V3 and user.referrer == ref \
                and user.referral_level.level >= ref.referral_level.level:
            continue
        elif ref.referral_level.level == ReferralLevelChoice.V3:
            if user.referrer == ref:
                ref.deposit += 50
            else:
                if user.referrer.referral_level.level == ReferralLevelChoice.V1:
                    ref.deposit += 20
                elif user.referrer.referral_level.level == ReferralLevelChoice.V2:
                    ref.deposit += 10
        elif ref.referral_level.level == ReferralLevelChoice.V4:
            if user.referrer == ref:
                ref.deposit += 60
            else:
                if user.referrer.referral_level.level == ReferralLevelChoice.V1:
                    ref.deposit += 30
                elif user.referrer.referral_level.level == ReferralLevelChoice.V2:
                    ref.deposit += 20
                elif user.referrer.referral_level.level == ReferralLevelChoice.V3:
                    ref.deposit += 10
        elif ref.referral_level.level == ReferralLevelChoice.V5:
            if user.referrer == ref:
                ref.deposit += 65
            else:
                if user.referral_level.level == ReferralLevelChoice.V1:
                    ref.deposit += 35
                elif user.referral_level.level == ReferralLevelChoice.V2:
                    ref.deposit += 25
                elif user.referral_level.level == ReferralLevelChoice.V3:
                    ref.deposit += 15
                elif user.referral_level.level == ReferralLevelChoice.V4:
                    ref.deposit += 10
        elif ref.referral_level.level == ReferralLevelChoice.V6:
            if user.referrer == ref:
                ref.deposit += 70
            else:
                if user.referral_level.level == ReferralLevelChoice.V1:
                    ref.deposit += 40
                elif user.referral_level.level == ReferralLevelChoice.V2:
                    ref.deposit += 30
                elif user.referral_level.level == ReferralLevelChoice.V3:
                    ref.deposit += 20
                elif user.referral_level.level == ReferralLevelChoice.V4:
                    ref.deposit += 10
                elif user.referral_level.level == ReferralLevelChoice.V5:
                    ref.deposit += 5
        ref = ref.referrer
