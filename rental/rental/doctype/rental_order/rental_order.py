# Copyright (c) 2024, me and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe  
from frappe import _, qb

class RentalOrder(Document):
	def validate(self):
		self.validate_location()
		self.validate_itemtable()

	def validate_location(self):
		if not self.location:
			frappe.throw(
				_("Set Location For Shipping")
			)
	def validate_itemtable(self):
		if not self.items:

			frappe.throw(
				_("Add Table values"))

@frappe.whitelist()
def set_table(item_code):
	get_item  = frappe.db.get_all('Rental Item',{'name':item_code},['*'])

	return get_item[0].rental_price, get_item[0].hour_rate
	
@frappe.whitelist()
def set_amount(item_code,qty):
	get_item  = frappe.db.get_all('Rental Item',{'name':item_code},['*'])
	amount = int(get_item[0].rental_price) * int(qty)

	return amount

