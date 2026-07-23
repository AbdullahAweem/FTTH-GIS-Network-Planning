import geopandas as gpd
import pandas as pd
import streamlit as st

from database.connection import get_postgres_engine


TABLES = {
    "basemap": "network.Basemap",
    "boundary": "network.Boundary",
    "cmo_tower": "network.CMO_Towers",
    "dist_cables": "network.Distribution_Cables",
    "dist_splicer": "network.Distribution_Splice_Closures",
    "ducts": "network.New_Planned_Ducts",
    "existing_ducts": "network.DKTCC_Ducts",
    "feeder": "network.Feeder_Back_Bone",
    "feeder_splicer": "network.Feeder_Splice_Closures",
    "existing_structure": "network.DKTCC_Structure",
    "new_structure": "network.New_Structure",
    "units": "network.Units",
}


def quote_table(full_name: str) -> str:
    """
    Wrap the table part of 'schema.Table' in double quotes so Postgres
    preserves the exact case instead of lowercasing it, e.g.
    'network.Distribution_Splice_Closures' -> 'network."Distribution_Splice_Closures"'
    """
    schema, table = full_name.split(".", 1)
    return f'{schema}."{table}"'


@st.cache_data(show_spinner=False, ttl=120)
def read_table(table_name: str) -> pd.DataFrame:
    """
    Read a PostGIS table without geometry.
    Used for dashboard calculations and data tables.
    """

    engine = get_postgres_engine()

    sql = f"""
        SELECT *
        FROM {quote_table(table_name)}
    """

    df = pd.read_sql(sql, engine)

    if "geom" in df.columns:
        df = df.drop(columns=["geom"])

    return df


@st.cache_data(show_spinner=False, ttl=120)
def read_geotable(table_name: str) -> gpd.GeoDataFrame:
    """
    Read a PostGIS table with geometry.
    Used for Folium map display.
    """

    engine = get_postgres_engine()

    sql = f"""
        SELECT *
        FROM {quote_table(table_name)}
    """

    gdf = gpd.read_postgis(
        sql,
        engine,
        geom_col="geom"
    )

    return gdf


@st.cache_data(show_spinner=False, ttl=120)
def load_all_postgis() -> dict:
    """
    Load all PostGIS tables used by the FTTH app.
    """

    data = {}

    for key, table_name in TABLES.items():
        try:
            data[key] = read_table(table_name)
        except Exception as error:
            st.warning(f"Could not load {table_name}: {error}")
            data[key] = pd.DataFrame()

    return data


def get_table_name(layer_key: str) -> str:
    """
    Convert app layer key to actual PostGIS table name.
    """

    return TABLES.get(layer_key)
