"""
Orchestrateur ETL DataOps.
Ordre strict : Extract -> Transform -> Load
Usage : python src/run.py
"""

import os
import psycopg2

from extract import extract
from transform import clean, aggregate_by_month
from load import get_engine, create_tables, load_ventes, load_mart, log_etape


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://etl_user:etl_secret@localhost:5433/warehouse"
)

CSV_PATH = "data/ventes.csv"


def main():
    print("=== Pipeline ETL DataOps ===")

    conn = psycopg2.connect(DATABASE_URL)
    engine = get_engine(DATABASE_URL)

    try:
        create_tables(conn)

        # EXTRACT
        print("\n[1/3] Extract ...")
        df_brut = extract(CSV_PATH)
        log_etape(conn, "extract", "success", nb_lignes=len(df_brut))

        # TRANSFORM
        print("\n[2/3] Transform (pandas)...")
        df_clean = clean(df_brut)
        df_mart = aggregate_by_month(df_clean)

        ecartees = len(df_brut) - len(df_clean)
        print(f"{ecartees} lignes invalides ecartees")

        log_etape(conn, "transform", "success", nb_lignes=len(df_clean))

        # LOAD
        print("\n[3/3] Load (PostgreSQL)...")
        n1 = load_ventes(df_clean, engine)
        n2 = load_mart(df_mart, engine)

        log_etape(conn, "load", "success", nb_lignes=n1 + n2)

        print("\n[DONE] Pipeline ETL termine avec succes.")

    except Exception as e:
        log_etape(conn, "pipeline", "failure", message=str(e))
        print(f"\n[ERROR] {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()