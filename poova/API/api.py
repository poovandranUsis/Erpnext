import frappe
from frappe import _

@frappe.whitelist()
def get_custom_data():
    return {"message":"Hello World"}

import frappe 
from frappe import _
#get API
@frappe.whitelist()
def firstapi():
    data = frappe.get_all("testingcal",fields=["name","title","startdate","end_date","jobtitle"])
    return {"status":"success","data":data}

#get API
@frappe.whitelist()
def createrecord():
    data = frappe.get_all("doc1",fields=["name","last_name","email"])
    return {"status":"success","data":data}

#POST API    
@frappe.whitelist()
def createname(doctype,data):
    data=frappe.parse_json(data)
    doc=frappe.get_doc({
        "doctype":doctype,
        **data
    })
    doc.insert()
    frappe.db.commit()
    return{"status":"success","message":"New Record Created","docname":doc.name}

#PUT API
@frappe.whitelist()
def update_value(doctype,docname,field,value):
    frappe.db.set_value(doctype,docname,field,value)
    frappe.db.commit()
    return{"status":"success","message":f"{field} updated for {docname}"}

#DELETE API
@frappe.whitelist()
def delete_value(doctype,docname):
       frappe.delete_doc(doctype,docname)
       frappe.db.commit()
       return {"status":"success","message":f"{docname} Deleted"}





@frappe.whitelist()
def get_testingcal_events():
    events = frappe.get_all("testingcal", fields=["name", "title", "startdate", "end_date", "jobtitle"])

    for event in events:
        # Fetch technicians
        technicians = frappe.get_all("Userchild", filters={"parent": event["name"]}, fields=["user"])
        technician_names = [frappe.db.get_value("User", tech["user"], "full_name") for tech in technicians]
        event["technicians"] = technician_names

        # Fetch vehicles
        vehicles = frappe.get_all("childdoc", filters={"parent": event["name"]}, fields=["vehicle"])
        vehicle_names = [frappe.db.get_value("Vehicles", vehi["vehicle"], "vehicle_name") for vehi in vehicles]
        event["vehicles"] = vehicle_names

        product_name = frappe.db.get_value("SalesPoc", {"name": event["title"]}, "product_name")

        # Set product_name as title, fallback to original title if not found
        event["product_name"] = product_name if product_name else event["title"]
        event["event_name"] = event["product_name"]  # Final title to be displayed

    return events

# @frappe.whitelist()
# def get_testingcal_events():
#     events = frappe.get_all("testingcal", fields=["name", "title", "startdate", "end_date", "jobtitle"])

#     for event in events:
#         # Fetch technicians
#         technicians = frappe.get_all("Userchild", filters={"parent": event.name}, fields=["user"])
#         event["technicians"] = [tech["user"] for tech in technicians]

#         # Fetch vehicles
#         vehicles = frappe.get_all("childdoc", filters={"parent": event.name}, fields=["vehicle"])
#         event["vehicles"] = [vehi["vehicle"] for vehi in vehicles]

#     return events
from datetime import datetime, timedelta

@frappe.whitelist()
def insert_testingcal_event(job_id, job_title, start_date):
    try:
        start_datetime = datetime.fromisoformat(start_date)  # Convert ISO string to datetime
        end_datetime = start_datetime + timedelta(hours=1)  # Add 1 hour

        # Create and insert new event
        doc = frappe.get_doc({
            "doctype": "testingcal",
            "title": job_id,
            "jobtitle": job_title,
            "startdate": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        })
        doc.insert()
        
        frappe.db.commit()  # Ensure changes are saved

        # Format time range for UI
        time_range = f"{start_datetime.strftime('%I:%M %p')} - {end_datetime.strftime('%I:%M %p')}"

        return {
            "name": doc.name,
            "jobtitle": doc.jobtitle,
            "time_range": time_range
        }

    except Exception as e:
        frappe.log_error(f"Error inserting event: {str(e)}")
        return {"error": str(e)}

# @frappe.whitelist()
# def get_role_testingcal_events(user_email=None):
#     events = frappe.get_all("testingcal", fields=["name", "title", "startdate", "end_date", "jobtitle"])

#     for event in events:
#         # Fetch technicians safely
#         technicians = frappe.get_all("Userchild", filters={"parent": event["name"]}, fields=["user"])
#         event["technicians"] = [tech["user"] for tech in technicians] if technicians else []

#         # Fetch vehicles safely
#         vehicles = frappe.get_all("childdoc", filters={"parent": event["name"]}, fields=["vehicle"])
#         event["vehicles"] = [vehi["vehicle"] for vehi in vehicles] if vehicles else []

#     return events

@frappe.whitelist()
def get_role_testingcal_events(user_email=None):
    if not user_email:
        return {"error": "user_email is required"}

    events = frappe.get_all("testingcal", fields=["name", "title", "startdate", "end_date", "jobtitle"])

    filtered_events = []

    for event in events:
        # Fetch technicians and get their emails
        technicians = frappe.get_all("Userchild", filters={"parent": event["name"]}, fields=["user"])
        technician_names = [frappe.db.get_value("User", tech["user"], "full_name") for tech in technicians]
        technician_emails = [frappe.db.get_value("User", tech["user"], "email") for tech in technicians]
        
        
        # Fetch vehicles
        vehicles = frappe.get_all("childdoc", filters={"parent": event["name"]}, fields=["vehicle"])
        vehicle_names = [frappe.db.get_value("Vehicles", vehi["vehicle"], "vehicle_name") for vehi in vehicles]
        
        # Fetch product name
        product_name = frappe.db.get_value("SalesPoc", {"name": event["title"]}, "product_name")

        # Set event properties
        event["technicians"] = technician_names
        event["vehicles"] = vehicle_names
        event["product_name"] = product_name if product_name else event["title"]
        event["event_name"] = event["product_name"]  # Final title

        # 🔥 **Filter events where the given `user_email` exists in `technician_emails`**
        if user_email in technician_emails:
            filtered_events.append(event)

    return filtered_events



@frappe.whitelist()
def get_event_details_by_id(event_id):
    if not event_id:
        return {"error": "event_id is required"}

    # Fetch the event by its ID
    event = frappe.get_all("testingcal", filters={"name": event_id}, fields=["name", "title", "startdate", "end_date", "jobtitle"])

    if not event:
        return {"error": f"Event with ID {event_id} not found"}

    event = event[0]  # Since get_all will return a list, we extract the first element

    # Fetch technicians and get their emails
    technicians = frappe.get_all("Userchild", filters={"parent": event["name"]}, fields=["user"])
    technician_names = [frappe.db.get_value("User", tech["user"], "full_name") for tech in technicians]
    technician_emails = [frappe.db.get_value("User", tech["user"], "email") for tech in technicians]

    # Fetch vehicles
    vehicles = frappe.get_all("childdoc", filters={"parent": event["name"]}, fields=["vehicle"])
    vehicle_names = [frappe.db.get_value("Vehicles", vehi["vehicle"], "vehicle_name") for vehi in vehicles]

    # Fetch product name
    product_name = frappe.db.get_value("SalesPoc", {"name": event["title"]}, "product_name")

    # Set event properties
    event["technicians"] = technician_names
    event["vehicles"] = vehicle_names
    event["product_name"] = product_name if product_name else event["title"]
    event["event_name"] = event["product_name"]  # Final title

    # Return the event details
    return event

