import frappe
from frappe import _

@frappe.whitelist()
def get_custom_data():
    return {"message":"Hello World"}
