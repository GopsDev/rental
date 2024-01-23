# Copyright (c) 2024, me and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _, qb
from frappe.utils import getdate, today

class RentalItem(Document):
	def validate(self):
		self.validate_delivery_date()
		self.validate_hours()

	def validate_delivery_date(self):
		if not self.purchase_date:
			frappe.throw(
				_("Set purchase_date")
			)
		if getdate(self.purchase_date) >= getdate(today()):
			frappe.throw(_("purchase_date must be after today"))

	def validate_hours(self):
		if not self.hour_rate:
			frappe.throw(
				_("Set Hours for rate")
			)
		if not isinstance(self.hour_rate, int):
			frappe.throw(_("Hours must be an integer"))



