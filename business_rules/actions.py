# -*- coding: utf-8 -*-
import frappe
import json

def _action_update_field(doc, args):
    """Met à jour un champ du document."""
    field = args.get("fieldname")
    value = args.get("value")
    if not field:
        frappe.throw("L'action 'update_field' requiert le paramètre 'fieldname'.")
    doc.set(field, value)

def _action_raise_error(doc, args):
    """Affiche un message d'erreur et bloque l'opération."""
    message = args.get("message")
    if not message:
        frappe.throw("L'action 'raise_error' requiert le paramètre 'message'.")
    frappe.throw(message)

# Dictionnaire des actions autorisées (la "whitelist")
ACTION_HANDLERS = {
    "update_field": _action_update_field,
    "raise_error": _action_raise_error,
}

def run_secure_action(action_type: str, action_args_json: str, doc):
    """
    Point d'entrée sécurisé pour exécuter une action. [cite: 441-445]
    """
    handler = ACTION_HANDLERS.get(action_type)
    if not handler:
        frappe.log_error(f"Tentative d'appel d'une action non autorisée : {action_type}", "Rule Engine Actions")
        return

    try:
        args = json.loads(action_args_json)
    except json.JSONDecodeError:
        frappe.log_error(f"Impossible de parser les arguments JSON pour l'action {action_type}", "Rule Engine Actions")
        return

    # Appelle la fonction correspondante (ex: _action_update_field)
    handler(doc, args)
