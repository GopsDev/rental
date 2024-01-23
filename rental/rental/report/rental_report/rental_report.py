import frappe
from frappe import _, qb

def execute(filters=None):
    columns = [
        {"fieldname": "name", "label": _("ID"), "fieldtype": "Data",},
        {"fieldname": "item_code", "label": _("item_code"), "fieldtype": "Data"},
        {"fieldname": "rental_price", "label": _("rental_price"), "fieldtype": "Data"},
        {"fieldname": "condition", "label": _("condition"), "fieldtype": "Data"},
        {"fieldname": "category", "label": _("category"), "fieldtype": "Data"},
        {"fieldname": "purchase_date", "label": _("purchase_date"), "fieldtype": "Data"},
        {"fieldname": "customer", "label": _("customer"), "fieldtype": "Data"},
        {"fieldname": "valid_till", "label": _("valid_till"), "fieldtype": "Data"},
        {"fieldname": "amount", "label": _("amount"), "fieldtype": "Data"},
        {"fieldname": "total_time", "label": _("total_time"), "fieldtype": "Data"},
    ]

    data = frappe.get_all("Rental Item", filters=filters, fields=["name", "item_code", "rental_price","condition","category","purchase_date"])
    data1 = frappe.get_all("Rental Order", filters=filters, fields=["customer","valid_till"])
    
    data2 = frappe.get_all("Rental Order Item", filters=filters, fields=["amount","total_time"])

    return columns, data + data1 + data2
