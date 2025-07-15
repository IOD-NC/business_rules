# -*- coding: utf-8 -*-
import frappe
import traceback
from .loader import load_active_rules
from .actions import run_secure_action

def execute_rules(doc, event):
    """
    Point d'entrée principal appelé par les hooks Frappe.
    """
    # Liste des DocTypes à ignorer pour ne pas surcharger le système
    SKIP_DOCTYPES = {"Version", "Activity Log", "Email Queue", "Error Log"}
    if doc.doctype in SKIP_DOCTYPES:
        return

    try:
        # 1. Charger les règles compilées applicables
        rules = load_active_rules(doc.doctype, event.lower())

        # 2. Évaluer chaque règle en séquence
        for r in rules:
            # La méthode evaluate() vient de la librairie rule-engine
            if r.rule_engine_instance.evaluate(doc.as_dict()):
                # 3. Si la condition est vraie, exécuter l'action sécurisée
                run_secure_action(r.action_type, r.action_args, doc)

    except Exception:
        frappe.log_error(
            f"Erreur critique exécuteur de règles sur {doc.doctype}::{event}",
            traceback.format_exc()
        )

