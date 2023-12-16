import logging

from django.apps import AppConfig

MODULE_NAME = 'invoice'

DEFAULT_CONFIG = {
    "default_currency_code": "USD",
    "gql_invoice_search_perms": ["155101"],
    "gql_invoice_create_perms": ["155102"],
    "gql_invoice_update_perms": ["155103"],
    "gql_invoice_delete_perms": ["155104"],
    "gql_invoice_amend_perms":  ["155109"],

    "gql_invoice_payment_search_perms": ["155201"],
    "gql_invoice_payment_create_perms": ["155202"],
    "gql_invoice_payment_update_perms": ["155203"],
    "gql_invoice_payment_delete_perms": ["155204"],
    "gql_invoice_payment_refund_perms": ["155206"],

    "gql_invoice_event_search_perms":             ["155301"],
    "gql_invoice_event_create_perms":             ["155302"],
    "gql_invoice_event_update_perms":             ["155303"],
    "gql_invoice_event_delete_perms":             ["155304"],
    "gql_invoice_event_create_message_perms":     ["155306"],
    "gql_invoice_event_delete_my_message_perms":  ["155307"],
    "gql_invoice_event_delete_all_message_perms": ["155308"],

    "gql_bill_search_perms": ["156101"],
    "gql_bill_create_perms": ["156102"],
    "gql_bill_update_perms": ["156103"],
    "gql_bill_delete_perms": ["156104"],
    "gql_bill_amend_perms":  ["156109"],

    "gql_bill_payment_search_perms": ["156201"],
    "gql_bill_payment_create_perms": ["156202"],
    "gql_bill_payment_update_perms": ["156203"],
    "gql_bill_payment_delete_perms": ["156204"],
    "gql_bill_payment_refund_perms": ["156206"],

    "gql_bill_event_search_perms":             ["156301"],
    "gql_bill_event_create_perms":             ["156302"],
    "gql_bill_event_update_perms":             ["156303"],
    "gql_bill_event_delete_perms":             ["156304"],
    "gql_bill_event_create_message_perms":     ["156306"],
    "gql_bill_event_delete_my_message_perms":  ["156307"],
    "gql_bill_event_delete_all_message_perms": ["156308"],
}

logger = logging.getLogger(__name__)


class InvoiceConfig(AppConfig):
    name = MODULE_NAME

    default_currency_code = None
    gql_invoice_search_perms = None
    gql_invoice_create_perms = None
    gql_invoice_update_perms = None
    gql_invoice_delete_perms = None
    gql_invoice_amend_perms = None
    gql_invoice_payment_search_perms = None
    gql_invoice_payment_create_perms = None
    gql_invoice_payment_update_perms = None
    gql_invoice_payment_delete_perms = None
    gql_invoice_payment_refund_perms = None
    gql_invoice_event_search_perms = None
    gql_invoice_event_create_perms = None
    gql_invoice_event_update_perms = None
    gql_invoice_event_delete_perms = None
    gql_invoice_event_create_message_perms = None
    gql_invoice_event_delete_my_message_perms = None
    gql_invoice_event_delete_all_message_perms = None
    gql_bill_search_perms = None
    gql_bill_create_perms = None
    gql_bill_update_perms = None
    gql_bill_delete_perms = None
    gql_bill_amend_perms = None
    gql_bill_payment_search_perms = None
    gql_bill_payment_create_perms = None
    gql_bill_payment_update_perms = None
    gql_bill_payment_delete_perms = None
    gql_bill_payment_refund_perms = None
    gql_bill_event_search_perms = None
    gql_bill_event_create_perms = None
    gql_bill_event_update_perms = None
    gql_bill_event_delete_perms = None
    gql_bill_event_create_message_perms = None
    gql_bill_event_delete_my_message_perms = None
    gql_bill_event_delete_all_message_perms = None

    def __load_config(self, cfg):
        for field in cfg:
            if hasattr(InvoiceConfig, field):
                setattr(InvoiceConfig, field, cfg[field])

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CONFIG)
        self.__load_config(cfg)
