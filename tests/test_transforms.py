import pytest
import pandas as pd

from src.transform import clean, aggregate_by_month, aggregate_by_category


class TestClean:

    def test_clean_retire_email_vide(self, df_brut):
        df = clean(df_brut)
        assert "" not in df["client_email"].values

    def test_clean_retire_montant_negatif(self, df_brut):
        df = clean(df_brut)
        assert (df["montant"] > 0).all()

    def test_clean_nombre_lignes(self, df_brut):
        df = clean(df_brut)
        assert len(df) == 2

    def test_clean_email_lowercase(self, df_brut):
        df = clean(df_brut)
        assert df["client_email"].iloc[0] == "alice@mail.com"

    def test_clean_montant_float(self, df_brut):
        df = clean(df_brut)
        assert df["montant"].dtype == "float64"

    def test_clean_date_datetime(self, df_brut):
        df = clean(df_brut)
        assert pd.api.types.is_datetime64_any_dtype(df["date_vente"])

    def test_clean_ne_modifie_pas_original(self, df_brut):
        original_len = len(df_brut)
        clean(df_brut)
        assert len(df_brut) == original_len


class TestAggregateByMonth:

    def test_agg_nombre_mois(self, df_clean):
        mart = aggregate_by_month(df_clean)
        assert len(mart) == 2

    def test_agg_ca_total(self, df_clean):
        mart = aggregate_by_month(df_clean)
        assert mart["chiffre_affaires"].sum() == pytest.approx(320.5)

    def test_agg_colonnes_presentes(self, df_clean):
        mart = aggregate_by_month(df_clean)
        assert set(mart.columns) >= {"mois", "chiffre_affaires", "nb_transactions"}

    def test_agg_ca_positifs(self, df_clean):
        mart = aggregate_by_month(df_clean)
        assert (mart["chiffre_affaires"] > 0).all()


class TestAggregateByCategory:

    def test_agg_category_nombre_categories(self, df_clean):
        mart = aggregate_by_category(df_clean)
        assert len(mart) == 1

    def test_agg_category_ca_total(self, df_clean):
        mart = aggregate_by_category(df_clean)
        assert mart["chiffre_affaires"].sum() == pytest.approx(320.5)

    def test_agg_category_colonnes_presentes(self, df_clean):
        mart = aggregate_by_category(df_clean)
        assert set(mart.columns) >= {"categorie", "chiffre_affaires", "nb_transactions"}

    def test_agg_category_ca_positifs(self, df_clean):
        mart = aggregate_by_category(df_clean)
        assert (mart["chiffre_affaires"] > 0).all()


