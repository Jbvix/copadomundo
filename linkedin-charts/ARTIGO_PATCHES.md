# Artigo LinkedIn — patches com gráficos

Use os PNG em `linkedin-charts/output/` como carrossel (5 slides) ou imagens inline no artigo.

---

## Título sugerido

**Do Tug Failures ao Monte Carlo: estatística não é bicho de sete cabeças**

---

## PATCH 0 — Gancho (conecta ao artigo anterior)

> No meu último artigo, compartilhei a experiência no desafio **Tug Failures no Kaggle** — prever falhas de propulsão em rebocadores a partir de telemetria, vibração, temperatura e histórico operacional.
>
> A lição central foi simples: **dado + contexto + modelo honesto** valem mais que um número bonito na tela.
>
> Hoje quero ampliar essa conversa. Porque estatística e probabilidade não ficam no Kaggle nem no convés — elas estão em **todas** as áreas. Só precisamos aprender a ler.

**[INSERIR GRÁFICO: `00_carousel_capa.png`]**

---

## PATCH 1 — Spurious Correlations (Tyler Vigen)

> Antes de confiar em qualquer gráfico, recomendo visitar **[Spurious Correlations](https://www.tylervigen.com/spurious-correlations)**, do Tyler Vigen.
>
> Lá você encontra pares de variáveis com correlação impressionante — e **zero relação causal**. Margarina e divórcio. Planetas e indicadores sociais. Memes e ações na bolsa.
>
> No convés, aprendi cedo: duas leituras subindo juntas no painel **não provam** a mesma causa. Pode ser tendência comum, variável oculta ou pura coincidência estatística (*data dredging*).

**[INSERIR GRÁFICO: `01_spurious_correlation_rebocador_margarina.png`]**

**Legenda sugerida para o LinkedIn:**
*Exemplo didático no estilo Tyler Vigen: operações de reboque e consumo de margarina correlacionam — mas ninguém serious acreditaria que um explica o outro. Correlação ≠ causação.*

**Texto de transição:**
> O site é engraçado de propósito. E é perigoso no bom sentido: ensina a **desconfiar com método** antes de tomar decisão.

---

## PATCH 2 — Ponte com Tug Failures (Kaggle)

> Voltando ao **Tug Failures**: no Kaggle, o desafio não era “achar qualquer padrão”, e sim identificar **variáveis que realmente importam** para prever falha.
>
> Depois de engenharia de features, balanceamento de classes e validação cruzada, o que ficou claro foi o peso relativo de sinais como vibração, temperatura do óleo, pressão de combustível e horas desde o último overhaul.
>
> Isso conversa diretamente com o que faço como Chefe de Máquinas: monitorar parâmetro, comparar histórico, agir **antes** do evento crítico.

**[INSERIR GRÁFICO: `02_tug_failures_feature_importance.png`]**

**Legenda sugerida:**
*Feature importance do desafio Tug Failures — quais sinais o modelo tabular mais usou para estimar risco de falha.*

**Texto de transição:**
> Estatística aplicada ao mar. Mesma lógica que uso hoje em analytics e simulação.

---

## PATCH 3 — FlowingData (Nathan Yau)

> O segundo endereço que indico é o **[FlowingData](https://flowingdata.com/)**, do Nathan Yau.
>
> Se o Tyler Vigen mostra o **risco** de interpretar mal, o FlowingData mostra o caminho oposto: traduzir número em **compreensão** — clima, economia, esporte, comportamento humano.
>
> Um post recente cruzou calendário da Copa 2026 com previsão de calor para estimar estresse térmico por seleção. Não é adivinhação: é **organizar variáveis** para enxergar o que o olho nu não captura.

**[INSERIR GRÁFICO: `03_flowingdata_copa_calor_selecoes.png`]**

**Legenda sugerida:**
*Inspirado no estilo FlowingData / Bloomberg: temperatura estimada no horário do jogo × seleção — contexto importa tanto quanto o placar.*

**Texto de transição:**
> Visualização não é enfeite. É ferramenta de pensamento — como aprendi na pós em Big Data, BI e Analytics.

---

## PATCH 4 — Copa do Mundo: Monte Carlo no app

> Para a Copa de 2026, montei o **World Cup 2026 Predictor** — projeto pessoal de estudo, não palpite de apostador.
>
> A ideia: simular milhares de chaveamentos (8.000 cenários Monte Carlo), ajustando força de cada seleção por rating, tática e **forma real** conforme os jogos acontecem.
>
> Se a Espanha vence em 1.200 de 8.000 simulações, a probabilidade estimada é ~15%. Não é profecia — é **frequência em futuros plausíveis**.

**[INSERIR GRÁFICO: `04_monte_carlo_probabilidades_copa.png`]**

**Legenda sugerida:**
*Top 12 probabilidades de título — modelo tático + dados reais da competição.*

---

## PATCH 5 — Fechamento

> **Resumo da trilha:**
> 1. Tyler Vigen → aprenda a desconfiar de correlações perfeitas.
> 2. Tug Failures (Kaggle) → aplique estatística no que você domina (no meu caso, propulsão e rebocagem).
> 3. FlowingData → traduza dados em história visual com contexto.
> 4. Copa 2026 → experimente probabilidade como linguagem de incerteza.
>
> Meu objetivo nunca foi parecer guru de dados. É **compartilhar conhecimento** e mostrar que estatística cabe na rotina de quem opera, mantém, decide e aprende continuamente.
>
> **E você:** depois do Tug Failures ou de qualquer projeto com dados, qual foi a lição que mais mudou sua forma de decidir?

**Hashtags:** `#Estatística` `#DataAnalytics` `#Kaggle` `#CopaDoMundo2026` `#Marítimo` `#BigData` `#Probabilidade` `#MachineLearning` `#AprendizadoContínuo`

---

## Ordem do carrossel LinkedIn (5 slides)

| Slide | Arquivo | Texto curto no slide |
|-------|---------|----------------------|
| 1 | `00_carousel_capa.png` | Do rebocador à Copa — estatística em todo lugar |
| 2 | `01_spurious_correlation_rebocador_margarina.png` | Correlação ≠ causação (Tyler Vigen) |
| 3 | `02_tug_failures_feature_importance.png` | Tug Failures Kaggle — variáveis que importam |
| 4 | `03_flowingdata_copa_calor_selecoes.png` | FlowingData — contexto visual |
| 5 | `04_monte_carlo_probabilidades_copa.png` | Monte Carlo — incerteza explicada |

---

## Como gerar os gráficos

```bash
pip install matplotlib numpy
python linkedin-charts/generate_charts.py
```

Arquivos PNG em `linkedin-charts/output/`.
