# Copyright (c) 2024, me and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RentalReturn(Document):
	pass

def sendmail(doc, method):
	args:{
		'customer':doc.customer,
		'employee_check': doc.custom_employee_check,
		'status': doc.status,
	}

	if doc.custom_status == 'Damaged':
		frappe.sendmail(
            recipients= ['sample'],
            template='damaged',
            args=args,
            subject=f"Rental Return Item Damaged",
            delayed=False
        )
	elif not doc.custom_status:
		frappe.sendmail(
            recipients= ['sample'],
            template='return_confirmation',
            args=args,
            subject=f"Rental Item Returned",
            delayed=False
        )