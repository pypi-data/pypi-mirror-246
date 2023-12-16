from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from contribution_plan.models import PaymentPlan
from core.datetimes.ad_datetime import datetime
from individual.models import Individual
from invoice.models import Bill
from payment_cycle.models import PaymentCycle
from payment_cycle.tests.data import benefit_plan_payload, individual_payload, beneficiary_payload, payment_plan_payload
from payment_cycle.services import BenefitPlanPaymentCycleService
from payment_cycle.tests.helpers import LogInHelper
from social_protection.models import BenefitPlan, Beneficiary


class BenefitPlanPaymentCycleServiceTests(TestCase):
    user = None
    service = None

    test_benefit_plan = None
    test_individual_1 = None
    test_individual_2 = None
    test_beneficiary_1 = None
    test_beneficiary_2 = None
    test_payment_plan = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = LogInHelper().get_or_create_user_api()
        cls.service = BenefitPlanPaymentCycleService(cls.user)

        cls.test_benefit_plan = BenefitPlan(**benefit_plan_payload)
        cls.test_benefit_plan.save(username=cls.user.username)

        cls.test_individual_1 = Individual(**individual_payload)
        cls.test_individual_1.save(username=cls.user.username)

        cls.test_individual_2 = Individual(**{**individual_payload, 'first_name': 'tests2'})
        cls.test_individual_2.save(username=cls.user.username)

        cls.test_beneficiary_1 = Beneficiary(**{
            **beneficiary_payload,
            "individual_id": cls.test_individual_1.id,
            "benefit_plan_id": cls.test_benefit_plan.id
        })
        cls.test_beneficiary_1.save(username=cls.user.username)

        cls.test_beneficiary_2 = Beneficiary(**{
            **beneficiary_payload,
            "individual_id": cls.test_individual_2.id,
            "benefit_plan_id": cls.test_benefit_plan.id
        })
        cls.test_beneficiary_2.save(username=cls.user.username)

        cls.test_payment_plan = PaymentPlan(**{
            **payment_plan_payload,
            'benefit_plan_id': cls.test_benefit_plan.id,
            'benefit_plan_type': ContentType.objects.get_for_model(BenefitPlan)
        })
        cls.test_payment_plan.save(username=cls.user.username)

    def test_trigger_payment_cycle(self):
        t = datetime.now()
        output = self.service.process(year=t.year, month=t.month)

        self.assertTrue(output)
        self.assertTrue(output['success'])
        self.assertEqual(2, Bill.objects.count())
        self.assertEqual(1, PaymentCycle.objects.count())
