import pandas as pd

df = pd.read_csv("data/ventes.csv")

# nettoyage
df["montant"] = pd.to_numeric(df["montant"], errors="coerce")
df["date_vente"] = pd.to_datetime(df["date_vente"], errors="coerce")

df = df[df["client_email"].notna() & (df["client_email"] != "")]
df = df[df["montant"] > 0]

print("Lignes valides :", len(df))

print("CA total :", df["montant"].sum())

df["mois"] = df["date_vente"].dt.to_period("M")

mart = (
    df.groupby("mois")
      .agg(
          chiffre_affaires=("montant", "sum"),
          nb_transactions=("montant", "count")
      )
      .reset_index()
)

print(mart)
print("Nombre de mois :", len(mart))