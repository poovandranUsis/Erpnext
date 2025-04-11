
//http://localhost:8081/api/method/frappe.poc.api.firstapi ---api worked inside module
//http://localhost:8081/api/method/frappe.poc.doctype.testingcal.testingcal.get_delivery_for_next_7_days --inside doctype
frappe.ui.form.on('testingcal', {
    setup(frm) {
        frm.fields_dict['title'].get_query = function () {
            return {
                filters: { status: "Accepted" },
                page_length: 100
            };
        };
    },

    refresh(frm) {
        // Hide sidebar
        frm.page.sidebar.hide();
        $(".form-sidebar").hide();

        // Avoid duplicate rendering
        if ($('#doc1-custom-layout').length) return;

        // Create custom layout
        const layout = `
            <div class="card mb-4" id="custom-card">
                <div class="card-body">
                    <h5 class="card-title" id="doc1-card-title">🧾 JOB Info ${frm.docname}</h5>
                    <div class="row" id="doc1-custom-layout"></div>
                </div>
            </div>
        `;

        // Insert layout before the first field (fallback to .frappe-control)
        const firstField = $(".frappe-control:first");
        if (firstField.length) {
            firstField.before(layout);
        } else {
            // fallback if no fields found
            frm.fields_area.prepend(layout);
        }

        // Style card and title
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
        const fields = ["title", "startdate","end_date", "jobtitle", "assigned", "vechicle", "enddate", "technicians", "vehicles"];

        fields.forEach(field => {
            const fieldWrapper = frm.fields_dict[field]?.$wrapper;
            if (!fieldWrapper) return;

            const $col = $(`<div class="col-md-6 mb-3"></div>`);
            $col.append(fieldWrapper);
            $("#doc1-custom-layout").append($col);

            // Style label
            fieldWrapper.find("label").css({
                "color": "black",
                "font-size": "larger"
            });

            // Style field container
            fieldWrapper.css({
                "background-color": "#f8f9fa",
                "border": "1px solid #ddd",
                "padding": "10px",
                "border-radius": "8px"
            });
        });

        // Move Save button into custom layout
        const $saveBtn = $('.page-actions .btn-primary:visible').detach();
        const $btnRow = $(`<div class="col-12 mt-3 text-end" id="custom-save-btn-row"></div>`);
        $btnRow.append($saveBtn);
        $("#doc1-custom-layout").append($btnRow);
    }
});

	
	