from core.datetimes.ad_datetime import datetime

benefit_plan_payload = {
    "code": "example",
    "name": "example_name",
    "max_beneficiaries": 0,
    "ceiling_per_beneficiary": "0.00",
    "beneficiary_data_schema": {
        "$schema": "https://json-schema.org/draft/2019-09/schema"
    },
    "date_valid_from": "2023-01-01",
    "date_valid_to": "2043-12-31",
}

individual_payload = {
    'first_name': 'TestFN',
    'last_name': 'TestLN',
    'dob': datetime.now(),
    'json_ext': {
        'key': 'value',
        'key2': 'value2'
    }
}

beneficiary_payload = {
    "status": "ACTIVE",
    "date_valid_from": "2023-01-01",
    "date_valid_to": "2043-12-31",
}

payment_plan_payload = {
    'code': 'test',
    'name': 'TestPlan',
    "date_valid_from": "2023-01-01",
    "date_valid_to": "2043-12-31",
    'calculation': '32d96b58-898a-460a-b357-5fd4b95cd87c',
    'periodicity': 1,
    'json_ext': {
        'calculation_rule': {
            'fixed_batch': 1500,
            'limit_per_single_transaction': 100000,
        },
        'advanced_criteria': [
            {
                'custom_filter_condition': 'able_bodied__exact__boolean=False',
                'count_to_max': False, 'amount': 2000
            }
        ]
    }
}
