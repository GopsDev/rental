import frappe
import random

def get_context(context):
    get_order = frappe.db.get_list('Rental Order',{'customer':frappe.session.user},pluck='name')
    if get_order:
        get_order_item = frappe.db.get_all('Rental Order Item',{'parent':get_order[0]},['*'])
    else:
        get_order_item = []
    get_return_item = frappe.db.get_all('Rental Return',{'customer':frappe.session.user},['*'])

    context.orders = get_order_item
    context.return_item = get_return_item
    return context  

@frappe.whitelist()
def return_list(web_item, return_date):
    rental_order = frappe.get_all('Rental Order', filters={'custom_tracking_id': web_item}, fields=['*'])

    if rental_order:
        return_item = frappe.new_doc('Rental Return')
        return_item.customer = rental_order[0]['customer']
        return_item.return_time = return_date
        rental_order_items = frappe.get_all('Rental Order Item', filters={'parent': rental_order[0]['name']}, fields=['*'])
        return_item.rental_order_reference = rental_order[0].name
        for order_item in rental_order_items:
            return_item.append('return_items', {
                'total_time': order_item['total_time'],
                'item_code': order_item['item_code'],
                'qty': order_item['qty'],
                'rate': order_item['rate'],
                'amount': order_item['amount'],
            })

            return_item.total = order_item['amount']

        assigned_customer = frappe.db.get_list('Employee',{'status':'active'},pluck='employee_name')
        if assigned_customer:
            return_item.custom_employee_check = random.choice(assigned_customer)
        frappe.db.set_value('Rental Item',web_item,'availability_status','Available')
        return_item.insert()
        
        return 'success'
