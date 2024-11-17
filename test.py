import mysql.connector

# 보안을 위해 제거 함
connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database="",
    port=1
)

cursor = connection.cursor()

# 데이터 삽입
try:
    insert_query = "INSERT INTO Book (BookID, BookName, Publisher, Price) VALUES (1234, 'SangJun Book', 'SangJun Park', 50000)"
    cursor.execute(insert_query)
    connection.commit()
    print("데이터 삽입")
except Exception as e:
    print("데이터 삽입 중 오류:", e)

# 데이터 검색
try:
    select_query = "SELECT * FROM Book"
    cursor.execute(select_query)
    results = cursor.fetchall()
    print("---")
    for row in results:
        print(row)
except Exception as e:
    print("데이터 검색 중 오류:", e)

# 데이터 삭제
try:
    delete_query = "DELETE FROM Book WHERE BookID = 1234"
    cursor.execute(delete_query)
    connection.commit()
    print("---")
    print("데이터 삭제")

    cursor.execute("SELECT * FROM Book")
    results = cursor.fetchall()
    for row in results:
        print(row)
except Exception as e:
    print("데이터 삭제 중 오류:", e)

# 연결 닫기
cursor.close()
connection.close()
