import calendar
import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, Union, Any

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet

from calculation.services import get_calculation_object
from contribution_plan.models import PaymentPlan
from core.models import InteractiveUser, VersionedModel, HistoryModel, User
from core.services.utils import output_exception, output_result_success
from payment_cycle.models import PaymentCycle
from social_protection.models import BenefitPlan

logger = logging.getLogger(__name__)


class PaymentCycleService(ABC):
    """
    Generic payment cycle service specifying workflow for generating payment cycle information for a specific business
    models. Based on Batch Run.
    """

    def __init__(self, user: Union[InteractiveUser, User]):
        self._user = user
        self._audit_user_id = user.id if isinstance(self._user, InteractiveUser) else user.i_user_id
        self._username = user.login_name if isinstance(self._user, InteractiveUser) else user.username

    def process(self, **kwargs) -> Dict:
        """
        Perform a processing run of payment cycle for a specific year and month. The run will only be performed if
        the run for that month does not exist yet.
        :param kwargs: Any arguments required to process the payment cycle. year and month are required
        :return: Dict containing status of a current payment cycle process run
        """
        year, month = int(kwargs['year']), int(kwargs['month'])
        logger.debug('payment cycle for period %s-%s', month, year)
        if self._payment_cycle_entry_exists(**kwargs):
            logger.debug('payment cycle for period %s-%s already processed, skipping', month, year)
            self._output_exception('PaymentCycle already processed for %s-%s' % (month, year))

        _, days_in_month = calendar.monthrange(year, month)
        end_date = datetime.datetime(year, month, days_in_month)

        payment_cycle_entry = self._create_payment_cycle_entry(**kwargs)
        logger.debug("payment cycle created entry: %s", payment_cycle_entry.id)

        q = self._get_main_queryset(end_date, **kwargs)

        logger.debug('Processing payment cycle %s-%s for %s entries', month, year, q.count())
        entry_outputs = {}
        for entry in q:
            entry_output = self._process_main_queryset_entry(entry, payment_cycle_entry, end_date, **kwargs)
            entry_outputs[str(entry.id)] = entry_output
        return output_result_success(entry_outputs)

    @abstractmethod
    def _process_main_queryset_entry(self, entry: Union[HistoryModel, VersionedModel],
                                     payment_cycle_entry: PaymentCycle, end_date: datetime, **kwargs) -> Any:
        """
        Process a single entry returned from _get_main_queryset().
        :param payment_cycle_entry: Model of a current payment cycle process entry
        :param entry: Model of a current benefit plan to process
        :param end_date: Date indicating last day of the current month
        :return: Status of processing a single entry from main queryset. Will be collected and returned from process()
        """
        raise NotImplementedError('`process_main_queryset_entry` must be implemented.')

    @abstractmethod
    def _get_main_queryset(self, end_date: datetime, **kwargs) -> QuerySet:
        """
        Return a queryset of all active entries to process payment cycles for.
        :param end_date: Date indicating last day of the current month
        :return: A queryset of all active objects to process payment cycles for
        """
        raise NotImplementedError('`get_main_queryset` must be implemented.')

    @abstractmethod
    def _create_payment_cycle_entry(self, **kwargs) -> PaymentCycle:
        """
        Create PaymentCycle object logging a payment cycle process for a specific year and month. Can be customized for
        current object type.
        :return: PaymentCycle object for a current process
        """
        raise NotImplementedError('`create_payment_cycle_entry` must be implemented.')

    @abstractmethod
    def _payment_cycle_entry_exists(self, **kwargs) -> bool:
        """
        Check if an entry of PaymentCycle object logging a payment cycle process for a specific year and month already
        exists. The run will be skipped if it does.
        :return:
        """
        raise NotImplementedError('`payment_cycle_entry_exists` must be implemented.')

    @staticmethod
    def _output_exception(error, method='process', model='PaymentCycle'):
        output_exception(error, method, model)

    @staticmethod
    def _get_start_date(end_date, periodicity):
        year = end_date.year
        month = end_date.month
        if periodicity not in [1, 2, 3, 4, 6, 12]:
            return None
        return datetime.date(year, month - periodicity + 1, 1) if month % periodicity == 0 else None


class BenefitPlanPaymentCycleService(PaymentCycleService):

    def __init__(self, user):
        super().__init__(user)
        self._bf_content_type = ContentType.objects.get_for_model(BenefitPlan)

    def _process_main_queryset_entry(self, entry: Union[HistoryModel, VersionedModel],
                                     payment_cycle_entry: PaymentCycle, end_date: datetime, **kwargs) -> Any:
        payment_plans = self._get_payment_plan_queryset(entry, end_date)
        for payment_plan in payment_plans:
            start_date = self._get_start_date(end_date, payment_plan.periodicity)
            if not start_date:
                # Not a month of payment
                continue
            calculation = get_calculation_object(payment_plan.calculation)
            if not calculation:
                logger.warning("Payment plan with not existent calculation: %s", payment_plan.id)
                continue
            return calculation.calculate_if_active_for_object(payment_plan, payment_cycle=payment_cycle_entry,
                                                              audit_user_id=self._audit_user_id, start_date=start_date,
                                                              end_date=end_date)

    def _payment_cycle_entry_exists(self, **kwargs) -> bool:
        return PaymentCycle.objects.filter(
            run_year=kwargs['year'],
            run_month=kwargs['month'],
            type=self._bf_content_type,
            is_deleted=False
        ).exists()

    def _create_payment_cycle_entry(self, **kwargs) -> PaymentCycle:
        pc = PaymentCycle(run_year=kwargs['year'], run_month=kwargs['month'], type=self._bf_content_type)
        pc.save(username=self._username)
        return pc

    def _get_main_queryset(self, end_date: datetime, **kwargs) -> QuerySet:
        return BenefitPlan.objects \
            .filter(date_valid_from__lte=end_date, is_deleted=False) \
            .filter(Q(date_valid_to__gte=end_date) | Q(date_valid_to__isnull=True))

    def _get_payment_plan_queryset(self, entry: Union[HistoryModel, VersionedModel], end_date: datetime):
        return PaymentPlan.objects \
            .filter(date_valid_to__gte=end_date) \
            .filter(date_valid_from__lte=end_date) \
            .filter(benefit_plan_id=entry.id) \
            .filter(benefit_plan_type=self._bf_content_type) \
            .filter(is_deleted=False)
