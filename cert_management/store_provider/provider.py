import re

from cert_management.contract.store_provider_contract import StoreProviderContract
from cert_management.configuration.variables import Configuration
from cert_management.store_provider import list_of_providers
import importlib


def choose_provider():
    provider_dir, provider_class = charge_provider()
    provider = vars(importlib.import_module(f"store_provider.{provider_dir}"))
    return provider[provider_class]

def charge_provider():
    provider_charge = False
    provider_dir = None
    provider_class = None
    for provider in list_of_providers:
            raw_data = Configuration.get(f"{str.upper(provider)}_PROVIDER")
            current_provider_is_used = bool(raw_data)
            if provider_charge is True and current_provider_is_used is True:
                raise Exception("system not support two providers enabled")
            if current_provider_is_used:
                provider_charge = True
                provider_dir = f"{provider}_store_provider"
                provider_class_name = format_provider_name_for_class_shape(provider)
                provider_class = f"{provider_class_name}StoreProvider"

    return  provider_dir,provider_class

def format_provider_name_for_class_shape(provider):
    if re.match(r'^[a-z]+([_-][a-z]+)*$', provider):
        text = provider.replace('-', '_')
        words = text.split('_')
        provider_camel_case = ''.join(word.capitalize() for word in words)
        return provider_camel_case
    return  provider



