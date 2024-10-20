from .mysql_db import connect_to_mysql
from sqlalchemy import text  # Import text function from SQLAlchemy
from src.google_sheets.sheets_sync import read_sheet_data, write_sheet_data

def sync_google_sheet_to_mysql(spreadsheet_id, range_name, table_name):
    connection = connect_to_mysql()
    try:
        # Fetch current data from MySQL
        existing_data_query = text(f"SELECT name, age, email FROM {table_name}")
        existing_data = connection.execute(existing_data_query).fetchall()
        
        # Create a dictionary to hold existing records by name
        existing_data_dict = {row[0]: {'age': row[1], 'email': row[2]} for row in existing_data}

        # Fetch data from Google Sheet
        data = read_sheet_data(spreadsheet_id, range_name)
        print("Data from Google Sheet:", data)  # Debugging: print the data being inserted

        for row in data[1:]:  # Skip the header row
            if len(row) != 3:
                print(f"Skipping row due to incorrect length: {row}")
                continue

            name = row[0]
            age = int(row[1])
            email = row[2]

            # Check if the record already exists
            if name in existing_data_dict:
                # Update if the data has changed
                existing_record = existing_data_dict[name]
                if existing_record['age'] != age or existing_record['email'] != email:
                    query = text(f"UPDATE {table_name} SET age = :age, email = :email WHERE name = :name")
                    connection.execute(query, {"age": age, "email": email, "name": name})
                    print(f"Updated: Name={name}, Age={age}, Email={email}")
            else:
                # Insert new record
                query = text(f"INSERT INTO {table_name} (name, age, email) VALUES (:name, :age, :email)")
                connection.execute(query, {"name": name, "age": age, "email": email})
                print(f"Inserted: Name={name}, Age={age}, Email={email}")

        # Determine which records to delete
        google_sheet_names = {row[0] for row in data[1:]}  # Get names from Google Sheets
        for name in existing_data_dict:
            if name not in google_sheet_names:
                delete_query = text(f"DELETE FROM {table_name} WHERE name = :name")
                connection.execute(delete_query, {"name": name})
                print(f"Deleted: Name={name}")

        connection.commit()  # Commit the changes to the database
        print("Data synced successfully from Google Sheets to MySQL.")
    except Exception as e:
        print(f"Error in syncing data: {e}")
    finally:
        connection.close()

def sync_mysql_to_google_sheet(spreadsheet_id, range_name, table_name):
    connection = connect_to_mysql()
    
    try:
        # Use connection.execute() with a valid SQL statement
        query = text(f"SELECT name, age, email FROM {table_name}")
        results = connection.execute(query).fetchall()  # Ensure this returns results correctly
        
        # Make sure you're formatting the results correctly
        values = [["Name", "Age", "Email"]]  # Include header row
        values.extend([[row[0], row[1], row[2]] for row in results])  # Adjusting to use index
            
        write_sheet_data(spreadsheet_id, range_name, values)
        print("Data synced successfully from MySQL to Google Sheets.")  # Confirmation message
    except Exception as e:
        print(f"Error in syncing data to Google Sheets: {e}")
    finally:
        connection.close()
