from datetime import date
from math import ceil

from django.contrib.auth import get_user_model

from .models import Measurement


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

SALE_COEFFICIENT = 0.8


def calculate_user_insurance_price(user: User) -> int:
    last_measurement: Measurement = user.measurements.order_by('-end', 'start').first()
    age = (date.today() - user.date_of_birth).days / 366
    preprocessed_age = ceil(age / 10.0) * 10
    normal_hrv_features = NORMAL_HRV_RANGE[preprocessed_age]
    normal_sdnn = normal_hrv_features['sdnn']
    normal_sdann = normal_hrv_features['sdann']
    normal_rmssd = normal_hrv_features['rmssd']
    old_price = user.insurance_company.individual_price
    if (normal_sdnn['left'] <= last_measurement.sdnn <= normal_sdnn['right']
            and normal_sdann['left'] <= last_measurement.sdann <= normal_sdann['right']
            and normal_rmssd['left'] <= last_measurement.rmssd <= normal_rmssd['right']):
        return old_price * SALE_COEFFICIENT
    return old_price



