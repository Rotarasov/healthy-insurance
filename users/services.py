from math import ceil
from typing import Dict, List, Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import Measurement, InsurancePrice


User = get_user_model()


NORMAL_HRV_RANGE = {
    10: {'sdnn': {'left': 101, 'right': 279}, 'sdann': {'left': 85, 'right': 261}, 'rmssd': {'left': 25, 'right': 103}},
    20: {'sdnn': {'left': 93, 'right': 257}, 'sdann': {'left': 79, 'right': 241}, 'rmssd': {'left': 21, 'right': 87}},
    30: {'sdnn': {'left': 86, 'right': 237}, 'sdann': {'left': 73, 'right': 223}, 'rmssd': {'left': 18, 'right': 74}},
    40: {'sdnn': {'left': 79, 'right': 219}, 'sdann': {'left': 67, 'right': 206}, 'rmssd': {'left': 15, 'right': 63}},
    50: {'sdnn': {'left': 63, 'right': 190}, 'sdann': {'left': 63, 'right': 190}, 'rmssd': {'left': 13, 'right': 53}},
    60: {'sdnn': {'left': 68, 'right': 186}, 'sdann': {'left': 58, 'right': 176}, 'rmssd': {'left': 11, 'right': 45}},
    70: {'sdnn': {'left': 62, 'right': 172}, 'sdann': {'left': 53, 'right': 163}, 'rmssd': {'left': 9, 'right': 38}},
    80: {'sdnn': {'left': 49, 'right': 151}, 'sdann': {'left': 49, 'right': 151}, 'rmssd': {'left': 8, 'right': 32}},
    90: {'sdnn': {'left': 53, 'right': 147}, 'sdann': {'left': 45, 'right': 140}, 'rmssd': {'left': 7, 'right': 28}},
}


SDNN_SALE_COEFFICIENT = 0.07
SDANN_SALE_COEFFICIENT = 0.05
RMSSD_SALE_COEFFICIENT = 0.03

NUMBER_OF_PREVIOUS_PRICES = 5
MINIMUM_ACCEPTABLE_RATIO = 0.8
STABILITY_DISCOUNT_COEFFICIENT = 0.05


def calculate_health_discount(measurement: Measurement, normal_hrv_features: Dict[str, Dict[str, int]]) -> float:
    normal_sdnn_range = normal_hrv_features['sdnn']
    normal_sdann_range = normal_hrv_features['sdann']
    normal_rmssd_range = normal_hrv_features['rmssd']

    return (
            SDNN_SALE_COEFFICIENT * (normal_sdnn_range['left'] <= measurement.sdnn <= normal_sdnn_range['right'])
            + SDANN_SALE_COEFFICIENT * (normal_sdann_range['left'] <= measurement.sdann <= normal_sdann_range['right'])
            + RMSSD_SALE_COEFFICIENT * (normal_rmssd_range['left'] <= measurement.rmssd <= normal_rmssd_range['right'])
    )


def calculate_stability_discount(standard_price: int, previous_prices: Union[QuerySet, List[InsurancePrice]]) -> float:
    total_number = len(previous_prices)
    total_number_with_discount = sum(map(lambda p: p.price < standard_price, previous_prices))

    if total_number == 0 or total_number_with_discount / total_number < MINIMUM_ACCEPTABLE_RATIO:
        return 0

    return STABILITY_DISCOUNT_COEFFICIENT


def calculate_user_insurance_price(user: User, measurement:Measurement) -> int:
    round_function = round
    if user.age % 10 == 5:
        round_function = ceil

    user_age_category = round_function(user.age / 10) * 10
    standard_insurance_price = user.insurance_company.individual_price

    normal_hrv_features = NORMAL_HRV_RANGE[user_age_category]
    health_discount = calculate_health_discount(measurement, normal_hrv_features)

    previous_prices = InsurancePrice.objects.all()[:NUMBER_OF_PREVIOUS_PRICES]
    stability_discount = calculate_stability_discount(standard_insurance_price, previous_prices)

    total_discount = health_discount + stability_discount
    return ceil((1 - total_discount) * standard_insurance_price)


def create_user_insurance_price(user: User, measurement: Measurement) -> None:
    price = calculate_user_insurance_price(user, measurement)
    InsurancePrice.objects.create(user=user, measurement=measurement, price=price)



