# Copyright (c) 2025, asset_management and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AssetMaintenanceRequest(Document):
	pass
import frappe
from frappe.model.document import Document
from frappe import _

class AssetMaintenanceRequest(Document):

    def validate(self):
        self.validate_dates()
        self.validate_asset_status()
        self.validate_duplicate_request()

    def validate_dates(self):
        if self.maintenance_date and self.maintenance_date < self.request_date:
            frappe.throw(_("Maintenance Date cannot be before Request Date."))

    def validate_asset_status(self):
        asset_status = frappe.db.get_value("Asset", self.asset, "status")
        if asset_status in ["Scrapped", "Sold"]:
            frappe.throw(_("Cannot create maintenance request for a scrapped or sold asset."))

    def validate_duplicate_request(self):
        existing = frappe.db.exists(
            "Asset Maintenance Request",
            {
                "asset": self.asset,
                "status": ["in", ["Open", "In Progress"]],
                "name": ["!=", self.name]
            }
        )
        if existing:
            frappe.throw(_("There is already an active maintenance request for this asset."))

import frappe
from frappe.utils import get_datetime, time_diff_in_hours

def update_resolution_time(doc, method):
    """Triggered when Task is completed – updates the linked Asset Maintenance Request."""
    frappe.logger().info("=== update_resolution_time triggered ===")
    frappe.logger().info(f"Task: {doc.name}, Status: {doc.status}")

    # ✅ Use the correct field name for the linked AMR
    if doc.status == "Completed" and getattr(doc, "custom_asset_maintenance_request", None):
        amr_name = doc.custom_asset_maintenance_request
        frappe.logger().info(f"Linked AMR: {amr_name}")

        if amr_name:
            amr_doc = frappe.get_doc("Asset Maintenance Request", amr_name)

            frappe.logger().info(f"AMR Request Date: {amr_doc.request_date}")
            frappe.logger().info(f"Task Completion Date: {getattr(doc, 'custom_expected_completion_date', None)}")

            # ✅ Calculate time difference
            if amr_doc.request_date and doc.custom_expected_completion_date:
                request_dt = get_datetime(amr_doc.request_date)
                completion_dt = get_datetime(doc.custom_expected_completion_date)

                hours = time_diff_in_hours(completion_dt, request_dt)
                amr_doc.resolution_time_hours = round(hours, 2)
                frappe.logger().info(f"Calculated Resolution Time: {hours} hours")

            # ✅ Update AMR status
            amr_doc.status = "In Review"
            amr_doc.save(ignore_permissions=True)
            frappe.msgprint(f"Updated AMR {amr_doc.name} to 'In Review' with {amr_doc.resolution_time_hours} hrs")
    else:
        frappe.logger().info("Task not completed or no linked AMR.")
