import lancedb
import logging


class VectorDatabase:
    def __init__(self, uri: str):
        self.db = self.connect(uri)

    @staticmethod
    def connect(uri: str):
        """
        Connect to the database and perform a connection check.
        """
        try:
            db = lancedb.connect(uri)
            return db
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise ValueError(f"Unable to connect to database: {uri}")

    def open_table(self, table_name: str):
        """
        Open the table with the specified name and check if it exists.
        """
        if table_name not in self.db.table_names():
            logging.warning(f"Table {table_name} does not exist!")
            raise ValueError(f"Table {table_name} does not exist")
        return self.db.open_table(table_name)

    def create_table(self, table_name: str, data: list):
        """
        Create a new table and perform data format validation.
        """

        # Create table
        try:
            table = self.db.create_table(table_name, data)
            logging.info(f"Table {table_name} created successfully.")
            return table
        except Exception as e:
            logging.error(f"Error creating table {table_name}: {e}")
            raise ValueError(f"Error creating table {table_name}: {e}")

    def read_table(self, table_name: str):
        """
        Read and return all data from the table.
        """
        table = self.open_table(table_name)
        try:
            data = table.to_pandas()
            return data
        except Exception as e:
            logging.error(f"Error reading table {table_name}: {e}")
            raise ValueError(f"Error reading table {table_name}: {e}")

    def update_data(self, table_name: str, update_condition: dict, new_data: dict):
        """
        Update data in the table based on the condition.
        """
        if not isinstance(update_condition, dict) or not isinstance(new_data, dict):
            logging.error("Both update_condition and new_data should be dictionaries.")
            raise ValueError("Both update_condition and new_data should be dictionaries.")

        table = self.open_table(table_name)
        try:
            # Fetch rows to be updated
            rows_to_update = table.query(update_condition)
            for row in rows_to_update:
                # Update the data with new values
                row.update(new_data)

            table.save()
            logging.info(f"Table {table_name} updated successfully.")
        except Exception as e:
            logging.error(f"Error updating table {table_name}: {e}")
            raise ValueError(f"Error updating table {table_name}: {e}")

    def delete_data(self, table_name: str, delete_condition: dict):
        """
        Delete data from the table based on the condition.
        """
        if not isinstance(delete_condition, dict):
            logging.error("Delete condition should be a dictionary.")
            raise ValueError("Delete condition should be a dictionary.")

        table = self.open_table(table_name)
        try:
            # Fetch rows to delete
            rows_to_delete = table.query(delete_condition)
            for row in rows_to_delete:
                table.delete(row)

            table.save()
            logging.info(f"Data deleted from table {table_name} successfully.")
        except Exception as e:
            logging.error(f"Error deleting data from table {table_name}: {e}")
            raise ValueError(f"Error deleting data from table {table_name}: {e}")

    def search(self, table_name: str, query_vector: list, top_k: int = 2):
        """
        Perform a semantic search and validate the query vector.
        """
        if len(query_vector) == 0:
            logging.error("Invalid query vector. It must be a non-empty list.")
            raise ValueError("Invalid query vector. It must be a non-empty list.")

        table = self.open_table(table_name)
        try:
            result = table.search(query_vector).limit(top_k).to_pandas()
            return result
        except Exception as e:
            logging.error(f"Error searching in table {table_name}: {e}")
            raise ValueError(f"Error searching in table {table_name}: {e}")

    def drop_table(self, table_name: str):
        """
        Drop the specified table if it exists.
        """
        if table_name not in self.db.table_names():
            logging.warning(f"Table {table_name} does not exist!")
            raise ValueError(f"Table {table_name} does not exist")

        try:
            self.db.drop_table(table_name)
            logging.info(f"Table {table_name} dropped successfully.")
        except Exception as e:
            logging.error(f"Error dropping table {table_name}: {e}")
            raise ValueError(f"Error dropping table {table_name}: {e}")
