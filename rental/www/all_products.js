function get_details(item_name) {
    console.log("Button clicked!");
    
    // First dialog to get address details
    var addressDialog = new frappe.ui.Dialog({
        title: __('Shipping Address'),
        wrapper_class: 'dialog-scroll',
        fields: [
            {
                  label: __('Address Title'),
                  fieldname: 'address_title',
                  fieldtype: 'Data',
                  reqd: 1
                },
                {
                  label: __('Address Line 1'),
                  fieldname: 'address_line1',
                  fieldtype: 'Data',
                  reqd: 1
                },
                {
                  label: __('Address Line 2'),
                  fieldname: 'address_line2',
                  fieldtype: 'Data'
                },
                {
                  label: __('City/Town'),
                  fieldname: 'city',
                  fieldtype: 'Data',
                  reqd: 1
                },
                {
                  label: __('State'),
                  fieldname: 'state',
                  fieldtype: 'Data'
                },
                {
                  label: __('Country'),
                  fieldname: 'country',
                  fieldtype: 'Link',
                  options: 'Country',
                  only_select: true,
                  reqd: 1
                },
                {
                  fieldname: "column_break0",
                  fieldtype: "Column Break",
                  width: "50%"
                },
                {
                  label: __('Address Type'),
                  fieldname: 'address_type',
                  fieldtype: 'Select',
                  options: [
                    'Shipping'
                  ],
                  reqd: 1
                },
                {
                  label: __('Postal Code'),
                  fieldname: 'pincode',
                  fieldtype: 'Data'
                },
                {
                  fieldname: "phone",
                  fieldtype: "Data",
                  label: "Phone",
                  reqd: 1
                },
              ],
        primary_action_label: __('Save'),
        primary_action: function(values) {
            frappe.call({
                method: 'erpnext.e_commerce.shopping_cart.cart.add_new_address',
                args: { doc: values },
                callback: function(response) {
                    if (!response.exc) {
                        var address_name = response.message;

                        addressDialog.hide();

                        openDetailsDialog(item_name, address_name);
                    } else {
                        frappe.msgprint({
                            message: __("Error saving address: ") + response.exc,
                            title: __("Error"),
                            indicator: "red"
                        });
                    }
                }
            });
        }
    });

    addressDialog.show();
}

function openDetailsDialog(item_name, address_name) {
    // Second dialog to get details
    var detailsDialog = new frappe.ui.Dialog({
        title: __("Take Rent"),
        fields: [
            { fieldname: "total_hour", fieldtype: "Data", label: "Required Hour", reqd: 1 },
            { fieldname: "return_date", fieldtype: "Data", label: "Return Date", reqd: 1 },
        ],
        primary_action: function() {
            console.log("Submit button clicked!");
            var data = detailsDialog.get_values();
            frappe.call({
                method: "rental.www.all_products.create_rentalorder",
                args: {
                    web_item: item_name,
                    total_hour: data.total_hour,
                    return_date: data.return_date,
                    location: address_name.name
                },
                freeze: true,
                freeze_message: __("Submitting Review ..."),
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint({
                            message: __("Thank you for the review"),
                            title: __("Review Submitted"),
                            indicator: "green"
                        });
                        detailsDialog.hide();
                        location.reload();
                    }
                }
            });
        },
        primary_action_label: __('Submit')
    });

    detailsDialog.show();
}

function payments(item_name){
    frappe.call({
        method: "rental.www.all_products.payment",
        args:{
          'code':item_name
        },
        callback: function(r) {
                window.location.href = '/return_page'               
            }
        
    });
}