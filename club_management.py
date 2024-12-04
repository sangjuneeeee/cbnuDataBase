import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database="",
            port=1234
        )
        if connection.is_connected():
            print("동아리 관리 프로그램에 연결되었습니다.")
        return connection
    except Error as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("동아리 관리 프로그램이 종료되었습니다.")

# 동아리원 관리 함수들
def view_members(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Member")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 동아리원 전체 조회 ===")
        headers = ["학번", "이름", "연락처", "이메일", "역할"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_member(connection):
    try:
        student_id = int(input("학번: "))
        name = input("이름: ")
        contact = input("연락처: ")
        email = input("이메일: ")
        role_name = input("역할명: ")

        cursor = connection.cursor()
        sql = "INSERT INTO Member (Student_ID, Name, Contact, Email, Role_Name) VALUES (%s, %s, %s, %s, %s)"
        val = (student_id, name, contact, email, role_name)
        cursor.execute(sql, val)
        connection.commit()
        print(f"{cursor.rowcount}개의 레코드가 추가되었습니다.")
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("학번은 숫자여야 합니다.")

def update_member(connection):
    try:
        student_id = int(input("수정할 회원의 학번: "))
        print("수정할 항목을 선택하세요:")
        print("1. 이름")
        print("2. 연락처")
        print("3. 이메일")
        print("4. 역할명")
        choice = input("선택: ")

        cursor = connection.cursor()
        if choice == '1':
            name = input("새로운 이름: ")
            sql = "UPDATE Member SET Name = %s WHERE Student_ID = %s"
            val = (name, student_id)
        elif choice == '2':
            contact = input("새로운 연락처: ")
            sql = "UPDATE Member SET Contact = %s WHERE Student_ID = %s"
            val = (contact, student_id)
        elif choice == '3':
            email = input("새로운 이메일: ")
            sql = "UPDATE Member SET Email = %s WHERE Student_ID = %s"
            val = (email, student_id)
        elif choice == '4':
            role_name = input("새로운 역할명: ")
            sql = "UPDATE Member SET Role_Name = %s WHERE Student_ID = %s"
            val = (role_name, student_id)
        else:
            print("잘못된 선택입니다.")
            return

        cursor.execute(sql, val)
        connection.commit()
        print(f"{cursor.rowcount}개의 레코드가 수정되었습니다.")
    except Error as e:
        print(f"데이터 수정 실패: {e}")
    except ValueError:
        print("학번은 숫자여야 합니다.")

def delete_member(connection):
    try:
        student_id = int(input("삭제할 회원의 학번: "))
        cursor = connection.cursor()
        sql = "DELETE FROM Member WHERE Student_ID = %s"
        val = (student_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount}개의 레코드가 삭제되었습니다.")
        else:
            print("해당 학번의 회원이 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("학번은 숫자여야 합니다.")

# 역할 관리 함수들
def view_roles(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Role")
        rows = cursor.fetchall()
        rows = [[str(item).strip() for item in row] for row in rows]

        print("\n=== 역할 전체 조회 ===")
        headers = ["역할명"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_role(connection):
    try:
        role_name = input("추가할 역할명: ")

        cursor = connection.cursor()
        sql = "INSERT INTO Role (Role_Name) VALUES (%s)"
        val = (role_name,)
        cursor.execute(sql, val)
        connection.commit()
        print(f"{cursor.rowcount}개의 레코드가 추가되었습니다.")
    except Error as e:
        print(f"데이터 추가 실패: {e}")

def delete_role(connection):
    try:
        role_name = input("삭제할 역할명: ")
        cursor = connection.cursor()
        sql = "DELETE FROM Role WHERE Role_Name = %s"
        val = (role_name,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount}개의 레코드가 삭제되었습니다.")
        else:
            print("해당 역할명이 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")

# 회비 납부 관리 함수들
def view_fee_payments(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM FeePayment")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 회비 납부 내역 조회 ===")
        headers = ["납부ID", "학번", "납부일", "금액"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_fee_payment(connection):
    try:
        student_id = int(input("학번: "))
        payment_date = input("납부일 (YYYY-MM-DD): ")
        amount = float(input("금액: "))

        cursor = connection.cursor()
        sql = "INSERT INTO FeePayment (Student_ID, Payment_Date, Amount) VALUES (%s, %s, %s)"
        val = (student_id, payment_date, amount)
        cursor.execute(sql, val)
        connection.commit()
        print("회비 납부 내역이 추가되었습니다. 납부ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_fee_payment(connection):
    try:
        payment_id = int(input("삭제할 납부ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM FeePayment WHERE Payment_ID = %s"
        val = (payment_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount}개의 레코드가 삭제되었습니다.")
        else:
            print("해당 납부ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("납부ID는 숫자여야 합니다.")

# 스터디 세션 관리 함수들
def view_study_sessions(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM StudySession")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 스터디 세션 조회 ===")
        headers = ["스터디ID", "주제", "장소", "일정"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_study_session(connection):
    try:
        topic = input("주제: ")
        location = input("장소: ")
        date = input("일정 (YYYY-MM-DD): ")

        cursor = connection.cursor()
        sql = "INSERT INTO StudySession (Topic, Location, Date) VALUES (%s, %s, %s)"
        val = (topic, location, date)
        cursor.execute(sql, val)
        connection.commit()
        print("스터디 세션이 추가되었습니다. 스터디ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")

def delete_study_session(connection):
    try:
        study_id = int(input("삭제할 스터디ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM StudySession WHERE Study_ID = %s"
        val = (study_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount}개의 레코드가 삭제되었습니다.")
        else:
            print("해당 스터디ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("스터디ID는 숫자여야 합니다.")

# 스터디 참석 관리 함수들
def view_study_attendance(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM StudyAttendance")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 스터디 참석 내역 조회 ===")
        headers = ["스터디ID", "학번", "상태"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_study_attendance(connection):
    try:
        study_id = int(input("스터디ID: "))
        student_id = int(input("학번: "))
        status = input("상태 (참석/불참): ")

        cursor = connection.cursor()
        sql = "INSERT INTO StudyAttendance (Study_ID, Student_ID, Status) VALUES (%s, %s, %s)"
        val = (study_id, student_id, status)
        cursor.execute(sql, val)
        connection.commit()
        print("스터디 참석 내역이 추가되었습니다.")
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_study_attendance(connection):
    try:
        study_id = int(input("스터디ID: "))
        student_id = int(input("학번: "))
        cursor = connection.cursor()
        sql = "DELETE FROM StudyAttendance WHERE Study_ID = %s AND Student_ID = %s"
        val = (study_id, student_id)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("스터디 참석 기록이 삭제되었습니다.")
        else:
            print("해당 기록이 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

# 이벤트 관리 함수들
def view_events(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Event")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 이벤트 조회 ===")
        headers = ["이벤트ID", "이름", "일시", "장소", "담당자 학번"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_event(connection):
    try:
        name = input("이름: ")
        date_time = input("일시 (YYYY-MM-DD HH:MM:SS): ")
        location = input("장소: ")
        manager_id = int(input("담당자 학번: "))

        cursor = connection.cursor()
        sql = "INSERT INTO Event (Name, Date_Time, Location, Manager_ID) VALUES (%s, %s, %s, %s)"
        val = (name, date_time, location, manager_id)
        cursor.execute(sql, val)
        connection.commit()
        print("이벤트가 추가되었습니다. 이벤트ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_event(connection):
    try:
        event_id = int(input("삭제할 이벤트ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM Event WHERE Event_ID = %s"
        val = (event_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount}개의 레코드가 삭제되었습니다.")
        else:
            print("해당 이벤트ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("이벤트ID는 숫자여야 합니다.")

# 이벤트 참석 관리 함수들
def view_event_attendance(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM EventAttendance")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 이벤트 참석 내역 조회 ===")
        headers = ["이벤트ID", "학번", "상태"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_event_attendance(connection):
    try:
        event_id = int(input("이벤트ID: "))
        student_id = int(input("학번: "))
        status = input("상태 (참석/불참): ")

        cursor = connection.cursor()
        sql = "INSERT INTO EventAttendance (Event_ID, Student_ID, Status) VALUES (%s, %s, %s)"
        val = (event_id, student_id, status)
        cursor.execute(sql, val)
        connection.commit()
        print("이벤트 참석 내역이 추가되었습니다.")
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_event_attendance(connection):
    try:
        event_id = int(input("이벤트ID: "))
        student_id = int(input("학번: "))
        cursor = connection.cursor()
        sql = "DELETE FROM EventAttendance WHERE Event_ID = %s AND Student_ID = %s"
        val = (event_id, student_id)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("이벤트 참석 기록이 삭제되었습니다.")
        else:
            print("해당 기록이 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

# 공지사항 관리 함수들
def view_notices(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Notice")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 공지사항 조회 ===")
        headers = ["공지ID", "제목", "내용", "작성일"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_notice(connection):
    try:
        title = input("제목: ")
        content = input("내용: ")
        date = input("작성일 (YYYY-MM-DD): ")

        cursor = connection.cursor()
        sql = "INSERT INTO Notice (Title, Content, Date) VALUES (%s, %s, %s)"
        val = (title, content, date)
        cursor.execute(sql, val)
        connection.commit()
        print("공지사항이 추가되었습니다. 공지ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")

def delete_notice(connection):
    try:
        notice_id = int(input("삭제할 공지ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM Notice WHERE Notice_ID = %s"
        val = (notice_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print(f"{cursor.rowcount}개의 레코드가 삭제되었습니다.")
        else:
            print("해당 공지ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("공지ID는 숫자여야 합니다.")

# 자료 관리 함수들
def view_materials(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Material")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 자료 조회 ===")
        headers = ["자료ID", "자료명", "유형", "업로드일", "파일 경로"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_material(connection):
    try:
        name = input("자료명: ")
        type_ = input("유형: ")
        upload_date = input("업로드일 (YYYY-MM-DD): ")
        file_path = input("파일 경로 또는 URL: ")

        cursor = connection.cursor()
        sql = "INSERT INTO Material (Name, Type, Upload_Date, File_Path) VALUES (%s, %s, %s, %s)"
        val = (name, type_, upload_date, file_path)
        cursor.execute(sql, val)
        connection.commit()
        print("자료가 추가되었습니다. 자료ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")

def delete_material(connection):
    try:
        material_id = int(input("삭제할 자료ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM Material WHERE Material_ID = %s"
        val = (material_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("자료가 삭제되었습니다.")
        else:
            print("해당 자료ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("자료ID는 숫자여야 합니다.")

# 예산 관리 함수들
def view_budgets(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Budget")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 예산 조회 ===")
        headers = ["예산ID", "항목", "금액", "사용일"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_budget(connection):
    try:
        item = input("항목: ")
        amount = float(input("금액: "))
        date = input("사용일 (YYYY-MM-DD): ")

        cursor = connection.cursor()
        sql = "INSERT INTO Budget (Item, Amount, Date) VALUES (%s, %s, %s)"
        val = (item, amount, date)
        cursor.execute(sql, val)
        connection.commit()
        print("예산 항목이 추가되었습니다. 예산ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_budget(connection):
    try:
        budget_id = int(input("삭제할 예산ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM Budget WHERE Budget_ID = %s"
        val = (budget_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("예산 항목이 삭제되었습니다.")
        else:
            print("해당 예산ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("예산ID는 숫자여야 합니다.")

# 예산 관리 기록 관리 함수들
def view_budget_management(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BudgetManagement")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 예산 관리 기록 조회 ===")
        headers = ["예산ID", "학번"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_budget_management(connection):
    try:
        budget_id = int(input("예산ID: "))
        student_id = int(input("학번: "))

        cursor = connection.cursor()
        sql = "INSERT INTO BudgetManagement (Budget_ID, Student_ID) VALUES (%s, %s)"
        val = (budget_id, student_id)
        cursor.execute(sql, val)
        connection.commit()
        print("예산 관리 기록이 추가되었습니다.")
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_budget_management(connection):
    try:
        budget_id = int(input("예산ID: "))
        student_id = int(input("학번: "))
        cursor = connection.cursor()
        sql = "DELETE FROM BudgetManagement WHERE Budget_ID = %s AND Student_ID = %s"
        val = (budget_id, student_id)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("예산 관리 기록이 삭제되었습니다.")
        else:
            print("해당 기록이 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

# 리포트 관리 함수들
def view_reports(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Report")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 리포트 조회 ===")
        headers = ["리포트ID", "유형", "생성일", "내용"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_report(connection):
    try:
        type_ = input("유형: ")
        date = input("생성일 (YYYY-MM-DD): ")
        content = input("내용: ")

        cursor = connection.cursor()
        sql = "INSERT INTO Report (Type, Date, Content) VALUES (%s, %s, %s)"
        val = (type_, date, content)
        cursor.execute(sql, val)
        connection.commit()
        print("리포트가 추가되었습니다. 리포트ID:", cursor.lastrowid)
    except Error as e:
        print(f"데이터 추가 실패: {e}")

def delete_report(connection):
    try:
        report_id = int(input("삭제할 리포트ID: "))
        cursor = connection.cursor()
        sql = "DELETE FROM Report WHERE Report_ID = %s"
        val = (report_id,)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("리포트가 삭제되었습니다.")
        else:
            print("해당 리포트ID가 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("리포트ID는 숫자여야 합니다.")

# 리포트 생성 관리 함수들
def view_report_generation(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ReportGeneration")
        rows = cursor.fetchall()
        rows = [[str(item).strip() if item is not None else '' for item in row] for row in rows]

        print("\n=== 리포트 생성 내역 조회 ===")
        headers = ["리포트ID", "학번"]
        print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
    except Error as e:
        print(f"데이터 조회 실패: {e}")

def add_report_generation(connection):
    try:
        report_id = int(input("리포트ID: "))
        student_id = int(input("학번: "))

        cursor = connection.cursor()
        sql = "INSERT INTO ReportGeneration (Report_ID, Student_ID) VALUES (%s, %s)"
        val = (report_id, student_id)
        cursor.execute(sql, val)
        connection.commit()
        print("리포트 생성 기록이 추가되었습니다.")
    except Error as e:
        print(f"데이터 추가 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

def delete_report_generation(connection):
    try:
        report_id = int(input("리포트ID: "))
        student_id = int(input("학번: "))
        cursor = connection.cursor()
        sql = "DELETE FROM ReportGeneration WHERE Report_ID = %s AND Student_ID = %s"
        val = (report_id, student_id)
        cursor.execute(sql, val)
        connection.commit()
        if cursor.rowcount > 0:
            print("리포트 생성 기록이 삭제되었습니다.")
        else:
            print("해당 기록이 없습니다.")
    except Error as e:
        print(f"데이터 삭제 실패: {e}")
    except ValueError:
        print("입력 값의 형식이 올바르지 않습니다.")

# 회원 상세 정보 조회
def view_member_details(connection):
    try:
        student_id = int(input("조회할 회원의 학번: "))
        cursor = connection.cursor()

        # MemberDetailView에서 회원 정보 조회
        sql = "SELECT * FROM MemberDetailView WHERE Student_ID = %s"
        cursor.execute(sql, (student_id,))
        row = cursor.fetchone()

        if row:
            headers = ["학번", "이름", "연락처", "이메일", "역할"]
            print("\n=== 회원 상세 정보 ===")
            print(tabulate([row], headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("해당 학번의 회원이 없습니다.")
    except Error as e:
        print(f"데이터 조회 실패: {e}")
    except ValueError:
        print("학번은 숫자여야 합니다.")

# 회원 회비 납부 내역 조회
def view_member_fee_payments(connection):
    try:
        student_id = int(input("회비 내역을 조회할 회원의 학번: "))
        cursor = connection.cursor()

        # FeePaymentView에서 회비 납부 내역 조회
        sql = "SELECT Payment_ID, Payment_Date, Amount FROM FeePaymentView WHERE Student_ID = %s"
        cursor.execute(sql, (student_id,))
        rows = cursor.fetchall()

        if rows:
            headers = ["납부ID", "납부일", "금액"]
            print("\n=== 회원 회비 납부 내역 ===")
            print(tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("해당 회원의 회비 납부 내역이 없습니다.")
    except Error as e:
        print(f"데이터 조회 실패: {e}")
    except ValueError:
        print("학번은 숫자여야 합니다.")

# 회원 활동 내역 조회
def view_member_activities(connection):
    try:
        student_id = int(input("활동 내역을 조회할 회원의 학번: "))
        cursor = connection.cursor()

        # 스터디 참석 내역 조회
        sql_study = "SELECT Study_ID, Topic, Date, Status FROM StudyAttendanceView WHERE Student_ID = %s"
        cursor.execute(sql_study, (student_id,))
        study_rows = cursor.fetchall()

        # 이벤트 참석 내역 조회
        sql_event = "SELECT Event_ID, Event_Name, Date_Time, Status FROM EventAttendanceView WHERE Student_ID = %s"
        cursor.execute(sql_event, (student_id,))
        event_rows = cursor.fetchall()

        if study_rows:
            headers = ["스터디ID", "주제", "일정", "상태"]
            print("\n=== 회원 스터디 참석 내역 ===")
            print(tabulate(study_rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("\n해당 회원의 스터디 참석 내역이 없습니다.")

        if event_rows:
            headers = ["이벤트ID", "이벤트명", "일시", "상태"]
            print("\n=== 회원 이벤트 참석 내역 ===")
            print(tabulate(event_rows, headers=headers, tablefmt="grid", numalign="center", stralign="center"))
        else:
            print("\n해당 회원의 이벤트 참석 내역이 없습니다.")

    except Error as e:
        print(f"데이터 조회 실패: {e}")
    except ValueError:
        print("학번은 숫자여야 합니다.")

def main():
    connection = create_connection()
    if not connection:
        return

    while True:
        print("\n=== 동아리 관리 프로그램 ===")
        print("1. 동아리원 관리")
        print("2. 역할 관리")
        print("3. 회비 납부 관리")
        print("4. 스터디 세션 관리")
        print("5. 스터디 참석 관리")
        print("6. 이벤트 관리")
        print("7. 이벤트 참석 관리")
        print("8. 공지사항 관리")
        print("9. 자료 관리")
        print("10. 예산 관리")
        print("11. 예산 관리 기록 관리")
        print("12. 리포트 관리")
        print("13. 리포트 생성 관리")
        print("14. 회원 상세 정보 조회")  # 새로운 기능 추가
        print("15. 회원 회비 납부 내역 조회")  # 새로운 기능 추가
        print("16. 회원 활동 내역 조회")  # 새로운 기능 추가
        print("17. 종료")
        choice = input("선택: ")

        if choice == '1':
            while True:
                print("\n=== 동아리원 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 수정")
                print("4. 삭제")
                print("5. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_members(connection)
                elif sub_choice == '2':
                    add_member(connection)
                elif sub_choice == '3':
                    update_member(connection)
                elif sub_choice == '4':
                    delete_member(connection)
                elif sub_choice == '5':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '2':
            while True:
                print("\n=== 역할 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_roles(connection)
                elif sub_choice == '2':
                    add_role(connection)
                elif sub_choice == '3':
                    delete_role(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '3':
            while True:
                print("\n=== 회비 납부 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_fee_payments(connection)
                elif sub_choice == '2':
                    add_fee_payment(connection)
                elif sub_choice == '3':
                    delete_fee_payment(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '4':
            while True:
                print("\n=== 스터디 세션 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_study_sessions(connection)
                elif sub_choice == '2':
                    add_study_session(connection)
                elif sub_choice == '3':
                    delete_study_session(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '5':
            while True:
                print("\n=== 스터디 참석 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_study_attendance(connection)
                elif sub_choice == '2':
                    add_study_attendance(connection)
                elif sub_choice == '3':
                    delete_study_attendance(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '6':
            while True:
                print("\n=== 이벤트 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_events(connection)
                elif sub_choice == '2':
                    add_event(connection)
                elif sub_choice == '3':
                    delete_event(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '7':
            while True:
                print("\n=== 이벤트 참석 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_event_attendance(connection)
                elif sub_choice == '2':
                    add_event_attendance(connection)
                elif sub_choice == '3':
                    delete_event_attendance(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '8':
            while True:
                print("\n=== 공지사항 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_notices(connection)
                elif sub_choice == '2':
                    add_notice(connection)
                elif sub_choice == '3':
                    delete_notice(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '9':
            while True:
                print("\n=== 자료 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_materials(connection)
                elif sub_choice == '2':
                    add_material(connection)
                elif sub_choice == '3':
                    delete_material(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '10':
            while True:
                print("\n=== 예산 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_budgets(connection)
                elif sub_choice == '2':
                    add_budget(connection)
                elif sub_choice == '3':
                    delete_budget(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '11':
            while True:
                print("\n=== 예산 관리 기록 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_budget_management(connection)
                elif sub_choice == '2':
                    add_budget_management(connection)
                elif sub_choice == '3':
                    delete_budget_management(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '12':
            while True:
                print("\n=== 리포트 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_reports(connection)
                elif sub_choice == '2':
                    add_report(connection)
                elif sub_choice == '3':
                    delete_report(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '13':
            while True:
                print("\n=== 리포트 생성 관리 ===")
                print("1. 전체 조회")
                print("2. 추가")
                print("3. 삭제")
                print("4. 뒤로가기")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    view_report_generation(connection)
                elif sub_choice == '2':
                    add_report_generation(connection)
                elif sub_choice == '3':
                    delete_report_generation(connection)
                elif sub_choice == '4':
                    break
                else:
                    print("잘못된 선택입니다.")

        elif choice == '14':
            view_member_details(connection)

        elif choice == '15':
            view_member_fee_payments(connection)

        elif choice == '16':
            view_member_activities(connection)

        elif choice == '17':
            break

        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

    close_connection(connection)

if __name__ == "__main__":
    main()
