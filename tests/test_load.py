import pytest

from src.load import create_tables, load_ventes, load_mart
from src.transform import aggregate_by_month


@pytest.fixture(autouse=True)
def setup_db(db, engine, df_clean):
    """Prepare la base : cree les tables et charge les donnees de test."""
    create_tables(db)
    load_ventes(df_clean, engine)
    load_mart(aggregate_by_month(df_clean), engine)


def query(db, sql):
    with db.cursor() as cur:
        cur.execute(sql)
        return cur.fetchone()[0]


class TestLoadVentes:

    def test_ventes_propres_count(self, db, df_clean):
        n = query(db, "SELECT COUNT(*) FROM ventes_propres")
        assert n == len(df_clean)

    def test_ventes_pas_de_montant_negatif(self, db):
        n = query(db, "SELECT COUNT(*) FROM ventes_propres WHERE montant <= 0")
        assert n == 0

    def test_ventes_pas_email_vide(self, db):
        n = query(
            db,
            """
            SELECT COUNT(*) FROM ventes_propres
            WHERE client_email IS NULL OR client_email = ''
            """
        )
        assert n == 0


class TestLoadMart:

    def test_ca_par_mois_count(self, db):
        n = query(db, "SELECT COUNT(*) FROM ca_par_mois")
        assert n == 2

    def test_ca_par_mois_ca_positif(self, db):
        mini = query(db, "SELECT MIN(chiffre_affaires) FROM ca_par_mois")
        assert mini > 0