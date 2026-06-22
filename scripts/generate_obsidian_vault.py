#!/usr/bin/env python3
"""Gera o vault Obsidian — Brasil e Adversários (MVP grafo Copa)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "obsidian-vault"


def w(rel: str, content: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    # --- Índice ---
    w("00-Indice.md", """---
type: Indice
id: indice-principal
---

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
""")

    # --- Times (13) ---
    teams = [
        ("Brasil", "team-brasil", "Brasil", "Brazil", "América do Sul", "🇧🇷", 5, True, "C",
         """Seleção brasileira de futebol — nó central do grafo.

## Rivalidades
[[Argentina]] · [[Alemanha]] · [[Italia]] · [[Uruguai]] · [[Franca]] · [[Holanda]]

## Grupo C — Copa 2026
[[Marrocos]] · [[Haiti]] · [[Escocia]]

## Edições
[[WC-1950]] · [[WC-1958]] · [[WC-1962]] · [[WC-1970]] · [[WC-1994]] · [[WC-1998]] · [[WC-2002]] · [[WC-2014]] · [[WC-2018]] · [[WC-2022]] · [[WC-2026]]

## Técnicos
[[Dorival-Junior]] · [[Tite]] · [[Felipao-Scolari]] · [[Mario-Zagallo]]

#time #brasil"""),
        ("Argentina", "team-argentina", "Argentina", "Argentina", "América do Sul", "🇦🇷", 3, True, None,
         "Rival histórico do [[Brasil]]. Superclássico das Américas.\n\nPartidas de contexto: [[Final-2022-ARG-FRA]]\n\n#time #adversario #rival"),
        ("Alemanha", "team-alemanha", "Alemanha", "Germany", "Europa", "🇩🇪", 4, True, None,
         "Rival histórico do [[Brasil]].\n\nPartidas: [[Final-2002-BRA-ALE]] · [[Semifinal-2014-ALE-BRA]]\n\n#time #adversario #rival"),
        ("Italia", "team-italia", "Itália", "Italy", "Europa", "🇮🇹", 4, True, None,
         "Rival histórico do [[Brasil]].\n\nPartidas: [[Final-1970-BRA-ITA]] · [[Final-1994-BRA-ITA]]\n\n#time #adversario #rival"),
        ("Uruguai", "team-uruguai", "Uruguai", "Uruguay", "América do Sul", "🇺🇾", 2, True, None,
         "Rival histórico do [[Brasil]]. Maracanaço 1950.\n\nPartida: [[Final-1950-URU-BRA]]\n\n#time #adversario #rival"),
        ("Franca", "team-franca", "França", "France", "Europa", "🇫🇷", 2, True, None,
         "Rival histórico do [[Brasil]].\n\nPartidas: [[Final-1998-FRA-BRA]] · [[Final-2022-ARG-FRA]]\n\n#time #adversario #rival"),
        ("Holanda", "team-holanda", "Holanda", "Netherlands", "Europa", "🇳🇱", 0, True, None,
         "Adversário recorrente do [[Brasil]] (2010, 2014).\n\n#time #adversario"),
        ("Marrocos", "team-marrocos", "Marrocos", "Morocco", "África", "🇲🇦", 0, False, "C",
         "Adversário do [[Brasil]] no Grupo C — Copa 2026.\n\nPartida: [[GrupoC-2026-BRA-MAR]]\n\n#time #adversario #grupo-c"),
        ("Haiti", "team-haiti", "Haiti", "Haiti", "América do Norte", "🇭🇹", 0, False, "C",
         "Adversário do [[Brasil]] no Grupo C — Copa 2026.\n\nPartida: [[GrupoC-2026-BRA-HAI]]\n\n#time #adversario #grupo-c"),
        ("Escocia", "team-escocia", "Escócia", "Scotland", "Europa", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", 0, False, "C",
         "Adversário do [[Brasil]] no Grupo C — Copa 2026.\n\nPartida: [[GrupoC-2026-SCO-BRA]]\n\n#time #adversario #grupo-c"),
        ("Tchecoslovaquia", "team-tchecoslovaquia", "Tchecoslováquia", "Czechoslovakia", "Europa", "🇨🇿", 0, False, None,
         "Adversário do [[Brasil]] na final de 1962.\n\nPartida: [[Final-1962-BRA-TCH]]\n\n#time #adversario"),
        ("Suecia", "team-suecia", "Suécia", "Sweden", "Europa", "🇸🇪", 0, False, None,
         "Adversário do [[Brasil]] na final de 1958.\n\nPartida: [[Final-1958-BRA-SUE]]\n\n#time #adversario"),
        ("Croacia", "team-croacia", "Croácia", "Croatia", "Europa", "🇭🇷", 0, False, None,
         "Eliminou o [[Brasil]] nas quartas de 2022.\n\nPartida: [[Quartas-2022-CRO-BRA]]\n\n#time #adversario"),
        ("Belgica", "team-belgica", "Bélgica", "Belgium", "Europa", "🇧🇪", 0, False, None,
         "Eliminou o [[Brasil]] nas quartas de 2018.\n\nPartida: [[Quartas-2018-BRA-BEL]]\n\n#time #adversario"),
    ]
    for fname, tid, npt, nen, cont, flag, titles, rival, grupo, body in teams:
        g = f'\ngrupo_2026: {grupo}' if grupo else ''
        r = 'true' if rival else 'false'
        w(f"Times/{fname}.md", f"""---
type: Time
id: {tid}
nome_pt: {npt}
nome_en: {nen}
continente: {cont}
bandeira: "{flag}"
titulos_copa: {titles}
rival_historico: {r}{g}
---

# {npt}

{body}
""")

    # --- Edições (11) ---
    editions = [
        ("WC-1950", "wc-1950", 1950, "Brasil", "Uruguai", "Brasil", "Ademir de Menezes (9 gols)",
         "[[Uruguai]] venceu. [[Brasil]] vice. [[Final-1950-URU-BRA]]"),
        ("WC-1958", "wc-1958", 1958, "Suécia", "Brasil", "Suécia", "Just Fontaine (13 gols)",
         "[[Brasil]] campeão. [[Final-1958-BRA-SUE]]. [[Pele]] · [[Garrincha]]"),
        ("WC-1962", "wc-1962", 1962, "Chile", "Brasil", "Tchecoslováquia", "Vários (4 gols)",
         "[[Brasil]] bicampeão. [[Final-1962-BRA-TCH]]. [[Garrincha]]"),
        ("WC-1970", "wc-1970", 1970, "México", "Brasil", "Itália", "Gerd Müller (10 gols)",
         "[[Brasil]] tricampeão. [[Final-1970-BRA-ITA]]. [[Pele]] · [[Mario-Zagallo]]"),
        ("WC-1994", "wc-1994", 1994, "EUA", "Brasil", "Itália", "Oleg Salenko / Stoichkov (6 gols)",
         "[[Brasil]] tetra. [[Final-1994-BRA-ITA]]. [[Romario]] · [[Roberto-Baggio]]"),
        ("WC-1998", "wc-1998", 1998, "França", "França", "Brasil", "Davor Šuker (6 gols)",
         "[[Franca]] campeã. [[Brasil]] vice. [[Final-1998-FRA-BRA]]. [[Zinedine-Zidane]]"),
        ("WC-2002", "wc-2002", 2002, "Japão / Coreia do Sul", "Brasil", "Alemanha", "Ronaldo Fenômeno (8 gols)",
         "[[Brasil]] penta. [[Final-2002-BRA-ALE]]. [[Ronaldo-Fenomeno]] · [[Felipao-Scolari]]"),
        ("WC-2014", "wc-2014", 2014, "Brasil", "Alemanha", "Argentina", "James Rodríguez (6 gols)",
         "Copa no Brasil. [[Semifinal-2014-ALE-BRA]]. [[Felipao-Scolari]] · [[Thomas-Muller]]"),
        ("WC-2018", "wc-2018", 2018, "Rússia", "França", "Croácia", "Harry Kane (6 gols)",
         "[[Brasil]] eliminado nas quartas. [[Quartas-2018-BRA-BEL]]. [[Tite]]"),
        ("WC-2022", "wc-2022", 2022, "Catar", "Argentina", "França", "Kylian Mbappé (8 gols)",
         "[[Argentina]] campeã. [[Quartas-2022-CRO-BRA]]. [[Final-2022-ARG-FRA]]. [[Lionel-Messi]]"),
        ("WC-2026", "wc-2026", 2026, "EUA / México / Canadá", "—", "—", "—",
         "Em andamento. [[Brasil]] no Grupo C. [[GrupoC-2026-BRA-MAR]] · [[GrupoC-2026-BRA-HAI]] · [[GrupoC-2026-SCO-BRA]]"),
    ]
    for fname, eid, ano, sede, camp, vice, art, body in editions:
        w(f"Edicoes/{fname}.md", f"""---
type: Edicao
id: {eid}
ano: {ano}
sede: "{sede}"
campeao: "{camp}"
vice: "{vice}"
artilheiro: "{art}"
---

# Copa do Mundo {ano}

- Participação [[Brasil]]: sim
- Campeão: {camp}
- Vice: {vice}

{body}

#edicao #copa
""")

    # --- Partidas (14) ---
    matches = [
        ("Final-1950-URU-BRA", "match-1950-final", 1950, "1950-07-16", "Uruguai 2 × 1 Brasil", "Final", "Maracanã, Rio de Janeiro",
         "Maracanaço", "[[Uruguai]]", "[[Alcides-Ghiggia]]", "wc-1950"),
        ("Final-1958-BRA-SUE", "match-1958-final", 1958, "1958-06-29", "Brasil 5 × 2 Suécia", "Final", "Råsunda, Estocolmo",
         "Primeiro título brasileiro", "[[Suecia]]", "[[Pele]]", "wc-1958"),
        ("Final-1962-BRA-TCH", "match-1962-final", 1962, "1962-06-17", "Brasil 3 × 1 Tchecoslováquia", "Final", "Estadio Nacional, Santiago",
         "Bicampeonato", "[[Tchecoslovaquia]]", "[[Garrincha]]", "wc-1962"),
        ("Final-1970-BRA-ITA", "match-1970-final", 1970, "1970-06-21", "Brasil 4 × 1 Itália", "Final", "Estadio Azteca, Cidade do México",
         "Tricampeonato — futebol-arte", "[[Italia]]", "[[Pele]]", "wc-1970"),
        ("Final-1994-BRA-ITA", "match-1994-final", 1994, "1994-07-17", "Brasil 0 × 0 (3 × 2 pen) Itália", "Final", "Rose Bowl, Pasadena",
         "Tetra nos pênaltis", "[[Italia]]", "[[Romario]] · [[Roberto-Baggio]]", "wc-1994"),
        ("Final-1998-FRA-BRA", "match-1998-final", 1998, "1998-07-12", "França 3 × 0 Brasil", "Final", "Stade de France, Saint-Denis",
         "Dois gols de cabeça de Zidane", "[[Franca]]", "[[Zinedine-Zidane]]", "wc-1998"),
        ("Final-2002-BRA-ALE", "match-2002-final", 2002, "2002-06-30", "Brasil 2 × 0 Alemanha", "Final", "International Stadium, Yokohama",
         "Penta — Ronaldo Fenômeno artilheiro", "[[Alemanha]]", "[[Ronaldo-Fenomeno]]", "wc-2002"),
        ("Semifinal-2014-ALE-BRA", "match-2014-semifinal", 2014, "2014-07-08", "Alemanha 7 × 1 Brasil", "Semifinal", "Mineirão, Belo Horizonte",
         "Maior derrota do Brasil em Copas", "[[Alemanha]]", "[[Thomas-Muller]] · [[Miroslav-Klose]]", "wc-2014"),
        ("Quartas-2018-BRA-BEL", "match-2018-quartas", 2018, "2018-07-06", "Bélgica 2 × 1 Brasil", "Quartas de final", "Kazan Arena, Kazan",
         "Gol nos acréscimos", "[[Belgica]]", "—", "wc-2018"),
        ("Quartas-2022-CRO-BRA", "match-2022-quartas", 2022, "2022-12-09", "Croácia 1 × 1 (4 × 2 pen) Brasil", "Quartas de final", "Estádio Education City, Al Rayyan",
         "Eliminação nos pênaltis", "[[Croacia]]", "[[Luka-Modric]] · [[Neymar]]", "wc-2022"),
        ("GrupoC-2026-BRA-MAR", "match-2026-gc1", 2026, "2026-06-13", "Brasil × Marrocos", "Grupo C — Rodada 1", "MetLife Stadium, Nova Jersey",
         "Abertura do Grupo C", "[[Marrocos]]", "—", "wc-2026"),
        ("GrupoC-2026-BRA-HAI", "match-2026-gc2", 2026, "2026-06-19", "Brasil × Haiti", "Grupo C — Rodada 2", "Lincoln Financial Field, Filadélfia",
         "Segundo jogo do Brasil", "[[Haiti]]", "—", "wc-2026"),
        ("GrupoC-2026-SCO-BRA", "match-2026-gc3", 2026, "2026-06-24", "Escócia × Brasil", "Grupo C — Rodada 3", "Hard Rock Stadium, Miami",
         "Fechamento do grupo", "[[Escocia]]", "—", "wc-2026"),
        ("Final-2022-ARG-FRA", "match-2022-final", 2022, "2022-12-18", "Argentina 3 × 3 (4 × 2 pen) França", "Final", "Lusail Stadium, Lusail",
         "Contexto — rival Messi/Neymar", "[[Argentina]] · [[Franca]]", "[[Lionel-Messi]] · [[Kylian-Mbappe]]", "wc-2022"),
    ]
    for fname, mid, ano, data, placar, fase, local, dest, adv, arts, wc in matches:
        w(f"Partidas/{fname}.md", f"""---
type: Partida
id: {mid}
ano: {ano}
data: "{data}"
placar: "{placar}"
fase: {fase}
edicao: {ano}
local: "{local}"
destaque: "{dest}"
---

# {placar}

- Edição: [[{wc.replace('wc-', 'WC-').upper() if wc.startswith('wc') else wc}]]
- [[Brasil]] vs {adv}
- Artilheiros / destaques: {arts}

#partida #copa
""")

    # Fix WC link format - wc-1950 -> WC-1950
    for f in (ROOT / "Partidas").glob("*.md"):
        t = f.read_text(encoding="utf-8")
        t = t.replace("[[WC-1950]]", "[[WC-1950]]")  # already correct if we use WC-1950
        # regenerate with correct links in loop below - let me fix the match loop

    # Re-write matches with correct WC links
    for fname, mid, ano, data, placar, fase, local, dest, adv, arts, wc in matches:
        wc_link = f"WC-{ano}" if wc == f"wc-{ano}" else "WC-2026"
        w(f"Partidas/{fname}.md", f"""---
type: Partida
id: {mid}
ano: {ano}
data: "{data}"
placar: "{placar}"
fase: {fase}
edicao: {ano}
local: "{local}"
destaque: "{dest}"
---

# {placar}

- Edição: [[{wc_link}]]
- [[Brasil]] vs {adv}
- Artilheiros / destaques: {arts}

#partida #copa
""")

    # --- Jogadores (28) ---
    players = [
        ("Pele", "player-pele", "Pelé", "Atacante", "Brasil", [1958, 1962, 1966, 1970], "Santos",
         "[[Brasil]] · [[Final-1958-BRA-SUE]] · [[Final-1970-BRA-ITA]]", "#jogador #brasil #lenda"),
        ("Garrincha", "player-garrincha", "Garrincha", "Atacante", "Brasil", [1958, 1962, 1966], "Botafogo",
         "[[Brasil]] · [[Final-1962-BRA-TCH]]", "#jogador #brasil #lenda"),
        ("Ronaldo-Fenomeno", "player-ronaldo-fenomeno", "Ronaldo Fenômeno", "Atacante", "Brasil", [1994, 1998, 2002, 2006], "Corinthians",
         "[[Brasil]] · [[Final-2002-BRA-ALE]]", "#jogador #brasil #lenda"),
        ("Romario", "player-romario", "Romário", "Atacante", "Brasil", [1990, 1994], "Flamengo",
         "[[Brasil]] · [[Final-1994-BRA-ITA]]", "#jogador #brasil #lenda"),
        ("Zico", "player-zico", "Zico", "Meio-campo", "Brasil", [1978, 1982, 1986], "Flamengo",
         "[[Brasil]]", "#jogador #brasil #lenda"),
        ("Cafu", "player-cafu", "Cafu", "Lateral", "Brasil", [1994, 1998, 2002, 2006], "Roma",
         "[[Brasil]] · [[Final-2002-BRA-ALE]]", "#jogador #brasil #lenda"),
        ("Rivaldo", "player-rivaldo", "Rivaldo", "Atacante", "Brasil", [1998, 2002], "Barcelona",
         "[[Brasil]] · [[Final-2002-BRA-ALE]]", "#jogador #brasil #lenda"),
        ("Neymar", "player-neymar", "Neymar", "Atacante", "Brasil", [2014, 2018, 2022, 2026], "Al-Hilal",
         "[[Brasil]] · [[Semifinal-2014-ALE-BRA]] · [[Quartas-2022-CRO-BRA]] · rival [[Lionel-Messi]]", "#jogador #brasil #atacante"),
        ("Vinicius-Junior", "player-vinicius-jr", "Vinícius Júnior", "Atacante", "Brasil", [2022, 2026], "Real Madrid",
         "[[Brasil]] · [[Real-Madrid]]", "#jogador #brasil #elenco2026"),
        ("Rodrygo", "player-rodrygo", "Rodrygo", "Atacante", "Brasil", [2022, 2026], "Real Madrid",
         "[[Brasil]] · [[Real-Madrid]]", "#jogador #brasil #elenco2026"),
        ("Bruno-Guimaraes", "player-bruno-guimaraes", "Bruno Guimarães", "Meio-campo", "Brasil", [2022, 2026], "Newcastle",
         "[[Brasil]] · [[Newcastle]]", "#jogador #brasil #elenco2026"),
        ("Alisson", "player-alisson", "Alisson", "Goleiro", "Brasil", [2018, 2022, 2026], "Liverpool",
         "[[Brasil]] · [[Liverpool]]", "#jogador #brasil #elenco2026"),
        ("Marquinhos", "player-marquinhos", "Marquinhos", "Zagueiro", "Brasil", [2014, 2018, 2022, 2026], "PSG",
         "[[Brasil]] · [[PSG]]", "#jogador #brasil #elenco2026"),
        ("Raphinha", "player-raphinha", "Raphinha", "Atacante", "Brasil", [2022, 2026], "Barcelona",
         "[[Brasil]] · [[Barcelona]]", "#jogador #brasil #elenco2026"),
        ("Casemiro", "player-casemiro", "Casemiro", "Meio-campo", "Brasil", [2018, 2022, 2026], "Manchester United",
         "[[Brasil]] · [[Manchester-United]]", "#jogador #brasil #elenco2026"),
        ("Endrick", "player-endrick", "Endrick", "Atacante", "Brasil", [2026], "Real Madrid",
         "[[Brasil]] · [[Real-Madrid]]", "#jogador #brasil #elenco2026"),
        ("Gabriel-Magalhaes", "player-gabriel-magalhaes", "Gabriel Magalhães", "Zagueiro", "Brasil", [2026], "Arsenal",
         "[[Brasil]] · [[Arsenal]]", "#jogador #brasil #elenco2026"),
        ("Estevao", "player-estevao", "Estêvão", "Atacante", "Brasil", [2026], "Chelsea",
         "[[Brasil]] · [[Chelsea]]", "#jogador #brasil #elenco2026"),
        ("Lionel-Messi", "player-messi", "Lionel Messi", "Atacante", "Argentina", [2006, 2010, 2014, 2018, 2022], "Inter Miami",
         "[[Argentina]] · [[Final-2022-ARG-FRA]] · rival [[Neymar]]", "#jogador #adversario"),
        ("Diego-Maradona", "player-maradona", "Diego Maradona", "Atacante", "Argentina", [1982, 1986, 1990, 1994], "—",
         "[[Argentina]] · rival histórico do [[Brasil]]", "#jogador #adversario #lenda"),
        ("Thomas-Muller", "player-muller", "Thomas Müller", "Atacante", "Alemanha", [2010, 2014, 2018, 2022], "Bayern München",
         "[[Alemanha]] · [[Semifinal-2014-ALE-BRA]]", "#jogador #adversario"),
        ("Miroslav-Klose", "player-klose", "Miroslav Klose", "Atacante", "Alemanha", [2002, 2006, 2010, 2014], "Lazio",
         "[[Alemanha]] · artilheiro histórico da Copa", "#jogador #adversario"),
        ("Zinedine-Zidane", "player-zidane", "Zinedine Zidane", "Meio-campo", "França", [1998, 2002, 2006], "Real Madrid",
         "[[Franca]] · [[Final-1998-FRA-BRA]]", "#jogador #adversario"),
        ("Paolo-Rossi", "player-paolo-rossi", "Paolo Rossi", "Atacante", "Itália", [1978, 1982, 1986], "Juventus",
         "[[Italia]]", "#jogador #adversario"),
        ("Roberto-Baggio", "player-baggio", "Roberto Baggio", "Atacante", "Itália", [1990, 1994, 1998], "Juventus",
         "[[Italia]] · [[Final-1994-BRA-ITA]]", "#jogador #adversario"),
        ("Alcides-Ghiggia", "player-ghiggia", "Alcides Ghiggia", "Atacante", "Uruguai", [1950], "Peñarol",
         "[[Uruguai]] · [[Final-1950-URU-BRA]]", "#jogador #adversario"),
        ("Luka-Modric", "player-modric", "Luka Modrić", "Meio-campo", "Croácia", [2006, 2014, 2018, 2022], "Real Madrid",
         "[[Croacia]] · [[Quartas-2022-CRO-BRA]]", "#jogador #adversario"),
        ("Kylian-Mbappe", "player-mbappe", "Kylian Mbappé", "Atacante", "França", [2018, 2022], "Real Madrid",
         "[[Franca]] · [[Final-2022-ARG-FRA]]", "#jogador #adversario"),
    ]
    for fname, pid, nome, pos, nat, copas, clube, links, tags in players:
        clube_link = f"[[{clube.replace(' ', '-')}]]" if clube not in ("—", "Santos", "Botafogo", "Corinthians", "Flamengo", "Roma", "Lazio", "Juventus", "Peñarol") else clube
        club_map = {
            "Real Madrid": "[[Real-Madrid]]", "Barcelona": "[[Barcelona]]", "Newcastle": "[[Newcastle]]",
            "Liverpool": "[[Liverpool]]", "PSG": "[[PSG]]", "Manchester United": "[[Manchester-United]]",
            "Chelsea": "[[Chelsea]]", "Arsenal": "[[Arsenal]]", "Al-Hilal": "[[Al-Hilal]]",
            "Bayern München": "[[Bayern-Munchen]]", "Inter Miami": "—", "Santos": "[[Santos]]",
        }
        cl = club_map.get(clube, clube)
        w(f"Jogadores/{fname}.md", f"""---
type: Jogador
id: {pid}
nome: {nome}
posicao: {pos}
nacionalidade: {nat}
copas: {copas}
clube_atual: {clube}
---

# {nome}

- Seleção / contexto: {links}
- Clube: {cl}

{tags}
""")

    # --- Técnicos (6) ---
    coaches = [
        ("Dorival-Junior", "coach-dorival", "Dorival Júnior", "Brasil", [2026],
         "Técnico do [[Brasil]] na [[WC-2026]]."),
        ("Tite", "coach-tite", "Tite", "Brasil", [2018, 2022],
         "Técnico do [[Brasil]] em [[WC-2018]] e [[WC-2022]]."),
        ("Felipao-Scolari", "coach-scolari", "Luiz Felipe Scolari", "Brasil", [2002, 2014],
         "Penta [[WC-2002]]. [[Semifinal-2014-ALE-BRA]]."),
        ("Mario-Zagallo", "coach-zagallo", "Mário Zagallo", "Brasil", [1970, 1994],
         "Tricampeonato [[WC-1970]] como técnico. Coordenador em [[WC-1994]]."),
        ("Joachim-Low", "coach-low", "Joachim Löw", "Alemanha", [2014],
         "Técnico da [[Alemanha]] no 7×1 — [[Semifinal-2014-ALE-BRA]]."),
        ("Didier-Deschamps", "coach-deschamps", "Didier Deschamps", "França", [2018, 2022],
         "Técnico da [[Franca]]. [[WC-2018]] · [[WC-2022]]."),
    ]
    for fname, cid, nome, sel, copas, body in coaches:
        w(f"Tecnicos/{fname}.md", f"""---
type: Tecnico
id: {cid}
nome: {nome}
selecao: {sel}
copas: {copas}
---

# {nome}

{body}

#tecnico
""")

    # --- Clubes (12) ---
    clubs = [
        ("Real-Madrid", "club-real-madrid", "Real Madrid", "Espanha", "🇪🇸",
         "[[Vinicius-Junior]] · [[Rodrygo]] · [[Endrick]]"),
        ("Barcelona", "club-barcelona", "Barcelona", "Espanha", "🇪🇸", "[[Rivaldo]] · [[Raphinha]]"),
        ("PSG", "club-psg", "Paris Saint-Germain", "França", "🇫🇷", "[[Marquinhos]]"),
        ("Liverpool", "club-liverpool", "Liverpool", "Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "[[Alisson]]"),
        ("Arsenal", "club-arsenal", "Arsenal", "Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "[[Gabriel-Magalhaes]]"),
        ("Newcastle", "club-newcastle", "Newcastle United", "Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "[[Bruno-Guimaraes]]"),
        ("Manchester-United", "club-man-utd", "Manchester United", "Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "[[Casemiro]]"),
        ("Chelsea", "club-chelsea", "Chelsea", "Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "[[Estevao]]"),
        ("Santos", "club-santos", "Santos FC", "Brasil", "🇧🇷", "[[Pele]]"),
        ("Al-Hilal", "club-al-hilal", "Al-Hilal", "Arábia Saudita", "🇸🇦", "[[Neymar]]"),
        ("Bayern-Munchen", "club-bayern", "Bayern München", "Alemanha", "🇩🇪", "[[Thomas-Muller]]"),
        ("Inter-Milan", "club-inter", "Inter de Milão", "Itália", "🇮🇹", "—"),
    ]
    for fname, cid, nome, pais, flag, jogadores in clubs:
        w(f"Clubes/{fname}.md", f"""---
type: Clube
id: {cid}
nome: {nome}
pais: {pais}
bandeira: "{flag}"
---

# {nome}

Jogadores no grafo: {jogadores}

#clube
""")

    # --- Templates (4) ---
    w("_templates/time.md", """---
type: Time
id: team-
nome_pt:
nome_en:
continente:
bandeira: ""
titulos_copa: 0
rival_historico: false
---

# 

#time
""")
    w("_templates/jogador.md", """---
type: Jogador
id: player-
nome:
posicao:
nacionalidade:
copas: []
clube_atual:
---

# 

- Seleção: [[Brasil]]
- Partidas:
- Clube:

#jogador
""")
    w("_templates/partida.md", """---
type: Partida
id: match-
ano:
data: ""
placar: ""
fase:
edicao:
local: ""
destaque: ""
---

# 

- Edição: [[]]
- [[Brasil]] vs 

#partida
""")
    w("_templates/edicao.md", """---
type: Edicao
id: wc-
ano:
sede: ""
campeao: ""
vice: ""
artilheiro: ""
---

# Copa do Mundo 

- [[Brasil]]

#edicao
""")

    md_count = len(list(ROOT.rglob("*.md")))
    print(f"Vault gerado em: {ROOT}")
    print(f"Total de notas .md: {md_count}")


if __name__ == "__main__":
    main()
