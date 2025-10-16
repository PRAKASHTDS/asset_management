frappe.pages['maintenance-dashboard'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Maintenance Dashboard',
        single_column: true
    });

    $(frappe.render_template("maintenance_dashboard", {})).appendTo(page.body);

    frappe.call({
        method: "asset_management.asset_management.page.maintenance_dashboard.maintenance_dashboard.get_dashboard_data",
        callback: function(r) {
            if (!r.message) return;
            const data = r.message;

            $("#total_open").text(data.total_open);
            $("#total_critical").text(data.total_critical);

            new frappe.Chart("#status_pie_chart", {
                title: "Requests by Status",
                data: {
                    labels: data.pie_chart.labels,
                    datasets: [{ values: data.pie_chart.values }]
                },
                type: 'pie',
                height: 250
            });
        }
    });
};
