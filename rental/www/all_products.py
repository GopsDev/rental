import frappe

def get_context(context):
    get_item = frappe.db.get_all('Rental Item',['*'])
    context.items = get_item

    return context

@frappe.whitelist()
def create_rentalorder(web_item,total_hour,return_date, location):
    customer = create_customer()
    create_order = frappe.new_doc('Rental Order')
    create_order.customer = customer
    create_order.valid_till = return_date
    create_order.location = location
    create_order.custom_tracking_id = web_item
    item1 = create_order.append('items', {})
    item1.item_code = web_item
    item1.qty = 1
    item1.total_time = total_hour
    item1.rate = frappe.db.get_value('Rental Item',{'item_name':web_item},['rental_price'])
    item1.amount = int(total_hour) * int(item1.rate)
    create_order.total = item1.amount
    item1.parent = create_order.name
    existing_rental_item = frappe.get_doc('Rental Item', {'name': web_item})
    frappe.db.set_value('Rental Item', existing_rental_item.name, 'availability_status', 'Reserved')
    create_order.insert()

def create_customer():
    existing_customer = frappe.get_all('Customer', filters={'customer_name': frappe.session.user})
    if existing_customer:
        return existing_customer[0]['name']
    else:
        customer = frappe.new_doc('Customer')
        customer.customer_name = frappe.session.user
        customer.customer_group = 'Individual'
        customer.territory = 'India'
        customer.save()
        return customer.name

@frappe.whitelist()
def payment(code):
    rental_order = frappe.get_all('Rental Order', filters={'custom_tracking_id': code}, limit=1)

    if rental_order:
        frappe.get_doc('Rental Order', rental_order[0].name).submit()
        existing_rental_item = frappe.get_doc('Rental Item', {'item_name': code})

        frappe.db.set_value('Rental Item', existing_rental_item.name, 'availability_status', 'Rented')

        return 'success'



    
