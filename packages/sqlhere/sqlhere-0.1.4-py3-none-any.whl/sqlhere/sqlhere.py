import os
import sqlite3

class DataAdderDB:
    def __init__(self, db_path, table_name):
        """
        Initializes the DataAdderDB class.

        Args:
            db_path (str): Path to the SQLite database file.
            table_name (str): Name of the table in the database.
        """
        self.db_path = db_path
        self.table_name = table_name

    def verify_db(self):
        """
        Checks if the database file exists. If not, it creates the database file.
        """
        if not os.path.exists(self.db_path):
            print(f"Creating database file: {self.db_path}")
            open(self.db_path, 'w').close()

    def _connect_db(self):
        """
        Connects to the SQLite database.
        """
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def _disconnect_db(self):
        """
        Disconnects from the SQLite database.
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def load_data(self, data, description=''):
        """
        Add data into the specified table in the database.

        Args:
            data (set): Set of data to be added.
            description (str, optional): Description of the data source.
        """
        self._connect_db()
        self._add_data_to_db(data, description)
        self._disconnect_db()

    def _add_data_to_db(self, data, description=''):
        """
        Adds unique data to the SQLite database table.

        Args:
            data (set): Set of unique items to be added to the table.
            description (str): Description of the data source.
        """
        if self.table_name:
            # Create the table if it doesn't exist
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match TEXT UNIQUE,
                    description TEXT
                )
            ''')

            max_id = self.cursor.execute(f'SELECT MAX(id) FROM {self.table_name}').fetchone()[0] or 0

            counter = 0
            temp = set()

            try:
                for i, value in enumerate(data, start=max_id + 1):
                    value_data = '.'.join(value.strip().split('.')[1:-1])
                    if 0 < len(value_data.strip()) < 15 and value_data not in temp:
                        self.cursor.execute(
                            f'INSERT OR IGNORE INTO {self.table_name} (match, description) VALUES (?, ?)',
                            (value_data, description)
                        )
                        temp.add(value_data)
                        counter += 1

                self.connection.commit()

                self.cursor.execute(f'PRAGMA table_info({self.table_name})')
                table_info = self.cursor.fetchall()
                print(f"Table Information - {self.table_name}:")
                for column_info in table_info:
                    print(column_info)

                print(f'Appended {counter} unique records from {description}')

            except sqlite3.Error as e:
                print(f"Error: {e}")

    def retrieve_data(self, other_table_name=None):
        """
        Retrieves all data from the specified table as a set.

        Returns:
            Set of data retrieved from the table.
        """
        if other_table_name:
            table=other_table_name
        else:
            table=self.table_name
        try:
            self._connect_db()
            self.cursor.execute(f"SELECT * FROM {table}")
            data = [item for item in self.cursor.fetchall()]
            self._disconnect_db()
            return data
        except Exception as e:
            print("Errors: ",e)

    def delete_data(self, other_table_name=None):
        """
        Moves all data from the specified table to the recycle bin and then deletes the table.

        Args:
            other_table_name (str, optional): Name of the table to delete. If None, uses the default table name.
        """
        if other_table_name:
            table = other_table_name
        else:
            table = self.table_name
        try:
            # Move the table to the recycle bin
            self.recycle_bin(table)

            # Now delete the table
            self._connect_db()
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Deleted table {table} from {self.db_path}")
            self._disconnect_db()

        except Exception as e:
            print("Error:", e)
            
    def query(self, q):
        """
        Executes the provided SQL query and returns the results.

        Args:
            q (str): String containing the SQL query to execute.

        Returns:
            List of tuples containing the query results.
        
        self._connect_db()
        
        --------------------------------------------------

        ### Example 1: Select (Retrieve) Data
        select_query = "SELECT * FROM your_table_name;"
        self.cursor.execute(select_query)
        select_results = self.cursor.fetchall()

        ### Example 2: Insert Data
        insert_query = "INSERT INTO your_table_name (column1, column2) VALUES ('value1', 'value2');"
        self.cursor.execute(insert_query)
        #### Commit the changes to the database
        self.connection.commit()

        ### Example 3: Update Data
        update_query = "UPDATE your_table_name SET column1 = 'new_value' WHERE condition;"
        self.cursor.execute(update_query)
        #### Commit the changes to the database
        self.connection.commit()

        ### Example 4: Delete Data
        delete_query = "DELETE FROM your_table_name WHERE condition;"
        self.cursor.execute(delete_query)

        --------------------------------------------------

        ### Commit the changes to the database
        self.connection.commit()
        """

        # Execute the provided query
        self.cursor.execute(q)
        results = self.cursor.fetchall()

        self._disconnect_db()
        return results

    def recycle_bin(self, deleted_table_name):
        """
        Moves the specified table to the recycle bin database.

        Args:
            deleted_table_name (str): Name of the table to be moved to the recycle bin.
        """
        recycle_bin_db_path = 'recycle_bin.db'
        recycle_bin_table_name = 'deleted_tables'

        # Connect to the recycle bin database
        recycle_bin_connection = sqlite3.connect(recycle_bin_db_path)
        recycle_bin_cursor = recycle_bin_connection.cursor()

        # Create the recycle bin database and table if not present
        recycle_bin_cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {recycle_bin_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        try:
            # Move the deleted table to the recycle bin
            self._connect_db()
            self.cursor.execute(f"ATTACH DATABASE '{recycle_bin_db_path}' AS recycle_bin_db")
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS recycle_bin_db.{recycle_bin_table_name} AS SELECT * FROM {deleted_table_name}")
            self.cursor.execute(f"DETACH DATABASE recycle_bin_db")

            # Record the deleted table in the recycle bin table
            recycle_bin_cursor.execute(
                f'INSERT INTO {recycle_bin_table_name} (table_name) VALUES (?)',
                (deleted_table_name,)
            )
            recycle_bin_connection.commit()

            print(f"Moved {deleted_table_name} to the recycle bin.")

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            self._disconnect_db()
            recycle_bin_connection.close()

    def undo_delete(self, target_db_path, target_table_name):
        """
        Retrieves a table from the recycle bin and inserts it into the specified database.

        Args:
            target_db_path (str): Path to the target database.
            target_table_name (str): Name of the table in the target database.
        """
        recycle_bin_db_path = 'recycle_bin.db'
        recycle_bin_table_name = 'deleted_tables'
        try:
            # Connect to the recycle bin database
            recycle_bin_connection = sqlite3.connect(recycle_bin_db_path)
            recycle_bin_cursor = recycle_bin_connection.cursor()

            # Check if the table exists in the recycle bin
            recycle_bin_cursor.execute(f"SELECT * FROM {recycle_bin_table_name} WHERE table_name = ?", (target_table_name,))
            deleted_table_data = recycle_bin_cursor.fetchone()

            if deleted_table_data:
                # Move the table from the recycle bin to the target database
                self._connect_db()
                self.cursor.execute(f"ATTACH DATABASE '{recycle_bin_db_path}' AS recycle_bin_db")
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {target_db_path}.{target_table_name} AS SELECT * FROM recycle_bin_db.{target_table_name}")
                self.cursor.execute(f"DETACH DATABASE recycle_bin_db")
                self.connection.commit()

                # Remove the table entry from the recycle bin
                recycle_bin_cursor.execute(f"DELETE FROM {recycle_bin_table_name} WHERE table_name = ?", (target_table_name,))
                recycle_bin_connection.commit()

                print(f"Restored {target_table_name} from the recycle bin to {target_db_path}.")

            else:
                print(f"Table {target_table_name} not found in the recycle bin.")

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            self._disconnect_db()
            recycle_bin_connection.close()