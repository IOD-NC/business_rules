import frappe
import os
import logging

def get_logger(name="business_rules"):
    log_dir = os.path.join(frappe.get_site_path(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def execute():
    logger = get_logger()

    if frappe.db.table_exists("Business Rule"):
        logger.info("La table 'Business Rule' existe déjà. Patch ignoré.")
        return

    if frappe.db.exists("DocType", "Business Rule"):
        logger.info("Le DocType 'Business Rule' existe déjà. Patch ignoré.")
        return

    logger.info("Création du DocType 'Business Rule'...")

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Business Rule",
        "module": "Business Rules",
        "custom": 0,
        "fields": [
            {"fieldname": "rule_name", "label": "Rule Name", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "applies_to_doctype", "label": "Applies To Doctype", "fieldtype": "Link", "options": "DocType", "reqd": 1},
            {"fieldname": "event_trigger", "label": "Event Trigger", "fieldtype": "Select", "options": "\nbefore_insert\nbefore_save\nbefore_submit\non_submit\non_update", "reqd": 1},
            {"fieldname": "rule_expression", "label": "Rule Expression", "fieldtype": "Text", "reqd": 1},
            {"fieldname": "action_if_true", "label": "Action If True", "fieldtype": "Code"},
            {"fieldname": "action_if_false", "label": "Action If False", "fieldtype": "Code"},
            {"fieldname": "is_active", "label": "Is Active", "fieldtype": "Check", "default": 1}
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1
            }
        ],
        "istable": 0,
        "is_submittable": 0,
        "track_changes": 1,
        "track_views": 1
    })

    doc.insert()
    frappe.db.commit()
    logger.info("DocType 'Business Rule' inséré avec succès.")

    create_index_if_not_exists()
    logger.info("Index ajouté (si inexistant) sur (applies_to_doctype, event_trigger, is_active).")


def create_index_if_not_exists():
    index_name = "idx_business_rule_trigger"
    frappe.db.sql(f"""
        CREATE INDEX IF NOT EXISTS `{index_name}`
        ON `tabBusiness Rule` (`applies_to_doctype`, `event_trigger`, `is_active`)
    """)
