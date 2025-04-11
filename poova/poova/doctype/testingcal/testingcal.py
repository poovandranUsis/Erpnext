# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe          ?????????????????????????Help Dropdown??????????
from frappe.model.document import Document
import frappe
from datetime import date, timedelta
# import requests
# import json
# import logging
# import urllib3



class testingcal(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.poova.doctype.childdoc.childdoc import childdoc
		from frappe.poova.doctype.userchild.userchild import Userchild
		from frappe.types import DF

		assigned: DF.Link | None
		end_date: DF.Datetime | None
		jobtitle: DF.Data | None
		name: DF.Int | None
		startdate: DF.Datetime | None
		technicians: DF.TableMultiSelect[Userchild]
		title: DF.Link | None
		vechicle: DF.Link | None
		vehicles: DF.TableMultiSelect[childdoc]
	# end: auto-generated types
	pass

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# logging.basicConfig(level=logging.INFO)
# logger=logging.getLogger(__name__)
import frappe
from datetime import datetime, timedelta

# @frappe.whitelist(methods=['GET'])
@frappe.whitelist()
def get_delivery_for_next_7_days():
    # Date range
    start_date = datetime.utcnow().date()
    end_date = start_date + timedelta(days=6)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Frappe Doctype count
    delivery_count = frappe.db.count(
        "testingcal",
        filters={"startdate": ["between", [start_date_str, end_date_str]]}
    )

    # Call external API
    # external_response = send_data_to_external_service(
    #     "https://localhost:44359/api/CmsForgetPasswordPosts",  # ✅ fixed host
    #     {
    #         "OTP": "123456",
    #         "EmailId": "test@example.com",
    #         "Password": "testpass"
    #     },
    #     {
    #         "Content-Type": "application/json"
    #     }
    # )

    return {
        "status": "success",
        "count": delivery_count or 0,
        "start_date": start_date_str,
        "end_date": end_date_str,
        # "external_response": external_response,
    }

# def send_data_to_external_service(url, payload, headers):
#     try:
#         response = requests.post(
#             url,
#             headers=headers,
#             data=json.dumps(payload),
#             verify=False  # ✅ skip SSL verification for dev
#         )
#         response.raise_for_status()
#         logger.info("External API success: %s", response.json())
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         logger.error("External API error: %s", str(e))
#         return {"error": str(e)}


	