import frappe

@frappe.whitelist()
def get_dashboard_data():
    """Return dashboard metrics for Maintenance Requests."""
    data = {}

    # Total Open Requests
    data["total_open"] = frappe.db.count("Asset Maintenance Request", {"status": "Open"})

    # Total Critical Requests
    data["total_critical"] = frappe.db.count("Asset Maintenance Request", {"priority": "Critical"})

    # Pie chart data (group by status)
    status_data = frappe.db.get_all(
        "Asset Maintenance Request",
        fields=["status", "count(name) as total"],
        group_by="status",
        order_by="total desc"
    )

    data["pie_chart"] = {
        "labels": [d.status for d in status_data],
        "values": [d.total for d in status_data]
    }

    return data
