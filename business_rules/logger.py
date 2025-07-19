import logging
import os
import frappe

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
