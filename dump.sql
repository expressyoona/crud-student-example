CREATE TABLE tbl_class(class_id INTEGER PRIMARY KEY, class_name TEXT NOT NULL);
CREATE TABLE tbl_student(student_id INTEGER PRIMARY KEY, student_name TEXT NOT NULL, student_address TEXT NOT NULL, class_id INTEGER);
