import pandas as pd
import geopandas as gpd

from database.connection import get_connection


def read_table(table_name: str) -> pd.DataFrame:
    """
    Read a normal table from the network schema without geometry.
    """
    query = f"""
        SELECT *
        FROM network.{table_name};
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df

    finally:
        connection.close()


def read_spatial_table(table_name: str) -> gpd.GeoDataFrame:
    """
    Read a spatial table from the network schema with geometry.
    """
    query = f"""
        SELECT *
        FROM network.{table_name};
    """

    connection = get_connection()

    try:
        gdf = gpd.read_postgis(
            query,
            connection,
            geom_col="geom"
        )

        return gdf

    finally:
        connection.close()


def read_table_without_geometry(table_name: str) -> pd.DataFrame:
    """
    Read a spatial table but exclude geometry for dashboard calculations.
    This is faster for KPIs and tables.
    """
    query = f"""
        SELECT *
        FROM network.{table_name};
    """

    connection = get_connection()

    try:
        gdf = gpd.read_postgis(
            query,
            connection,
            geom_col="geom"
        )

        df = pd.DataFrame(gdf.drop(columns="geom", errors="ignore"))
        return df

    finally:
        connection.close()