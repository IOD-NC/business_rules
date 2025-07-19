import frappe
from business_rules.logger import get_logger

def execute():
    logger = get_logger()

    # Vérifie que le DocType existe
    if not frappe.db.table_exists("Business Rule"):
        logger.warning("Le DocType 'Business Rule' est absent. Règle de test non créée.")
        return

    # Vérifie si la règle existe déjà
    if frappe.db.exists("Business Rule", {"rule_name": "Test: Bloquer si > 5 jours sans ancienneté"}):
        logger.info("La règle de test existe déjà. Patch ignoré.")
        return

    logger.info("Création d'une règle de test dans Business Rule...")

    test_rule = frappe.get_doc({
        "doctype": "Business Rule",
        "module": "business_rule",
        "rule_name": "Test: Bloquer si > 5 jours sans ancienneté",
        "applies_to_doctype": "Leave Application",
        "event_trigger": "before_submit",
        "rule_expression": "doc.total_leave_days > 5 and doc.employee_seniority < 1",
        "action_if_true": "frappe.throw('Vous devez avoir 1 an d\\'ancienneté pour poser plus de 5 jours.')",
        "action_if_false": "pass",
        "is_active": 1
    })

    test_rule.insert()
    frappe.db.commit()

    logger.info("Règle de test insérée avec succès.")
