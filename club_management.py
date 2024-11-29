import mysql.connector
from mysql.connector import Error

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
            print("데이터베이스에 연결되었습니다.")
        return connection
    except Error as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None
    
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("데이터베이스 연결이 종료되었습니다.")


# 동아리원 관리 함수들
def view_members(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Member")
        rows = cursor.fetchall()
        print("\n=== 동아리원 전체 조회 ===")
        print("학번\t이름\t연락처\t이메일\t역할")
        for row in rows:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}")
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


def main():
    connection = create_connection()
    if not connection:
        return

    while True:
        print("\n=== 동아리 관리 프로그램 ===")
        print("1. 동아리원 관리")
        print("2. 종료")
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
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

    close_connection(connection)

if __name__ == "__main__":
    main()
