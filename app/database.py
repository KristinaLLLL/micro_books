from mysql.connector import Error
import MySQLdb


# def show(cur):
#      try:
#          cur.execute("SELECT * FROM book")
#          print("Query sent successfully!")
#          for row in cur.fetchall():
#              print(row[0])
#          #db.close()
#      except Error as e:
#          print(f"The error '{e}' occurred")


class Database:

    def __init__(self, id: int, title: str, body: str) -> None:
        #self.show = None
        try:
            db = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='121133',
                db="micro"
            )

            print("Connection to MySQL DB successful!")
        except Error as e:
            print(f"The error '{e}' occurred")

        cur = db.cursor()
        try:
            cur.execute(f"""INSERT INTO `book` (`id`, `title`, `body`) VALUE ({id}, '{title}', '{body}');""")
            db.commit()

            #self.show = cur.execute("SELECT * FROM book")

            db.close()
            print("Query sent successfully!")
        except Error as e:
            print(f"The error '{e}' occurred")
