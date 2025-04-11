// Copyright (c) 2025, Frappe Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("SalesPoc", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("SalesPoc", {
	setup: function(frm) {
		frm.fields_dict.user.get_query = function() {
			return {
				filters: {
					"role_profile_name": "EnigneerPOC"
				},
				limit_page_length: 100
			};
		};
	},

	refresh: function (frm) {
		// Disable past dates for delivery_date
		frm.fields_dict.delivery_date.datepicker.update({
			minDate: new Date(frappe.datetime.get_today())
		});

		// Hide the sidebar
		frm.page.sidebar.hide();
		$(".form-sidebar").css({ "display": "none" });

		// Prevent re-rendering on multiple refresh
		if ($('#doc1-custom-layout').length) return;

		// Custom layout wrapper
		const layout = `
			<div class="card mb-4" id="custom-card">
				<div class="card-body">
					<h5 class="card-title" id="doc1-card-title">🧾 Basic Info ${frm.docname}</h5>
					<div class="row" id="doc1-custom-layout"></div>
				</div>
			</div>
		`;

		// ✅ Safe insert above the first field, scoped to this form only
		const firstField = frm.$wrapper.find(".frappe-control:first");
		if (firstField.length) {
			firstField.before(layout);
		} else {
			frm.$wrapper.find(".form-layout").prepend(layout); // fallback if no fields yet
		}

		// Style the custom card
		$("#custom-card").css({
			"background": "lightblue"
		});
		$("#doc1-card-title").css({
			"border-radius": "45%",
			"width": "fit-content",
			"background": "#ccc",
			"color": "black",
			"font-size": "large",
			"padding": "10px"
		});

		// Add and style fields
		const fields = [
			"product_name", "user", "number_of_product",
			"delivery_date", "cost", "priority",
			"status", "rejection_comments"
		];

		fields.forEach(field => {
			const fieldWrapper = frm.fields_dict[field]?.$wrapper;
			if (!fieldWrapper) return;

			const $col = $(`<div class="col-md-6 mb-3"></div>`);
			$col.append(fieldWrapper);
			$("#doc1-custom-layout").append($col);

			// Style the label
			fieldWrapper.find("label").css({
				"color": "black",
				"font-size": "larger"
			});

			// Style the field container
			fieldWrapper.css({
				"background-color": "#f8f9fa",
				"border": "1px solid #ddd",
				"padding": "10px",
				"border-radius": "8px"
			});
		});

		// Move Save button inside layout
		const $saveBtn = $('.page-actions .btn-primary:visible').detach();
		const $btnRow = $(`<div class="col-12 mt-3 text-end" id="custom-save-btn-row"></div>`);
		$btnRow.append($saveBtn);
		$("#doc1-custom-layout").append($btnRow);
	}
});



frappe.ui.form.on("SalesPoc", {
	workflow_state : function(frm) {  
        if (frm.doc.status === "Accepted") {			
            frappe.db.insert({
                doctype: "Event",
                subject: `Product ${frm.doc.product_name} Status changed to Accepted: ${frm.doc.name} by ${frm.doc.user}`,
                event_type: "Public",
                starts_on: frm.doc.delivery_date,
                owner: frm.doc.owner,
				status: "Open",
				color:"#b943f0"
            });
			frappe.db.insert({
				doctype: "CustomerPOC",
				user:frm.doc.user,
				product_name:frm.doc.product_name,
				number_of_product: frm.doc.number_of_product,
				owner: frm.doc.owner,
				delivery_date :frm.doc.delivery_date,
				priority: frm.doc.priority,
				cost: frm.doc.cost
		   });
	
        }
    }
});



