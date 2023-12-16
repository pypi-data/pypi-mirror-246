from django.apps import AppConfig

MODULE_NAME = 'payment_cycle'

DEFAULT_CONFIG = {
    'gql_query_payment_cycle_perms': ['200001'],
    'gql_create_payment_cycle_perms': ['200002'],
    'gql_update_payment_cycle_perms': ['200003'],
    'gql_delete_payment_cycle_perms': ['200004'],
    'gql_mutation_process_payment_cycle_perms': ['200005']
}


class PaymentCycleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = MODULE_NAME

    gql_query_payment_cycle_perms = None
    gql_create_payment_cycle_perms = None
    gql_update_payment_cycle_perms = None
    gql_delete_payment_cycle_perms = None
    gql_mutation_process_payment_cycle_perms = None

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(self.name, DEFAULT_CONFIG)
        self.__load_config(cfg)

    @classmethod
    def __load_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(PaymentCycleConfig, field):
                setattr(PaymentCycleConfig, field, cfg[field])
