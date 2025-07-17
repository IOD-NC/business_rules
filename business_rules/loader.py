# -*- coding: utf-8 -*-
import frappe
from rule_engine import Rule
from functools import lru_cache
from typing import List

@lru_cache(maxsize=128)
def _get_compiled_rule(condition: str) -> Rule:
    """
    Compile une expression et la met en cache.
    Cette fonction est privée au module loader.
    """
    return Rule(condition)

def load_active_rules(document_type: str, event: str) -> List[frappe._dict]:
    """
    Charge les règles actives pour un DocType et un événement donnés,
    triées par priorité. [cite: 1661-1665]
    """
    rules_data = frappe.get_all(
        "Business Rules",
        filters={
            "document_type": document_type,
            "event": event,
            "is_active": 1
        },
        fields=["name", "condition", "action_type", "action_args"],
        order_by="priority asc"
    )

    compiled_rules = []
    for r in rules_data:
        try:
            # Compile la règle via le cache LRU
            r.rule_engine_instance = _get_compiled_rule(r.condition)
            compiled_rules.append(r)
        except Exception as e:
            frappe.log_error(
                f"Erreur de compilation de la règle {r.name}: {e}",
                "Rule Engine Loader"
            )
    return compiled_rules

def clear_cache():
    """
    Invalide le cache de règles compilées. [cite: 1694]
    Cette fonction est appelée par le hook on_update de Business Rules.
    """
    _get_compiled_rule.cache_clear()
    frappe.log_info("Cache des règles métier vidé.", "Rule Engine")
