import pytest
from alembic import command
from models.trip import Trip
from sqlalchemy import BOOLEAN
from sqlalchemy.orm import load_only
from sqlalchemy.sql import text


def test_table_exists(engine, alembic_client, alembic_config, inspector):
    """
    Check if a table is successfully populated.
    `base` is a starting point for alembic, and `base+1` is actual table creation.
    Unfortunately, alembic does not support sequential naming pattern,
    and that's why we use the method mentioned above,
    """
    alembic_client.upgrade(alembic_config, 'base+1')
    assert inspector.has_table(Trip.__tablename__)


@pytest.mark.parametrize("revision, expected_name, expected_type", [("head", "store_and_fwd_flag", BOOLEAN)])
def test_table_column_conversion(engine, alembic_client, alembic_config, inspector, revision, expected_name, expected_type):
    alembic_client.upgrade(alembic_config, revision)
    columns = inspector.get_columns(Trip.__tablename__)
    column = [column for column in columns if column["name"] == expected_name][0]
    assert type(column["type"]) == expected_type


def test_migrate_and_update(alembic_client, alembic_config, db_session, data, engine, inspector):
    old_to_new_value_mapping = {'N': False, 'Y': True}
    alembic_client.upgrade(alembic_config, 'base+1')
    select_migrated_query = text("select trip_id, store_and_fwd_flag from trips order by trip_id")
    old_statement = """
    insert into trips (
        trip_id, vendor_id, pickup_datetime, dropoff_datetime,passenger_count,
        pickup_longitude, pickup_latitude, dropoff_longitude,
        dropoff_latitude, store_and_fwd_flag, trip_duration
    )
    values (
       :trip_id, :vendor_id, :pickup_datetime, :dropoff_datetime, :passenger_count,
       :pickup_longitude, :pickup_latitude, :dropoff_longitude, :dropoff_latitude,
       :store_and_fwd_flag, :trip_duration)
    """
    # Query old data
    with engine.connect() as conn:
        for record in data:
            conn.execute(text(old_statement), record)
            conn.commit()
    # Migrate to new version
    with engine.connect() as conn:
        old_column_values = dict(map(lambda item: tuple(item), list(conn.execute(select_migrated_query))))
    alembic_client.upgrade(alembic_config, "head")
    # Query old data
    with engine.connect() as conn:
        new_column_values = dict(map(lambda item: tuple(item), list(conn.execute(select_migrated_query))))
    assert len(old_column_values) == len(new_column_values)
    for key, value in old_column_values.items():
        assert old_to_new_value_mapping[old_column_values[key]] == new_column_values[key]


