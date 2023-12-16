import graphene
import graphene_django_optimizer as gql_optimizer
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from core.schema import OrderedDjangoFilterConnectionField
from core.utils import append_validity_filter
from payment_cycle.apps import PaymentCycleConfig
from payment_cycle.gql_mutations import ProcessBenefitPlanPaymentCycleMutation
from payment_cycle.gql_queries import PaymentCycleGQLType
from payment_cycle.models import PaymentCycle


class Query(graphene.ObjectType):
    payment_cycle = OrderedDjangoFilterConnectionField(
        PaymentCycleGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        dateValidFrom__Gte=graphene.DateTime(),
        dateValidTo__Lte=graphene.DateTime(),
        applyDefaultValidityFilter=graphene.Boolean(),
        client_mutation_id=graphene.String()
    )

    def resolve_payment_cycle(self, info, **kwargs):
        filters = append_validity_filter(**kwargs)

        client_mutation_id = kwargs.get("client_mutation_id")
        if client_mutation_id:
            filters.append(Q(mutations__mutation__client_mutation_id=client_mutation_id))

        Query._check_permissions(info.context.user, PaymentCycleConfig.gql_query_payment_cycle_perms)
        query = PaymentCycle.objects.filter(*filters)
        return gql_optimizer.query(query, info)

    @staticmethod
    def _check_permissions(user, perms):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(perms):
            raise PermissionError("Unauthorized")


class Mutation(graphene.ObjectType):
    process_benefit_plan_payment_cycle = ProcessBenefitPlanPaymentCycleMutation.Field()
