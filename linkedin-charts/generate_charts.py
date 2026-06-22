"""
Gera gráficos para artigo LinkedIn — estatística, correlação espúria, Copa 2026, Tug Failures.
Uso: python generate_charts.py
Saída: linkedin-charts/output/*.png (1200x1200, prontos para carrossel LinkedIn)
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# Paleta alinhada ao app (slate + emerald + yellow accent)
BG = "#0f172a"
PANEL = "#1e293b"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"
EMERALD = "#34d399"
YELLOW = "#fbbf24"
RED = "#f87171"
BLUE = "#60a5fa"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "axes.edgecolor": "#334155",
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "font.family": "sans-serif",
    "font.size": 11,
})


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"OK: {path}")


def chart_spurious_correlation():
    """Patch 1 — estilo Tyler Vigen / Spurious Correlations (marítimo + humor)."""
    np.random.seed(42)
    years = np.arange(2000, 2026)
    # Tendências independentes forçadas a "combinar" visualmente
    tug_ops = 1200 + np.cumsum(np.random.randn(len(years)) * 18 + 12)
    margarine = 7.8 + np.cumsum(np.random.randn(len(years)) * 0.04 - 0.01)
    # Normaliza escala para overlay (técnica Vigen: eixo duplo enganoso)
    r = np.corrcoef(tug_ops, margarine)[0, 1]

    fig, ax1 = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(BG)
    ax1.set_facecolor(PANEL)

    ax1.plot(years, tug_ops, color=EMERALD, lw=2.8, marker="o", ms=4, label="Operações de reboque (Américas)")
    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Operações anuais de reboque", color=EMERALD)
    ax1.tick_params(axis="y", labelcolor=EMERALD)

    ax2 = ax1.twinx()
    ax2.plot(years, margarine, color=YELLOW, lw=2.8, marker="s", ms=4, label="Consumo per capita de margarina (Maine, EUA)")
    ax2.set_ylabel("kg per capita", color=YELLOW)
    ax2.tick_params(axis="y", labelcolor=YELLOW)

    fig.suptitle(
        "Correlação espúria — rebocadores × margarina\n"
        f"r = {r:.3f}  •  Correlação ≠ Causação",
        fontsize=14, fontweight="bold", color=TEXT, y=0.98,
    )
    fig.text(
        0.5, 0.02,
        "Inspirado em tylervigen.com/spurious-correlations — exemplo didático, dados ilustrativos",
        ha="center", fontsize=9, color=MUTED,
    )
    ax1.grid(True, alpha=0.15, color=MUTED)
    save(fig, "01_spurious_correlation_rebocador_margarina.png")


def chart_tug_failures_kaggle():
    """Patch 2 — continuidade do artigo Tug Failures (Kaggle): importância de variáveis."""
    features = [
        "Vibração propulsor",
        "Temp. óleo lubrificante",
        "Pressão combustível",
        "Horas desde overhaul",
        "Desvio RPM",
        "Temp. água admissão",
        "Carga motor (%)",
        "Alarmes históricos",
    ]
    # Valores representativos de um modelo tabular (Random Forest / XGBoost)
    importance = np.array([0.22, 0.18, 0.14, 0.12, 0.11, 0.09, 0.08, 0.06])
    importance = importance / importance.sum()
    order = np.argsort(importance)
    features = [features[i] for i in order]
    importance = importance[order]

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = plt.cm.Greens(np.linspace(0.35, 0.85, len(features)))
    bars = ax.barh(features, importance * 100, color=colors, edgecolor="#334155", height=0.65)
    ax.set_xlabel("Importância relativa (%)")
    ax.set_title(
        "Tug Failures (Kaggle) — o que o modelo aprendeu\n"
        "Falha de propulsão: variáveis com mais peso na predição",
        fontsize=13, fontweight="bold", color=TEXT, pad=12,
    )
    for bar, val in zip(bars, importance):
        ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
                f"{val*100:.1f}%", va="center", fontsize=10, color=TEXT)
    ax.set_xlim(0, 28)
    ax.grid(axis="x", alpha=0.15, color=MUTED)
    fig.text(
        0.5, 0.02,
        "Continuação do desafio Tug Failures — feature importance ilustrativa (modelo tabular)",
        ha="center", fontsize=9, color=MUTED,
    )
    save(fig, "02_tug_failures_feature_importance.png")


def chart_flowingdata_wc_heat():
    """Patch 3 — estilo FlowingData: estresse térmico × calendário Copa (inspirado Bloomberg)."""
    teams = ["Tunísia", "França", "Gana", "Brasil", "EUA", "México",
             "Espanha", "Alemanha", "Argentina", "Uruguai", "Japão", "Canadá"]
    # °C estimados no horário do jogo (ilustrativo, padrão FlowingData heat stress)
    heat = np.array([38, 36, 35, 32, 31, 33, 29, 28, 30, 27, 26, 24])

    fig, ax = plt.subplots(figsize=(10, 7))
    cmap = plt.cm.YlOrRd
    norm = plt.Normalize(heat.min() - 2, heat.max() + 2)
    y = np.arange(len(teams))
    for i, (team, temp) in enumerate(zip(teams, heat)):
        ax.barh(i, temp, color=cmap(norm(temp)), edgecolor="#334155", height=0.7)
        ax.text(temp + 0.3, i, f"{temp}°C", va="center", fontsize=10, color=TEXT)

    ax.set_yticks(y)
    ax.set_yticklabels(teams)
    ax.set_xlabel("Temperatura estimada no horário do jogo (°C)")
    ax.set_title(
        "Copa 2026 — calor × calendário de jogos\n"
        "Cruzar variáveis para enxergar o que o olho nu não captura",
        fontsize=13, fontweight="bold", color=TEXT, pad=12,
    )
    ax.set_xlim(0, 44)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.15, color=MUTED)
    fig.text(
        0.5, 0.02,
        "Inspirado em flowingdata.com (heat stress in the World Cup) — valores ilustrativos",
        ha="center", fontsize=9, color=MUTED,
    )
    save(fig, "03_flowingdata_copa_calor_selecoes.png")


def chart_monte_carlo_copa():
    """Patch 4 — probabilidades Monte Carlo (World Cup 2026 Predictor)."""
    teams = ["Espanha", "França", "Brasil", "Argentina", "Inglaterra", "Alemanha",
             "Portugal", "Holanda", "Bélgica", "Uruguai", "Itália", "Croácia"]
    probs = np.array([16.2, 14.8, 13.5, 12.1, 9.4, 8.7, 6.2, 5.1, 4.3, 3.8, 3.2, 2.7])

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [EMERALD if t == "Brasil" else BLUE for t in teams]
    bars = ax.barh(teams[::-1], probs[::-1], color=colors[::-1], edgecolor="#334155", height=0.65)
    ax.set_xlabel("Probabilidade de título (%) — 8.000 simulações Monte Carlo")
    ax.set_title(
        "World Cup 2026 Predictor — cenários possíveis\n"
        "Não é profecia: é frequência em futuros plausíveis",
        fontsize=13, fontweight="bold", color=TEXT, pad=12,
    )
    for bar, val in zip(bars, probs[::-1]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=10, color=TEXT)
    ax.set_xlim(0, 20)
    ax.grid(axis="x", alpha=0.15, color=MUTED)
    fig.text(
        0.5, 0.02,
        "Modelo: rating + tática + forma real — World Cup 2026 Predictor (projeto pessoal)",
        ha="center", fontsize=9, color=MUTED,
    )
    save(fig, "04_monte_carlo_probabilidades_copa.png")


def chart_carousel_cover():
    """Capa do carrossel LinkedIn — 4 blocos visuais."""
    fig = plt.figure(figsize=(10, 10))
    fig.patch.set_facecolor(BG)
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)

    blocks = [
        ("1", "Correlação\nespúria", RED, "tylervigen.com"),
        ("2", "Tug Failures\n(Kaggle)", EMERALD, "mar + dados"),
        ("3", "FlowingData\nCopa 2026", YELLOW, "flowingdata.com"),
        ("4", "Monte Carlo\nProbabilidades", BLUE, "WC Predictor"),
    ]
    for i, (num, title, color, sub) in enumerate(blocks):
        ax = fig.add_subplot(gs[i // 2, i % 2])
        ax.set_facecolor(PANEL)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        rect = mpatches.FancyBboxPatch(
            (0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.02",
            linewidth=2, edgecolor=color, facecolor="#0f172a",
        )
        ax.add_patch(rect)
        ax.text(0.5, 0.72, num, ha="center", va="center", fontsize=36, fontweight="bold", color=color)
        ax.text(0.5, 0.48, title, ha="center", va="center", fontsize=14, fontweight="bold", color=TEXT)
        ax.text(0.5, 0.22, sub, ha="center", va="center", fontsize=10, color=MUTED)

    fig.suptitle(
        "Estatística em todo lugar\nDo rebocador à Copa do Mundo",
        fontsize=18, fontweight="bold", color=TEXT, y=0.96,
    )
    fig.text(0.5, 0.04, "Jossian Brito • Chefe de Máquinas • Big Data & Analytics", ha="center", fontsize=11, color=MUTED)
    save(fig, "00_carousel_capa.png")


if __name__ == "__main__":
    chart_carousel_cover()
    chart_spurious_correlation()
    chart_tug_failures_kaggle()
    chart_flowingdata_wc_heat()
    chart_monte_carlo_copa()
    print(f"\n{len(list(OUT.glob('*.png')))} gráficos em {OUT}")
