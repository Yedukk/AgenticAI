import pymysql
import threading
import os

class DatabaseSingleton:
    _instance = None
    _lock = threading.Lock()  # Thread-safe singleton

    def __new__(cls, host, database, user, password, port=3306):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                cls._instance._connect(host, database, user, password, port)
        return cls._instance

    def _connect(self, host, database, user, password, port):
        """Establish a new database connection."""
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                cursorclass=pymysql.cursors.DictCursor,  # Return results as dictionaries
                autocommit=True  # Ensure immediate commit
            )
            self.cursor = self.connection.cursor()
            print("✅ Database connection established.")
        except pymysql.MySQLError as e:
            print(f"❌ Error connecting to database: {e}")
            self.connection = None
            self.cursor = None

    def _ensure_connection(self):
        """Check if the connection is alive, and reconnect if necessary."""
        try:
            if self.connection is None or not self.connection.open:
                print("🔄 Reconnecting to database...")
                self._connect(self.connection.host, self.connection.db, self.connection.user, self.connection.password, self.connection.port)
        except AttributeError:
            print("🔄 Reconnecting to database...")
            self._connect(self.connection.host, self.connection.db, self.connection.user, self.connection.password, self.connection.port)

    def execute_procedure(self, procedure_name, params=None):
        """
        Calls a stored procedure using a singleton cursor.
        """
        try:
            self._ensure_connection()  # Ensure connection is active before executing
            if params:
                self.cursor.callproc(procedure_name, params)
            else:
                self.cursor.callproc(procedure_name)

            return self.cursor.fetchall()  # Fetch all results

        except pymysql.MySQLError as e:
            print(f"❌ Error executing procedure {procedure_name}: {e}")
            return None

    def close(self):
        """Close the database connection"""
        if self.connection:
            try:
                self.cursor.close()
                self.connection.close()
                print("🔴 Database connection closed.")
            except pymysql.MySQLError as e:
                print(f"⚠️ Error closing connection: {e}")

db = DatabaseSingleton(
    host="joevirtualagent.database.windows.net",
    database="JoeDev",
    user="JoeDevUser@joevirtualagent",
    password="fw@GVg4#WSG@vds"
)

# Call a stored procedure
# results = db.execute_procedure("fetch_orders", (123,))

# print(results)  # Output example: [{'order_id': 123, 'status': 'Shipped'}]

# Close the connection when done
db.close()