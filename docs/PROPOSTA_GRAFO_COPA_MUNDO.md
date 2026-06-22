# Proposta: Knowledge Graph da Copa do Mundo

## Obsidian → HTML estático → Netlify + integração com o World Cup 2026 Predictor

**Autor:** Jossian Brito  
**Data:** 20/06/2026  
**Status:** Proposta para avaliação (implementação pausada até aprovação)  
**Projeto base:** [copadomundo](https://github.com/Jbvix/copadomundo) — app monolítico (`index.html`) no Netlify com proxies API-Football, Zafronix e IA (Téo)

---

## 1. Resumo executivo

A Copa do Mundo é um domínio natural para **grafos de conhecimento**: times, jogadores, partidas, edições, técnicos, clubes e estatísticas formam uma rede de relações que gráficos de barras e tabelas sozinhos não exploram bem.

A proposta é criar uma **página dedicada de exploração em grafo**, alimentada por um **vault Obsidian** (fonte de conhecimento estruturado), exportada para **JSON + HTML estático** e publicada no **Netlify** — com um **botão de acesso** no app principal.

**Veredicto preliminar:** ✅ **Viável e recomendado**, começando por um MVP estático (Fase 1). O Obsidian que você já usa é ideal como *authoring tool*; o app atual já tem dados ao vivo (API-Football) que podem enriquecer o grafo na Fase 2.

---

## 2. Contexto do projeto atual


| Item             | Situação atual                                        | Implicação para o grafo                      |
| ---------------- | ----------------------------------------------------- | -------------------------------------------- |
| Deploy           | Netlify, publish na raiz, `index.html` único          | Nova rota `/grafo/` ou site irmão            |
| Dados ao vivo    | API-Football via `/api/af`                            | Nós dinâmicos: jogos, placares, elencos 2026 |
| Dados históricos | Array `HISTORICO_COPAS` no JS + Zafronix/openfootball | Seed inicial do grafo                        |
| Jogadores        | `JOGADORES` + CSV API-Football                        | Nós `Jogador` com propriedades               |
| IA               | Téo via `/api/ia`                                     | RAG sobre o grafo na Fase 3                  |
| UI               | Tailwind CDN, tabs internas, dark theme               | Reutilizar identidade visual                 |


**Limitação atual:** tudo vive em um único `index.html` (~4.000 linhas). O grafo **não deve** ser embutido na mesma página no MVP — página separada mantém performance e manutenção saudáveis.

---

## 3. Avaliação da proposta original

### 3.1 Pontos fortes ✅

1. **Obsidian como CMS de conhecimento** — Notas com `[[links]]`, frontmatter YAML, tags e Canvas permitem modelar o domínio sem banco de dados no início.
2. **Grafos alinhados ao domínio** — Relações `jogou_em`, `marcou_gol_em`, `rival_de`, `tecnico_de` são naturais.
3. **Portfólio diferenciado** — Combina experiência marítima/analytics (Tug Failures, BI) com produto visual interativo.
4. **Escalabilidade clara** — JSON estático → Neo4j / RAG depois, sem reescrever o modelo.
5. **Sinergia com o app** — Botão no header leva ao explorador; dados 2026 podem voltar ao Predictor enriquecido.

### 3.2 Riscos e mitigações ⚠️


| Risco                                   | Impacto | Mitigação                                             |
| --------------------------------------- | ------- | ----------------------------------------------------- |
| Obsidian não exporta grafo nativamente  | Médio   | Script Python no repo ou plugin (Juggl / custom)      |
| Grafo grande trava o browser            | Alto    | Lazy load, limite de nós visíveis, filtros por edição |
| Duplicação manual Obsidian ↔ app        | Médio   | Pipeline automatizado no deploy (GitHub Action)       |
| Conta Obsidian ≠ Obsidian Publish       | Baixo   | Publish é opcional; vault local + export basta        |
| Manutenção durante a Copa (dados novos) | Médio   | Camada API-Football sobrepõe nós “ao vivo”            |


### 3.3 O que **não** fazer no MVP

- Neo4j em produção no dia 1  
- RAG completo com LLM  
- Sincronização bidirecional Obsidian ↔ app em tempo real  
- Graph view com 10.000+ nós sem filtro

---

## 4. Arquitetura recomendada (Proposta A — preferida)

```
┌─────────────────────────────────────────────────────────────────┐
│  OBSIDIAN VAULT (local / Sync)                                  │
│  Notas: Times, Jogadores, Partidas, Edições, Técnicos           │
│  [[links]] + frontmatter + tags                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ export (manual ou CI)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  scripts/export_obsidian_graph.py                               │
│  → data/worldcup-graph.json  { nodes[], edges[], meta{} }       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
┌──────────────────────┐         ┌──────────────────────────────┐
│  grafo/index.html    │         │  index.html (app principal)  │
│  vis-network /       │         │  botão "Mapa de Conexões"    │
│  Cytoscape.js        │         │  → link /grafo/              │
└──────────────────────┘         └──────────────────────────────┘
          │                                 │
          └────────────────┬────────────────┘
                           ▼
                    NETLIFY (mesmo site)
                    /          → Predictor
                    /grafo/    → Graph Explorer
                    /api/af    → dados ao vivo (Fase 2)
```

### 4.1 Estrutura de pastas proposta

```
2026 WC/
├── index.html                 # app atual
├── grafo/
│   ├── index.html             # página do grafo (standalone)
│   ├── graph.js               # lógica vis-network
│   └── styles.css             # opcional; ou Tailwind CDN
├── data/
│   └── worldcup-graph.json    # exportado do Obsidian
├── obsidian-vault/            # opcional: vault versionado no repo
│   └── (notas .md)
├── scripts/
│   └── export_obsidian_graph.py
├── netlify.toml               # redirects inalterados
└── docs/
    └── PROPOSTA_GRAFO_COPA_MUNDO.md
```

### 4.2 Schema do grafo (v1)

**Tipos de nó (`type`):**


| Tipo      | ID exemplo         | Propriedades                     |
| --------- | ------------------ | -------------------------------- |
| `Edicao`  | `wc-2022`          | ano, sede, campeao, artilheiro   |
| `Time`    | `team-brasil`      | nome, pais, continente, bandeira |
| `Jogador` | `player-neymar`    | nome, posicao, copas             |
| `Partida` | `match-2022-final` | placar, fase, data               |
| `Tecnico` | `coach-tite`       | nome, nacionalidade              |
| `Clube`   | `club-psg`         | nome, pais                       |


**Tipos de aresta (`rel`):**


| Relação           | De → Para         | Exemplo                |
| ----------------- | ----------------- | ---------------------- |
| `participou_de`   | Time → Edicao     | Brasil → WC 2022       |
| `jogou_em`        | Jogador → Time    | Neymar → Brasil        |
| `marcou_em`       | Jogador → Partida | Messi → Final 2022     |
| `disputou`        | Partida → Edicao  | Final → WC 2022        |
| `venceu`          | Time → Partida    | Argentina → Final 2022 |
| `tecnico_de`      | Tecnico → Time    | Tite → Brasil          |
| `atua_no_clube`   | Jogador → Clube   | Neymar → Al-Hilal      |
| `rival_historico` | Time ↔ Time       | Brasil ↔ Argentina     |


**Formato JSON:**

```json
{
  "meta": { "version": "1.0", "generated": "2026-06-20", "source": "obsidian" },
  "nodes": [
    { "id": "team-brasil", "type": "Time", "label": "Brasil", "continent": "América do Sul" }
  ],
  "edges": [
    { "from": "player-neymar", "to": "team-brasil", "rel": "jogou_em", "years": [2014, 2018, 2022] }
  ]
}
```

### 4.3 Exemplo de nota Obsidian

```markdown
---
type: Jogador
id: player-neymar
posicao: Atacante
copas: [2014, 2018, 2022, 2026]
nacionalidade: Brasil
---

# Neymar

- Seleção: [[Brasil]]
- Clubes: [[Santos]], [[Barcelona]], [[PSG]], [[Al-Hilal]]
- Partidas marcantes: [[Brasil 1-7 Alemanha 2014]], [[Final Copa 2022]]
- Conexões: jogou com [[Lionel Messi]] no [[PSG]]

#jogador #brasil #atacante
```

O script de export lê frontmatter + links `[[ ]]` e gera nós/arestas.

### 4.4 Stack da página HTML


| Camada       | Escolha                              | Motivo                                            |
| ------------ | ------------------------------------ | ------------------------------------------------- |
| Visualização | **vis-network** (via CDN)            | Leve, touch-friendly, sem build step              |
| Alternativa  | Cytoscape.js                         | Mais queries de grafo; curva de aprendizado maior |
| Estilo       | Tailwind CDN                         | Consistência com o app                            |
| Dados        | `fetch('/data/worldcup-graph.json')` | Estático, cacheável                               |
| Busca        | Filtro client-side por label/type    | MVP simples                                       |


### 4.5 Botão no app principal

No header de `index.html`, nova aba ou link externo:

```html
<a href="/grafo/" class="...">
  <i class="fa-solid fa-circle-nodes mr-1"></i> Mapa de Conexões
</a>
```

**Recomendação:** link para `/grafo/` (página separada), não tab interna — evita carregar vis-network no bundle principal.

### 4.6 Netlify

**Opção recomendada:** mesma site, nova pasta `grafo/` — zero config extra, mesmo domínio, APIs compartilhadas.

**Alternativa:** site Netlify separado (`wc-graph.netlify.app`) — útil se o grafo crescer muito ou tiver ciclo de deploy independente.

---

## 5. Outras propostas avaliadas

### Proposta B — Aba interna no app (grafo dentro do `index.html`)


| Prós              | Contras                                |
| ----------------- | -------------------------------------- |
| Uma URL só        | +200 KB JS; pior LCP no mobile         |
| Navegação por tab | `index.html` ainda mais monolítico     |
|                   | Grafo e dashboard competem por memória |


**Veredicto:** ❌ Não recomendado para MVP. Reavaliar se unificar após extrair JS para módulos.

---

### Proposta C — Obsidian Publish como página hospedada

Usar [Obsidian Publish](https://obsidian.md/publish) ($) e linkar do app.


| Prós                  | Contras                                            |
| --------------------- | -------------------------------------------------- |
| Zero código de export | Custo mensal; visual limitado ao tema Publish      |
| Graph view nativo     | Sem integração API-Football                        |
|                       | URL externa (obsidian.md) quebra identidade visual |


**Veredicto:** ⚠️ Bom para documentação; **não** substitui o explorador interativo customizado.

---

### Proposta D — Neo4j Community + API serverless

Vault → import Neo4j → Netlify Function com Cypher → front-end.


| Prós                                             | Contras                                          |
| ------------------------------------------------ | ------------------------------------------------ |
| Queries poderosas (caminho mais curto, PageRank) | Neo4j precisa hospedagem (Aura free tier ou VPS) |
| Base para RAG sério                              | Complexidade operacional alta                    |
| Referência profissional                          | Overkill para MVP                                |


**Veredicto:** ✅ **Fase 3–4** — depois que JSON estático provar valor.

---

### Proposta E — Grafo híbrido: Obsidian (histórico) + API-Football (2026 ao vivo)

Mesma arquitetura da Proposta A, com camada extra:

```
worldcup-graph.json (Obsidian, estático)
        +
/api/af/fixtures + /players (dinâmico, merge no client)
        =
grafo unificado com nós "live" destacados
```


| Prós                             | Contras                     |
| -------------------------------- | --------------------------- |
| Diferencial forte durante a Copa | Lógica de merge no front    |
| Reaproveita infra existente      | IDs precisam mapear EN ↔ PT |


**Veredicto:** ✅ **Melhor evolução pós-MVP** — alinha grafo ao Predictor.

---

### Proposta F — Canvas Obsidian exportado como imagem interativa

Exportar Canvas do Obsidian como PNG/SVG e embedar.


| Prós                   | Contras                     |
| ---------------------- | --------------------------- |
| Rápido para prototipar | Não é interativo de verdade |
| Visual bonito          | Não escala; sem busca       |


**Veredicto:** ⚠️ Apenas para **mockup** ou slide de apresentação.

---

### Proposta G — Subgrafo temático (escopo reduzido)

Em vez do grafo completo, lançar exploradores focados:

1. **"Rivalidades"** — apenas Times + `rival_historico`
2. **"Elenco 2026"** — 48 seleções + jogadores API
3. **"Linha do tempo"** — Edições encadeadas


| Prós                       | Contras                                |
| -------------------------- | -------------------------------------- |
| MVP em 1–2 semanas         | Visão parcial                          |
| Menos risco de performance | Usuário pode querer "o grafo completo" |


**Veredicto:** ✅ **Excelente estratégia de entrega incremental** — começar por **Elenco 2026 + Rivalidades**.

---

## 6. Comparativo resumido


| Proposta                                   | Esforço     | Impacto    | Quando              |
| ------------------------------------------ | ----------- | ---------- | ------------------- |
| **A — Página `/grafo/` + export Obsidian** | Médio       | Alto       | **Agora (MVP)**     |
| B — Tab interna                            | Baixo       | Médio      | Evitar              |
| C — Obsidian Publish                       | Baixo       | Baixo      | Doc complementar    |
| D — Neo4j                                  | Alto        | Muito alto | Fase 3+             |
| **E — Híbrido Obsidian + API**             | Médio-alto  | Muito alto | **Pós-MVP Copa**    |
| F — Canvas estático                        | Muito baixo | Baixo      | Protótipo           |
| **G — Subgrafos temáticos**                | Baixo       | Alto       | **Sprint 1 do MVP** |


**Recomendação final:** **A + G** no curto prazo, evoluindo para **E**, com **D** como horizon.

---

## 7. Funcionalidades por fase

### Fase 1 — MVP (2–3 semanas)

- [x] Vault Obsidian com ~30 notas seed (Brasil, Argentina, 5 edições, 10 jogadores icônicos)
- [ ] Script `export_obsidian_graph.py` → `worldcup-graph.json`
- [ ] `grafo/index.html` com vis-network: zoom, pan, clique no nó → painel lateral
- [ ] Filtros: tipo de nó, edição, busca por nome
- [ ] Botão **"Mapa de Conexões"** no header do app
- [ ] Deploy Netlify (mesmo repositório)

**Entregável:** URL `/grafo/` funcional, grafo explorável no desktop e mobile.

### Fase 2 — Enriquecimento (3–4 semanas)

- [ ] Expandir vault: 48 seleções 2026, técnicos, sedes
- [ ] Merge parcial com API-Football (jogos disputados → nós Partida ao vivo)
- [ ] Métricas simples: grau do nó, contagem de conexões
- [ ] Destaque visual: caminho entre dois nós selecionados
- [ ] Link "Ver no Predictor" ao clicar em partida 2026

### Fase 3 — Inteligência (4–6 semanas)

- [ ] Téo RAG: perguntas sobre o grafo via `/api/ia` + contexto JSON
- [ ] PageRank / centralidade (JS ou pré-calculado no export)
- [ ] Export PNG do subgrafo para compartilhar no LinkedIn
- [ ] CI: push no vault → regenera JSON → redeploy automático

### Fase 4 — Escala (opcional)

- [ ] Neo4j Aura (free) + sync noturno
- [ ] Comunidades (detecção de clusters: CONMEBOL, UEFA, etc.)
- [ ] Recomendação: "jogadores com perfil similar"

---

## 8. Modelagem Obsidian — guia rápido

### 8.1 Plugins úteis (versão free)


| Plugin          | Uso                                                          |
| --------------- | ------------------------------------------------------------ |
| **Dataview**    | Testar queries antes do export (`TABLE copas FROM #jogador`) |
| **Juggl**       | Visualização alternativa do grafo local                      |
| **Templater**   | Templates para Jogador/Time/Partida                          |
| **Folder Note** | Índice por pasta (Edições/, Times/)                          |


*Não é obrigatório plugin de export — o script Python lê `.md` puro.*

### 8.2 Convenções do vault

```
vault-copa/
├── 00-Inbox/
├── Edicoes/
│   └── WC-2022.md
├── Times/
│   └── Brasil.md
├── Jogadores/
│   └── Neymar.md
├── Partidas/
│   └── Final-2022-ARG-FRA.md
├── Tecnicos/
├── Clubes/
└── _templates/
    ├── jogador.md
    └── time.md
```

### 8.3 Quantidade inicial sugerida (MVP)


| Entidade  | Qtd mínima                       |
| --------- | -------------------------------- |
| Edições   | 5 (1970, 1994, 2002, 2022, 2026) |
| Times     | 12 (principais + Brasil)         |
| Jogadores | 20                               |
| Partidas  | 10 icônicas                      |
| Arestas   | ~80 (via links)                  |


---

## 9. Integração visual com o app


| Elemento       | App Predictor       | Página Grafo                   |
| -------------- | ------------------- | ------------------------------ |
| Fundo          | `#0f172a` slate-950 | Igual                          |
| Accent         | emerald + yellow    | Igual                          |
| Fonte          | Tailwind default    | Igual                          |
| Header         | Logo + tabs         | Logo + "← Voltar ao Predictor" |
| Ícone sugerido | `fa-circle-nodes`   | Grafo / rede                   |


Manter identidade evita sensação de "site externo".

---

## 10. Estimativa de esforço


| Tarefa                           | Horas (estimativa) |
| -------------------------------- | ------------------ |
| Modelar vault Obsidian (seed)    | 8–12 h             |
| Script export Python             | 6–10 h             |
| `grafo/index.html` + vis-network | 12–16 h            |
| Filtros, busca, painel detalhe   | 8–12 h             |
| Botão + testes Netlify           | 2–4 h              |
| **Total Fase 1**                 | **~36–54 h**       |


*Compatível com ritmo part-time alinhado à Copa (jun–jul 2026).*

---

## 11. Critérios de sucesso

1. Usuário abre `/grafo/` e explora conexões sem tutorial.
2. Busca "Pelé" ou "Brasil" centraliza o subgrafo relevante.
3. Página carrega em < 3 s com ~200 nós.
4. Botão no app principal funciona em mobile.
5. Vault Obsidian permanece editável sem tocar no HTML manualmente (export script).

---

## 12. Decisões pendentes (para você aprovar)


| #   | Decisão        | Opções                                             | Recomendação                              |
| --- | -------------- | -------------------------------------------------- | ----------------------------------------- |
| 1   | Onde hospedar  | Mesmo site vs site Netlify separado                | **Mesmo site** `/grafo/`                  |
| 2   | Vault no Git?  | Público no repo vs local only                      | **Subpasta `obsidian-vault/`** versionada |
| 3   | MVP scope      | Grafo completo vs subgrafo                         | **Subgrafo "Brasil + rivais + 5 Copas"**  |
| 4   | Biblioteca JS  | vis-network vs Cytoscape                           | **vis-network**                           |
| 5   | Nome da página | "Mapa de Conexões" / "Copa Graph" / "Rede da Copa" | **Mapa de Conexões**                      |


---

## 13. Próximos passos imediatos (quando retomar)

1. Aprovar Proposta **A + G** e decisões da seção 12.
2. Criar vault Obsidian local (ou Sync) com templates.
3. Implementar `scripts/export_obsidian_graph.py`.
4. Criar `grafo/index.html` + JSON seed mínimo (sem Obsidian, para testar UI).
5. Adicionar botão no header do `index.html`.
6. Deploy e teste mobile.

---

## 14. Conclusão

A ideia de usar **grafos na Copa do Mundo via Obsidian** é sólida, alinhada ao seu perfil (engenharia + analytics + app em produção) e complementar ao Predictor — não concorrente.

**Obsidian** resolve o problema difícil: **curadoria e estrutura do conhecimento**.  
**HTML + JSON no Netlify** resolve o problema de **distribuição simples e gratuita**.  
**O app atual** continua sendo o hub de probabilidades e dados ao vivo; o grafo vira a camada de **exploração relacional e educacional**.

Começar pequeno (subgrafo temático, export automatizado, página dedicada) reduz risco e entrega valor visível antes da Copa entrar na fase decisiva.

---

*Documento vivo — atualizar conforme decisões e implementação.*