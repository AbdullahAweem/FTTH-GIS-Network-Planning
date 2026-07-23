import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_postgres_engine() -> Engine:
    """
    Create SQLAlchemy engine for PostgreSQL/PostGIS.
    Connection details come from .streamlit/secrets.toml
    """

    db = st.secrets["postgres"]

    user = db["user"]
    password = db["password"]
    host = db["host"]
    port = db["port"]
    database = db["database"]

    connection_url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{database}"
    )

    engine = create_engine(connection_url)

    return engine
