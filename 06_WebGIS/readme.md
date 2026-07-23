# FTTH Network Planning and Monitoring Web GIS Portal

A PostGIS-backed Web GIS application for FTTH network planning, asset visualization, FDH-wise analysis, search, and reporting.

## Project Overview

This project is a role-based FTTH Network Planning and Monitoring Web GIS Portal developed using Python, Streamlit, PostgreSQL/PostGIS, GeoPandas, Folium, Plotly, and ReportLab.

The system is designed for telecom GIS and FTTH planning workflows. It allows users to visualize network assets, analyze FDH areas, inspect layer data, search assets, calculate engineering KPIs, and generate reports.

## Key Features

- Role-based login system
- Secure PostgreSQL/PostGIS database integration
- Interactive FTTH network map
- FDH-wise filtering and analysis
- Dashboard KPIs for FTTH assets
- Layer-wise spatial data viewing
- Asset search by FDH, plot, cable, structure, and splice information
- Cable and duct length summaries
- Structure and boundary summaries
- CSV export
- PDF report generation
- PTCL-inspired professional interface

## Technology Stack

- Python
- Streamlit
- PostgreSQL
- PostGIS
- GeoPandas
- Folium
- Streamlit-Folium
- Plotly
- Pandas
- SQLAlchemy
- psycopg2
- ReportLab
- bcrypt

## Main Modules

```text
app.py
database/
  connection.py
  postgis_loader.py
  users.py
  search_queries.py
utils/
  pdf_report.py
assets/
  logo.png

  ## Live Demo

This project is deployed as a portfolio demo on Streamlit Cloud.
## Live Demo

🔗 Live App: https://ftth-gis-network-planning-2geuduvrwpamygyajkqpwv.streamlit.app/

Demo Login:

- Username: `admin`
- Password: `demo123`

Note: The deployed version runs in demo mode using sample FTTH GIS data. The full local version connects to PostgreSQL/PostGIS.