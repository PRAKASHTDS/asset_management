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
