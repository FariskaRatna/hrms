import frappe

def get_employee_overtime(employee, start_date, end_date):
    return frappe.db.sql("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM `tabOvertime`
        WHERE employee = %s
          AND status = 'Approved'
          AND date BETWEEN %s AND %s
    """, (employee, start_date, end_date))[0][0] or 0.0

def add_overtime_to_salary_slip(doc, method):
    # safety checks
    if not (doc.employee and doc.start_date and doc.end_date):
        return

    overtime_total = get_employee_overtime(doc.employee, doc.start_date, doc.end_date)
    # simpan ke custom field Salary Slip
    doc.overtime_amount = overtime_total

    # ---- update earnings child table ----
    # hapus entri Overtime lama jika ada (untuk mencegah duplikat)
    for row in list(doc.get("earnings") or []):
        if row.salary_component == "Overtime":
            doc.remove(row)

    # jika ada nilai lembur, tambahkan baris earnings
    if overtime_total and hasattr(doc, "append"):
        row = doc.append("earnings", {})
        row.salary_component = "Overtime"
        row.amount = overtime_total
        # opsional: set other fields: row.abbr = "OVT" (jika perlu)
