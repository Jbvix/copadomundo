# Vault Seed — Brasil e Adversários
## Lista exata para Obsidian (MVP do Mapa de Conexões)

**Escopo:** Seleção Brasileira como nó central + rivais históricos + Grupo C 2026  
**Total estimado:** 13 times · 11 edições · 14 partidas · 28 jogadores · 6 técnicos · ~95 arestas  
**Alinhado ao app:** Grupo C (Marrocos, Haiti, Escócia), `JOGADORES`, `HISTORICO_COPAS`

---

## 1. Times (13 notas)

Cada nota em `Times/Nome.md`. ID usado no JSON exportado.

| # | Arquivo Obsidian | `id` | Tipo relação com Brasil | Prioridade |
|---|------------------|------|-------------------------|------------|
| 1 | `Brasil.md` | `team-brasil` | **Nó central** | ★★★ |
| 2 | `Argentina.md` | `team-argentina` | Rival histórico (Superclássico das Américas) | ★★★ |
| 3 | `Alemanha.md` | `team-alemanha` | Rival histórico (7×1, finais) | ★★★ |
| 4 | `Italia.md` | `team-italia` | Rival histórico (1994, 1970) | ★★★ |
| 5 | `Uruguai.md` | `team-uruguai` | Rival histórico (Maracanaço 1950) | ★★★ |
| 6 | `Franca.md` | `team-franca` | Rival histórico (final 1998, 2006) | ★★★ |
| 7 | `Holanda.md` | `team-holanda` | Adversário recorrente (2010, 2014) | ★★☆ |
| 8 | `Marrocos.md` | `team-marrocos` | Grupo C 2026 — Jogo 1 | ★★★ |
| 9 | `Haiti.md` | `team-haiti` | Grupo C 2026 — Jogo 2 | ★★★ |
| 10 | `Escocia.md` | `team-escocia` | Grupo C 2026 — Jogo 3 | ★★★ |
| 11 | `Tchecoslovaquia.md` | `team-tchecoslovaquia` | Final 1962 | ★★☆ |
| 12 | `Suecia.md` | `team-suecia` | Final 1958 | ★★☆ |
| 13 | `Croacia.md` | `team-croacia` | Quartas 2022 (pênaltis) | ★★☆ |

### Frontmatter modelo — Time

```yaml
---
type: Time
id: team-brasil
nome_pt: Brasil
nome_en: Brazil
continente: América do Sul
bandeira: "🇧🇷"
titulos_copa: 5
rival_historico: true
grupo_2026: C
---
```

**Links obrigatórios em `Brasil.md`:**
`[[Argentina]]` · `[[Alemanha]]` · `[[Italia]]` · `[[Uruguai]]` · `[[Franca]]` · `[[Holanda]]` · `[[Marrocos]]` · `[[Haiti]]` · `[[Escocia]]`

**Tag sugerida:** `#time #brasil` ou `#time #adversario`

---

## 2. Edições (11 notas)

Pasta: `Edicoes/`. Apenas Copas com peso narrativo para o Brasil.

| # | Arquivo | `id` | Ano | Sede | Campeão | Brasil |
|---|---------|------|-----|------|---------|--------|
| 1 | `WC-1950.md` | `wc-1950` | 1950 | Brasil | Uruguai | Vice (Maracanaço) |
| 2 | `WC-1958.md` | `wc-1958` | 1958 | Suécia | Brasil | **Campeão** |
| 3 | `WC-1962.md` | `wc-1962` | 1962 | Chile | Brasil | **Campeão** |
| 4 | `WC-1970.md` | `wc-1970` | 1970 | México | Brasil | **Campeão** |
| 5 | `WC-1994.md` | `wc-1994` | 1994 | EUA | Brasil | **Campeão** |
| 6 | `WC-1998.md` | `wc-1998` | 1998 | França | França | Vice |
| 7 | `WC-2002.md` | `wc-2002` | 2002 | Japão/Coreia | Brasil | **Campeão** |
| 8 | `WC-2014.md` | `wc-2014` | 2014 | Brasil | Alemanha | 4º (semifinal) |
| 9 | `WC-2018.md` | `wc-2018` | 2018 | Rússia | França | Quartas |
| 10 | `WC-2022.md` | `wc-2022` | 2022 | Catar | Argentina | Quartas |
| 11 | `WC-2026.md` | `wc-2026` | 2026 | EUA/México/Canadá | — | Em andamento |

### Frontmatter modelo — Edição

```yaml
---
type: Edicao
id: wc-2002
ano: 2002
sede: "Japão / Coreia do Sul"
campeao: "Brasil"
vice: "Alemanha"
artilheiro: "Ronaldo Fenômeno (8 gols)"
---
```

**Links em cada edição:** campeão, vice, partidas-chave, `[[Brasil]]` se participou.

---

## 3. Partidas (14 notas)

Pasta: `Partidas/`. Nome do arquivo = slug curto.

| # | Arquivo | `id` | Placar | Fase | Edição | Adversário |
|---|---------|------|--------|------|--------|------------|
| 1 | `Final-1950-URU-BRA.md` | `match-1950-final` | Uruguai 2×1 Brasil | Final | 1950 | Uruguai |
| 2 | `Final-1958-BRA-SUE.md` | `match-1958-final` | Brasil 5×2 Suécia | Final | 1958 | Suécia |
| 3 | `Final-1962-BRA-TCH.md` | `match-1962-final` | Brasil 3×1 Tchecoslováquia | Final | 1962 | Tchecoslováquia |
| 4 | `Final-1970-BRA-ITA.md` | `match-1970-final` | Brasil 4×1 Itália | Final | 1970 | Itália |
| 5 | `Final-1994-BRA-ITA.md` | `match-1994-final` | Brasil 0×0 (3×2 pen) Itália | Final | 1994 | Itália |
| 6 | `Final-1998-FRA-BRA.md` | `match-1998-final` | França 3×0 Brasil | Final | 1998 | França |
| 7 | `Final-2002-BRA-ALE.md` | `match-2002-final` | Brasil 2×0 Alemanha | Final | 2002 | Alemanha |
| 8 | `Semifinal-2014-ALE-BRA.md` | `match-2014-semifinal` | Alemanha 7×1 Brasil | Semifinal | 2014 | Alemanha |
| 9 | `Quartas-2018-BRA-BEL.md` | `match-2018-quartas` | Bélgica 2×1 Brasil | Quartas | 2018 | Bélgica* |
| 10 | `Quartas-2022-CRO-BRA.md` | `match-2022-quartas` | Croácia 1×1 (4×2 pen) Brasil | Quartas | 2022 | Croácia |
| 11 | `GrupoC-2026-BRA-MAR.md` | `match-2026-gc1` | Brasil × Marrocos | Grupo C R1 | 2026 | Marrocos |
| 12 | `GrupoC-2026-BRA-HAI.md` | `match-2026-gc2` | Brasil × Haiti | Grupo C R2 | 2026 | Haiti |
| 13 | `GrupoC-2026-SCO-BRA.md` | `match-2026-gc3` | Escócia × Brasil | Grupo C R3 | 2026 | Escócia |
| 14 | `Final-2022-ARG-FRA.md` | `match-2022-final` | Argentina 3×3 (4×2 pen) França | Final | 2022 | — (contexto) |

\* Bélgica 2018: incluir nota `Bélgica.md` (`team-belgica`) **opcional** — adiciona +1 time se quiser grafo mais completo em 2018.

### Frontmatter modelo — Partida

```yaml
---
type: Partida
id: match-2014-semifinal
ano: 2014
data: "2014-07-08"
placar: "Alemanha 7 × 1 Brasil"
fase: Semifinal
edicao: 2014
local: "Estádio Mineirão, Belo Horizonte"
destaque: "Maior derrota do Brasil em Copas"
---
```

**Links obrigatórios:** `[[Brasil]]`, adversário, `[[WC-XXXX]]`, artilheiros (`[[Thomas Müller]]` etc.).

---

## 4. Jogadores (28 notas)

Pasta: `Jogadores/`.

### 4.1 Lenda — Brasil (8)

| # | Arquivo | `id` | Posição | Copas | Links principais |
|---|---------|------|---------|-------|------------------|
| 1 | `Pele.md` | `player-pele` | Atacante | 1958, 1962, 1966, 1970 | `[[Brasil]]`, `[[Final-1958-BRA-SUE]]`, `[[Final-1970-BRA-ITA]]` |
| 2 | `Garrincha.md` | `player-garrincha` | Atacante | 1958, 1962, 1966 | `[[Brasil]]`, `[[Final-1962-BRA-TCH]]` |
| 3 | `Ronaldo-Fenomeno.md` | `player-ronaldo-fenomeno` | Atacante | 1994*, 1998, 2002, 2006 | `[[Brasil]]`, `[[Final-2002-BRA-ALE]]` |
| 4 | `Romario.md` | `player-romario` | Atacante | 1990*, 1994 | `[[Brasil]]`, `[[Final-1994-BRA-ITA]]` |
| 5 | `Zico.md` | `player-zico` | Meio-campo | 1978, 1982, 1986 | `[[Brasil]]` |
| 6 | `Cafu.md` | `player-cafu` | Lateral | 1994, 1998, 2002, 2006 | `[[Brasil]]`, `[[Final-2002-BRA-ALE]]` |
| 7 | `Rivaldo.md` | `player-rivaldo` | Atacante | 1998, 2002 | `[[Brasil]]`, `[[Final-2002-BRA-ALE]]` |
| 8 | `Neymar.md` | `player-neymar` | Atacante | 2014, 2018, 2022, 2026 | `[[Brasil]]`, `[[Semifinal-2014-ALE-BRA]]`, `[[Quartas-2022-CRO-BRA]]` |

\*Convocado / elenco em algumas edições.

### 4.2 Elenco 2026 — Brasil (10)

Alinhado ao app (`JOGADORES` + elenco provável):

| # | Arquivo | `id` | Posição | Clube (link) |
|---|---------|------|---------|--------------|
| 9 | `Vinicius-Junior.md` | `player-vinicius-jr` | Atacante | `[[Real Madrid]]` |
| 10 | `Rodrygo.md` | `player-rodrygo` | Atacante | `[[Real Madrid]]` |
| 11 | `Bruno-Guimaraes.md` | `player-bruno-guimaraes` | Meio-campo | `[[Newcastle]]` |
| 12 | `Alisson.md` | `player-alisson` | Goleiro | `[[Liverpool]]` |
| 13 | `Marquinhos.md` | `player-marquinhos` | Zagueiro | `[[PSG]]` |
| 14 | `Raphinha.md` | `player-raphinha` | Atacante | `[[Barcelona]]` |
| 15 | `Casemiro.md` | `player-casemiro` | Meio-campo | `[[Manchester United]]` |
| 16 | `Endrick.md` | `player-endrick` | Atacante | `[[Real Madrid]]` |
| 17 | `Gabriel-Magalhaes.md` | `player-gabriel-magalhaes` | Zagueiro | `[[Arsenal]]` |
| 18 | `Estevao.md` | `player-estevao` | Atacante | `[[Chelsea]]` |

### 4.3 Adversários — ícones (10)

Um ícone por rival, para conectar partidas sem inflar o grafo:

| # | Arquivo | `id` | Seleção | Partida link |
|---|---------|------|---------|--------------|
| 19 | `Lionel-Messi.md` | `player-messi` | Argentina | `[[Final-2022-ARG-FRA]]` + rival de `[[Neymar]]` |
| 20 | `Diego-Maradona.md` | `player-maradona` | Argentina | rival histórico |
| 21 | `Thomas-Muller.md` | `player-muller` | Alemanha | `[[Semifinal-2014-ALE-BRA]]` |
| 22 | `Miroslav-Klose.md` | `player-klose` | Alemanha | artilheiro recorde |
| 23 | `Zinedine-Zidane.md` | `player-zidane` | França | `[[Final-1998-FRA-BRA]]` |
| 24 | `Paolo-Rossi.md` | `player-paolo-rossi` | Itália | contexto 1982* |
| 25 | `Roberto-Baggio.md` | `player-baggio` | Itália | `[[Final-1994-BRA-ITA]]` (pênalti) |
| 26 | `Alcides-Ghiggia.md` | `player-ghiggia` | Uruguai | `[[Final-1950-URU-BRA]]` (gol) |
| 27 | `Luka-Modric.md` | `player-modric` | Croácia | `[[Quartas-2022-CRO-BRA]]` |
| 28 | `Kylian-Mbappe.md` | `player-mbappe` | França | `[[Final-2022-ARG-FRA]]` |

### Frontmatter modelo — Jogador

```yaml
---
type: Jogador
id: player-neymar
nome: Neymar
posicao: Atacante
nacionalidade: Brasil
copas: [2014, 2018, 2022, 2026]
clube_atual: Al-Hilal
---
```

**Corpo mínimo:**
```markdown
# Neymar

- Seleção: [[Brasil]]
- Partidas marcantes: [[Semifinal-2014-ALE-BRA]], [[Quartas-2022-CRO-BRA]]
- Rival de campo: [[Lionel Messi]]

#jogador #brasil #atacante
```

---

## 5. Técnicos (6 notas)

Pasta: `Tecnicos/`.

| # | Arquivo | `id` | Seleção | Copas |
|---|---------|------|---------|-------|
| 1 | `Dorival-Junior.md` | `coach-dorival` | Brasil | 2026 |
| 2 | `Tite.md` | `coach-tite` | Brasil | 2018, 2022 |
| 3 | `Felipao-Scolari.md` | `coach-scolari` | Brasil | 2002, 2014 |
| 4 | `Mario-Zagallo.md` | `coach-zagallo` | Brasil | 1970 (técnico), 1994 (coord.) |
| 5 | `Joachim-Low.md` | `coach-low` | Alemanha | 2014 |
| 6 | `Didier-Deschamps.md` | `coach-deschamps` | França | 2018, 2022 |

Link: `tecnico_de` → `[[Brasil]]` ou adversário.

---

## 6. Clubes (12 notas — opcional, enriquece elenco 2026)

Pasta: `Clubes/`. Só clubes dos jogadores atuais + históricos icônicos.

| Arquivo | `id` |
|---------|------|
| `Real-Madrid.md` | `club-real-madrid` |
| `Barcelona.md` | `club-barcelona` |
| `PSG.md` | `club-psg` |
| `Liverpool.md` | `club-liverpool` |
| `Arsenal.md` | `club-arsenal` |
| `Newcastle.md` | `club-newcastle` |
| `Manchester-United.md` | `club-man-utd` |
| `Chelsea.md` | `club-chelsea` |
| `Santos.md` | `club-santos` |
| `Al-Hilal.md` | `club-al-hilal` |
| `Bayern-Munchen.md` | `club-bayern` |
| `Inter-Milan.md` | `club-inter` |

Relação: `atua_no_clube` (Jogador → Clube).

---

## 7. Mapa de arestas (referência para export)

| Relação | Qtd estimada | Exemplo |
|---------|--------------|---------|
| `rival_historico` | 6 | Brasil ↔ Argentina |
| `participou_de` | ~25 | Brasil → WC-2002 |
| `disputou` | 14 | Partida → WC-XXXX |
| `venceu` / `perdeu` | 14 | Alemanha → Semifinal 2014 |
| `jogou_em` | ~28 | Neymar → Brasil |
| `marcou_em` | ~15 | Ronaldo → Final 2002 |
| `tecnico_de` | 6 | Tite → Brasil |
| `atua_no_clube` | ~12 | Vinícius → Real Madrid |
| **Total** | **~120** | |

---

## 8. Estrutura de pastas do vault

```
obsidian-vault-copa-brasil/
├── 00-Indice.md              ← mapa mental + link para Brasil
├── Edicoes/
│   ├── WC-1950.md … WC-2026.md
├── Times/
│   ├── Brasil.md
│   ├── Argentina.md … Escocia.md
├── Partidas/
│   ├── Final-1950-URU-BRA.md …
├── Jogadores/
│   ├── Pele.md … Estevao.md
├── Tecnicos/
│   └── …
├── Clubes/                   ← opcional fase 1.5
│   └── …
└── _templates/
    ├── time.md
    ├── jogador.md
    ├── partida.md
    └── edicao.md
```

---

## 9. Nota central — `00-Indice.md`

```markdown
# Rede da Seleção Brasileira

Nó central: [[Brasil]]

## Grupo C — Copa 2026
- [[Marrocos]] · [[Haiti]] · [[Escocia]]
- [[GrupoC-2026-BRA-MAR]] · [[GrupoC-2026-BRA-HAI]] · [[GrupoC-2026-SCO-BRA]]

## Rivalidades históricas
- [[Argentina]] · [[Alemanha]] · [[Italia]] · [[Uruguai]] · [[Franca]] · [[Holanda]]

## Títulos (5)
[[WC-1958]] · [[WC-1962]] · [[WC-1970]] · [[WC-1994]] · [[WC-2002]]

## Traumas e viradas
- [[Final-1950-URU-BRA]] (Maracanaço)
- [[Semifinal-2014-ALE-BRA]] (7×1)
- [[Final-2002-BRA-ALE]] (redenção)

#indice #brasil #copa2026
```

---

## 10. Template Obsidian — `_templates/jogador.md`

```markdown
---
type: Jogador
id: player-{{nome_slug}}
nome: {{nome}}
posicao:
nacionalidade:
copas: []
clube_atual:
---

# {{nome}}

- Seleção: [[Brasil]]
- Partidas:
- Clube: [[]]

#jogador
```

---

## 11. Ordem de criação sugerida (3 sessões)

### Sessão 1 — Esqueleto (2 h)
1. `00-Indice.md` + `Brasil.md`
2. 6 rivais históricos + 3 do Grupo C
3. `WC-2026.md` + 3 partidas do grupo

### Sessão 2 — História (3 h)
4. Edições 1950–2022 (10 notas)
5. 8 partidas icônicas (1950 → 2022)
6. 8 jogadores lenda

### Sessão 3 — Atual (2 h)
7. 10 jogadores elenco 2026
8. 6 técnicos
9. 10 ícones adversários
10. Revisar links `[[ ]]` quebrados

---

## 12. Checklist antes do export

- [ ] Todo nó tem `id` único no frontmatter
- [ ] `Brasil.md` linka todos os 9 adversários diretos
- [ ] Toda partida linka `[[Brasil]]` + adversário + `[[WC-XXXX]]`
- [ ] Jogadores 2026 linkam `[[Brasil]]` + clube
- [ ] Tags consistentes: `#time` `#jogador` `#partida` `#edicao`
- [ ] Nenhum link órfão (Dataview: `LIST FROM [[Brasil]]`)

---

## 13. Resumo numérico

| Entidade | Quantidade |
|----------|------------|
| Times | 13 (+1 Bélgica opcional) |
| Edições | 11 |
| Partidas | 14 |
| Jogadores | 28 |
| Técnicos | 6 |
| Clubes | 12 (opcional) |
| **Notas totais (MVP)** | **~72** (+12 clubes) |
| **Arestas estimadas** | **~120** |

---

*Próximo passo técnico: gerar `data/worldcup-graph.json` a partir desta lista (seed manual) ou implementar `export_obsidian_graph.py`.*
