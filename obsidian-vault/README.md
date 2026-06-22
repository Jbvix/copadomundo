# Vault Obsidian — Rede da Seleção Brasileira

Knowledge graph da Copa do Mundo focado no **Brasil e adversários**.

## Como abrir no Obsidian

1. Abra o Obsidian.
2. **Open folder as vault** → selecione esta pasta (`obsidian-vault`).
3. Comece por [[00-Indice]] ou [[Brasil]].
4. Ative o **Graph view** (ícone de rede) para visualizar conexões.

## Conteúdo

| Pasta | Notas |
|-------|-------|
| `Times/` | 14 seleções (Brasil + rivais + Grupo C + Bélgica) |
| `Edicoes/` | 11 Copas (1950–2026) |
| `Partidas/` | 14 jogos icônicos |
| `Jogadores/` | 28 (lenda + elenco 2026 + ícones adversários) |
| `Tecnicos/` | 6 |
| `Clubes/` | 12 |
| `_templates/` | 4 modelos para novas notas |

**Total:** 86 notas de conteúdo + índice + 4 templates.

## Regenerar

```bash
python scripts/generate_obsidian_vault.py
```

## Próximo passo

Export para `data/worldcup-graph.json` → página `/grafo/` no Netlify.
