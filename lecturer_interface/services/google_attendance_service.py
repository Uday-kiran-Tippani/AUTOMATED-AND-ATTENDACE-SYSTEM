# # services/google_attendance_service.py
# from datetime import datetime
# from config.google_sheets_config import init_gspread
# import gspread
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
#           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# EMAIL_ADDRESS = "your_email@gmail.com"
# EMAIL_PASSWORD = "your_app_password"  # Use Gmail App Password

# def mark_attendance_to_sheet(lecturer_email, class_name, present_rolls, students_master):
#     """
#     Marks attendance in Google Sheets and sends email.
#     Uses batch updates for speed.
#     """
#     client = init_gspread()
#     sheet_title = f"{lecturer_email}_{class_name}".replace("@", "_").replace(".", "_")
    
#     # Open or create spreadsheet
#     try:
#         sh = client.open(sheet_title)
#     except gspread.SpreadsheetNotFound:
#         sh = client.create(sheet_title)
#         sh.share(lecturer_email, perm_type='user', role='writer')

#     now = datetime.now()
#     month_name = MONTHS[now.month - 1]
#     date_str = now.strftime("%d-%m-%Y")

#     # Open or create month sheet
#     try:
#         worksheet = sh.worksheet(month_name)
#     except gspread.WorksheetNotFound:
#         worksheet = sh.add_worksheet(title=month_name, rows=str(len(students_master)+10), cols="50")
#         # Setup first 3 columns
#         worksheet.update("A1:C1", [["Roll Number", "Name", "Total Classes"]])
#         # Add students
#         students_data = [[s["roll"], s["name"]] for s in students_master]
#         worksheet.update(f"A2:B{len(students_data)+1}", students_data)

#     # Get current headers
#     all_values = worksheet.get_all_values()
#     headers = all_values[0]
    
#     if date_str in headers:
#         col_index = headers.index(date_str)
#     else:
#         col_index = len(headers)
#         worksheet.update_cell(1, col_index+1, date_str)

#     # --- Prepare batch values ---
#     student_rows = []
#     for i, s in enumerate(students_master, start=2):
#         roll = s["roll"]
#         student_row = all_values[i-1] if i-1 < len(all_values) else [""]* (col_index+1)
#         # Ensure row is long enough
#         while len(student_row) <= col_index:
#             student_row.append("")
#         student_row[col_index] = "Present" if roll in present_rolls else "Absent"
#         student_rows.append(student_row)

#     # Batch update
#     cell_range = f"A2:{chr(64 + len(student_rows[0]))}{len(student_rows)+1}"
#     worksheet.update(cell_range, student_rows)

#     # Update total classes and percentage
#     total_classes = col_index - 2  # excluding Roll, Name, Total Classes
#     percentage_updates = []
#     for i, row in enumerate(student_rows, start=2):
#         present_count = sum(1 for v in row[3:] if v == "Present")
#         row[2] = total_classes
#         percentage = round((present_count / total_classes) * 100, 2) if total_classes > 0 else 0
#         # Update percentage in column D (4th)
#         if len(row) < 4:
#             row.append(f"{percentage}%")
#         else:
#             row[3] = f"{percentage}%"
#         percentage_updates.append(row)

#     # Update all rows again including percentages
#     worksheet.update(cell_range, percentage_updates)

#     print(f"[INFO] Attendance marked for {len(present_rolls)} students on {date_str}.")

#     send_attendance_email(lecturer_email, class_name, present_rolls, students_master, sh.url)


# def send_attendance_email(to_email, class_name, present_rolls, students_master, sheet_url):
#     total = len(students_master)
#     present_count = len(present_rolls)
#     absent_count = total - present_count

#     subject = f"Attendance Update: {class_name} ({datetime.now().strftime('%d-%m-%Y')})"
#     body = f"""
#     Hello,

#     Attendance for class '{class_name}' has been marked.

#     Total Students   : {total}
#     Students Present : {present_count}
#     Students Absent  : {absent_count}

#     You can view the attendance sheet here:
#     {sheet_url}

#     Regards,
#     Attendance System
#     """

#     try:
#         msg = MIMEMultipart()
#         msg['From'] = EMAIL_ADDRESS
#         msg['To'] = to_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         server.send_message(msg)
#         server.quit()

#         print(f"[INFO] Attendance email sent to {to_email}")
#     except Exception as e:
#         print(f"[ERROR] Failed to send email: {e}")
