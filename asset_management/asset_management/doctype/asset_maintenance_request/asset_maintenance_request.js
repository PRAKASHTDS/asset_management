// Copyright (c) 2025, asset_management and contributors
// For license information, please see license.txt


frappe.ui.form.on("Asset Maintenance Request", {
    refresh: function (frm) {
        // Show button only after save and only to Maintenance Team Supervisor
        if (!frm.is_new() && frappe.user_roles.includes("Maintenance Team Supervisor")) {
            frm.add_custom_button(__('Create Maintenance Task'), function () {
                frappe.call({
                    method: "asset_management.asset_management.doctype.asset_maintenance_request.asset_maintenance_request.create_maintenance_task",
                    args: { docname: frm.doc.name },
                    freeze: true,
                    freeze_message: __("Creating Maintenance Task..."),
                    callback: function (r) {
                        if (!r.exc) {
                            frappe.msgprint({
                                message: __("Maintenance Task Created Successfully: ") + r.message,
                                title: __("Success"),
                                indicator: "green"
                            });
                            frm.reload_doc();
                        }
                    }
                });
            }).addClass("btn-primary");
        }
    }
});
