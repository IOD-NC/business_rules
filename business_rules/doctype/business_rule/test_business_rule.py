import frappe
import unittest

class TestBusinessRule(unittest.TestCase):
    def test_rule_existence(self):
        """Vérifie que la règle de test est bien présente en base"""
        rule = frappe.db.exists("Business Rule", {
            "rule_name": "Test: Bloquer si > 5 jours sans ancienneté",
            "applies_to_doctype": "Leave Application",
            "event_trigger": "before_submit",
            "is_active": 1
        })
        self.assertTrue(rule, "La règle de test n'existe pas ou est inactive.")

    def test_rule_expression_format(self):
        """Valide la syntaxe de l'expression"""
        rule = frappe.get_doc("Business Rule", "Test: Bloquer si > 5 jours sans ancienneté")
        self.assertIn("doc.total_leave_days", rule.rule_expression)
        self.assertIn("doc.employee_seniority", rule.rule_expression)

    def test_action_code_safety(self):
        """Vérifie que l'action_if_true utilise bien frappe.throw et n'est pas dangereuse"""
        rule = frappe.get_doc("Business Rule", "Test: Bloquer si > 5 jours sans ancienneté")
        self.assertTrue(rule.action_if_true.strip().startswith("frappe.throw"))
        self.assertNotIn("exec(", rule.action_if_true)
        self.assertNotIn("eval(", rule.action_if_true)
