"""Análise exploratória do World Happiness Report 2019.

Execute a partir da raiz do repositório: python analise.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "world-happiness-report-2019.csv"
IMAGES = ROOT / "images"
IMAGES.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
country = "Country (region)"
rank = "Ladder"
factor_columns = {
    "Apoio social": "Social support",
    "PIB per capita (log)": "Log of GDP\nper capita",
    "Expectativa de vida saudável": "Healthy life\nexpectancy",
    "Liberdade": "Freedom",
    "Afeto positivo": "Positive affect",
}

print("=== QUALIDADE DOS DADOS ===")
print(f"Países: {df[country].nunique()}")
print(f"Colunas: {df.shape[1]}")
print(f"Valores ausentes: {int(df.isna().sum().sum())}")
print(f"Linhas duplicadas: {int(df.duplicated().sum())}")
print(f"Países duplicados: {int(df[country].duplicated().sum())}")
print("\\nAusentes por coluna:")
print(df.isna().sum().to_string())

print("\\n=== RANKING LADDER ===")
print(f"Média das posições: {df[rank].mean():.2f}")
print(f"Mediana das posições: {df[rank].median():.2f}")
print("\\n10 melhores posições:")
print(df.nsmallest(10, rank)[[country, rank]].to_string(index=False))
print("\\n10 piores posições:")
print(df.nlargest(10, rank)[[country, rank]].sort_values(rank, ascending=False).to_string(index=False))

corr = df[[rank] + list(factor_columns.values())].corr(method="spearman")[rank].drop(rank)
print("\\n=== SPEARMAN ENTRE RANKINGS ===")
for label, column in factor_columns.items():
    print(f"{label}: {corr[column]:.3f}")

# Gráficos de ranking: posição 1 é a melhor.
best = df.nsmallest(10, rank).sort_values(rank, ascending=False)
plt.figure(figsize=(10, 6))
plt.barh(best[country], best[rank])
plt.xlabel("Posição no ranking (1 = maior felicidade)")
plt.ylabel("País")
plt.title("10 países mais bem posicionados — 2019")
plt.tight_layout()
plt.savefig(IMAGES / "top10_paises.png", dpi=160)
plt.close()

worst = df.nlargest(10, rank).sort_values(rank, ascending=True)
plt.figure(figsize=(10, 6))
plt.barh(worst[country], worst[rank])
plt.xlabel("Posição no ranking (156 = menor felicidade)")
plt.ylabel("País")
plt.title("10 países menos bem posicionados — 2019")
plt.tight_layout()
plt.savefig(IMAGES / "bottom10_paises.png", dpi=160)
plt.close()

for label, column, filename, title in [
    ("Apoio social", "Social support", "felicidade_apoio_social.png",
     "Ranking de felicidade × ranking de apoio social — 2019"),
    ("PIB per capita", "Log of GDP\nper capita", "felicidade_pib.png",
     "Ranking de felicidade × ranking de PIB per capita — 2019"),
]:
    plt.figure(figsize=(8, 6))
    plt.scatter(df[column], df[rank], alpha=0.75)
    plt.xlabel(f"Ranking de {label.lower()} (1 = melhor posição)")
    plt.ylabel("Ranking de felicidade (1 = melhor posição)")
    plt.title(title)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(IMAGES / filename, dpi=160)
    plt.close()

plt.figure(figsize=(8, 5))
labels = list(factor_columns.keys())
values = [corr[column] for column in factor_columns.values()]
plt.barh(labels, values)
plt.axvline(0, linewidth=0.8)
plt.xlabel("Correlação de Spearman com Ladder")
plt.title("Associação entre rankings dos fatores e ranking de felicidade")
plt.tight_layout()
plt.savefig(IMAGES / "correlacoes_spearman.png", dpi=160)
plt.close()

print("\\nGráficos atualizados na pasta images/.")
print("Nota: Ladder é posição no ranking, não pontuação de felicidade de 0 a 10.")
