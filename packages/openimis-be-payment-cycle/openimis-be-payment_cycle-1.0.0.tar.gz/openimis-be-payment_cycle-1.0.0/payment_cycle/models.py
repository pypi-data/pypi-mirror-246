from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models import HistoryModel


class PaymentCycle(HistoryModel):
    run_year = models.IntegerField()
    run_month = models.SmallIntegerField()
    type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True, unique=False)
