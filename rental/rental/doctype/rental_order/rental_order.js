// Copyright (c) 2024, me and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Order', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Rental Order Item', {
	item_code: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];

        console.log("Item Code:", child.item_code);
		frappe.call({
            method: 'rental.rental.doctype.rental_order.rental_order.set_table',
            args: {
                item_code: child.item_code
            },
            callback: function (r) {
				console.log(r)
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, 'rate', r.message[0]);
                    frappe.model.set_value(cdt, cdn, 'total_time', r.message[1]);
					frappe.model.set_value(cdt, cdn, 'amount', r.message[0]);
					frm.set_value('total', r.message)
                }
            }
        });
        
    },
	total_time: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];

		frappe.call({
            method: 'rental.rental.doctype.rental_order.rental_order.set_amount',
            args: {
				item_code: child.item_code,
                qty: child.total_time
            },
            callback: function (r) {
				console.log(r)
                if (r.message) {
                   
                    frappe.model.set_value(cdt, cdn, 'amount', r.message);
					frm.set_value('total', r.message)
                }
            }
        });
        
    }
});

