import pandas as pd
from database.connection import get_postgres_engine
from database.postgis_loader import TABLES, quote_table

# Maps display name -> (loader_key, list of possible searchable columns)
SEARCH_TABLES = {
    "Basemap / Plot":            ("Basemap",            ["plot_no", "category", "fdh_name", "building_name"]),
    "Boundary":                  ("Boundary",            ["fdh_name", "fdh_no", "type", "region", "exchange"]),
    "Distribution Cables":       ("Dist_cables",         ["cable_id", "fdh_name", "cable_capacity"]),
    "Distribution Splicers":     ("Dist_splicer",        ["splice_id", "fdh_name", "splicetype", "capacity"]),
    "New Planned Ducts":         ("Ducts",                ["duct_id", "fdh_name", "type"]),
    "Existing Ducts":            ("Existing_Ducts",       ["duct_id", "fdh_name", "type"]),
    "Feeder Cables":             ("Feeder",               ["cable_id", "fdh_name", "cable_capacity"]),
    "Feeder Splicers":           ("Feeder_splicer",       ["splice_id", "fdh_name", "splicetype"]),
    "Existing Structures":       ("Existing_structure",   ["structure_id", "type", "fdh_name"]),
    "New Structures":            ("New_structure",        ["structure_id", "type", "fdh_name"]),
    "Units / FDH / NAP / FAT":   ("Units",                ["element_name", "fdh_name", "type", "exchange", "cable_id"]),
}


def get_existing_columns(table_name: str) -> list:
    """Return real column names from a PostGIS table (schema-qualified, e.g. 'network.Units')."""
    engine = get_postgres_engine()
    schema_name, table_only = table_name.split(".", 1)
    sql = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
    """
    df = pd.read_sql(sql, engine, params=(schema_name, table_only))
    return df["column_name"].tolist()


def search_assets(search_text: str, selected_category: str = "All") -> pd.DataFrame:
    """Search multiple PostGIS asset tables using text search."""
    if not search_text:
        return pd.DataFrame()

    engine = get_postgres_engine()
    search_value = f"%{search_text.lower()}%"
    results = []

    selected = SEARCH_TABLES
    if selected_category != "All":
        selected = {selected_category: SEARCH_TABLES[selected_category]}

    for display_name, (loader_key, possible_columns) in selected.items():
        table_name = TABLES.get(loader_key)
        if not table_name:
            continue
        try:
            real_columns = get_existing_columns(table_name)
            searchable_columns = [c for c in possible_columns if c in real_columns]
            if not searchable_columns:
                continue

            where_sql = " OR ".join([f"LOWER(CAST({c} AS TEXT)) LIKE %s" for c in searchable_columns])
            sql = f"""
                SELECT '{display_name}' AS asset_category, *
                FROM {quote_table(table_name)}
                WHERE {where_sql}
                LIMIT 100;
            """
            params = tuple([search_value] * len(searchable_columns))
            df = pd.read_sql(sql, engine, params=params)
            if "geom" in df.columns:
                df = df.drop(columns=["geom"])
            if not df.empty:
                results.append(df)
        except Exception:
            continue

    if not results:
        return pd.DataFrame()
    return pd.concat(results, ignore_index=True)