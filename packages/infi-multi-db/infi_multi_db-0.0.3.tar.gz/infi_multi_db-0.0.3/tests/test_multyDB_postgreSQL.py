from infi_multi_db import MultiDB
import pytest

# Replace 'connection_params' with your actual PostgreSQL connection parameters
connection_params = {
    "dbname": "test",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432,
}


@pytest.fixture
def multy_db_instance():
    multy_db = MultiDB(db_type="postgresql", connection_params=connection_params)
    multy_db.start_connection()
    yield multy_db
    multy_db.stop_connection()


@pytest.fixture
def setup_and_teardown_table(multy_db_instance):
    table_name = "test_table"

    # Setup: Create the table
    multy_db_instance.delete_table(table_name)
    multy_db_instance.create_table(table_name, [("id", "SERIAL"), ("name", "VARCHAR(255)"), ("age", "INTEGER")])

    yield table_name  # This is where the tests run

    # Teardown: Drop the table if it exists
    multy_db_instance.delete_table(table_name)


def test_insert_and_get_record(multy_db_instance, setup_and_teardown_table):
    table_name = setup_and_teardown_table
    record_data = {"name": "John Doe", "age": 30}

    # Insert a record
    multy_db_instance.create_record(table_name, record_data)

    # Get the inserted record
    records = multy_db_instance.read_records(table_name, "")
    assert len(records) == 1
    assert records[0]["name"] == "John Doe"
    assert records[0]["age"] == 30


def test_delete_record(multy_db_instance, setup_and_teardown_table):
    table_name = setup_and_teardown_table
    record_data = {"name": "John Doe", "age": 30}

    # Insert a record
    multy_db_instance.create_record(table_name, record_data)

    # Get the initial count of records
    initial_records = multy_db_instance.read_records(table_name, "")
    initial_count = len(initial_records)

    # Delete the record
    multy_db_instance.remove_record(table_name, record_id=1)

    # Get the count of records after deletion
    final_records = multy_db_instance.read_records(table_name, "")
    final_count = len(final_records)

    # Assert that one record was deleted
    assert final_count == initial_count - 1


def test_get_all_records(multy_db_instance, setup_and_teardown_table):
    table_name = setup_and_teardown_table
    records_data = [
        {"name": "John Doe", "age": 30},
        {"name": "Jane Doe", "age": 25},
        {"name": "Bob Smith", "age": 40},
    ]

    # Insert multiple records
    for record_data in records_data:
        multy_db_instance.create_record(table_name, record_data)

    # Get all records
    all_records = multy_db_instance.read_records(table_name, "")

    # Assert the correct number of records and their content
    assert len(all_records) == len(records_data)
    for idx, record_data in enumerate(records_data):
        assert all_records[idx]["name"] == record_data["name"]
        assert all_records[idx]["age"] == record_data["age"]
