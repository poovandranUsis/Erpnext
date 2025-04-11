# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class SalesPoc(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cost: DF.Currency
		delivery_date: DF.Date
		name: DF.Int | None
		number_of_product: DF.Int
		priority: DF.Literal["1", "2", "3"]
		product_name: DF.Data
		rejection_comments: DF.SmallText | None
		status: DF.Data | None
		user: DF.Link | None
	# end: auto-generated types
	pass

