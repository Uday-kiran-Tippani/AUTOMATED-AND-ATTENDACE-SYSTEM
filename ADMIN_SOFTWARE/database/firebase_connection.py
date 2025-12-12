# import firebase_admin
# from firebase_admin import credentials, db

# # Path to your Firebase JSON credentials
# cred = credentials.Certificate("firebase_credentials.json")
# firebase_admin.initialize_app(cred, {
#     "databaseURL": "https://admin-software-ff838-default-rtdb.firebaseio.com/"
# })

# # -------------------------------
# # Sanitize any string to be a valid Firebase path
# def sanitize_key(name):
#     invalid_chars = ['.', '#', '$', '[', ']', ' ']
#     for char in invalid_chars:
#         name = name.replace(char, '_')
#     return name.strip().lower()
# # -------------------------------

# # Fetch all classes
# def get_classes():
#     ref = db.reference("classes")
#     classes = ref.get() or {}
#     # return dict mapping display_name → sanitized key_name
#     return {v['name']: sanitize_key(k) for k, v in classes.items()}

# # Add new class
# def add_class(class_name):
#     key_name = sanitize_key(class_name)
#     ref = db.reference("classes")
#     if ref.child(key_name).get():
#         raise Exception(f"Class '{class_name}' already exists")
#     ref.child(key_name).set({"name": class_name})

# # Delete class
# def delete_class(class_name):
#     key_name = sanitize_key(class_name)
#     ref = db.reference("classes")
#     ref.child(key_name).delete()

# # Add student with roll number as key
# def add_student(class_name, student_data):
#     roll_number = str(student_data['roll_number'])
#     key_class = sanitize_key(class_name)
#     ref = db.reference(f"students/{key_class}")
#     if ref.child(roll_number).get():
#         raise Exception(f"Roll number {roll_number} already exists in class '{class_name}'")
#     ref.child(roll_number).set(student_data)

# # Get students of a class
# def get_students(class_name):
#     key_class = sanitize_key(class_name)
#     ref = db.reference(f"students/{key_class}")
#     return ref.get() or {}

import firebase_admin
from firebase_admin import credentials, db

# Path to your Firebase JSON credentials
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://admin-software-ff838-default-rtdb.firebaseio.com/"
})

# -------------------------------
# Sanitize any string to be a valid Firebase path
def sanitize_key(name):
    invalid_chars = ['.', '#', '$', '[', ']', ' ']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip().lower()
# -------------------------------

# Fetch all classes
def get_classes():
    ref = db.reference("classes")
    classes = ref.get() or {}
    # return dict mapping display_name → actual Firebase key
    return {v['name']: k for k, v in classes.items()}

# Add new class
def add_class(class_name):
    key_name = sanitize_key(class_name)
    ref = db.reference("classes")
    if ref.child(key_name).get():
        raise Exception(f"Class '{class_name}' already exists")
    ref.child(key_name).set({"name": class_name})

# ✅ Delete class
def delete_class(key_name):
    """
    Deletes the class by its Firebase key.
    """
    ref = db.reference("classes")
    ref.child(key_name).delete()

    # Also delete its students if any
    db.reference(f"students/{key_name}").delete()

# Add student with roll number as key
def add_student(class_name, student_data):
    roll_number = str(student_data['roll_number'])
    key_class = sanitize_key(class_name)
    ref = db.reference(f"students/{key_class}")
    if ref.child(roll_number).get():
        raise Exception(f"Roll number {roll_number} already exists in class '{class_name}'")
    ref.child(roll_number).set(student_data)

# Get students of a class
def get_students(class_name):
    key_class = sanitize_key(class_name)
    ref = db.reference(f"students/{key_class}")
    return ref.get() or {}
