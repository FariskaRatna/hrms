# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class Overtime(Document):
    def before_save(self):
        if self.start_time and self.end_time:
            start = get_datetime(self.start_time)
            end = get_datetime(self.end_time)

            if end < start:
                frappe.throw("End Time cannot be before Start Time")

            # hitung selisih jam
            diff = (end - start).total_seconds() / 3600
            self.total_in_hours = round(diff, 2)
            self.total_amount = self.total_in_hours * 100000
        else:
            self.total_in_hours = 0
            self.total_amount = 0





