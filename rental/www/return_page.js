function return_items() {
    var button = event.target;
    var webItem = button.getAttribute("data-web-item");
    var detailsDialog = new frappe.ui.Dialog({
        title: __("Return Item"),
        fields: [
            { fieldname: "return_date", fieldtype: "Data", label: "Return Date", reqd: 1 },
        ],
        primary_action: function() {
            console.log("Submit button clicked!");
            var data = detailsDialog.get_values();
            frappe.call({
                method: "rental.www.return_page.return_list",
                args: {
                    web_item: webItem,
                    return_date: data.return_date,
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
