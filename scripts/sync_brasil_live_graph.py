#!/usr/bin/env python3
"""
Gera data/brasil-live-graph.json a partir da API-Football (jogos do Brasil na Copa 2026).

Uso:
  python scripts/sync_brasil_live_graph.py          # seed se sem chave API
  APIFOOTBALL_API_KEY=xxx python scripts/sync_brasil_live_graph.py

Endpoints: fixtures, events, lineups (times com Brazil).
"""

import json
import os
import re
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "brasil-live-graph.json"

AF_BASE = "https://v3.football.api-sports.io"
AF_LEAGUE = 1
AF_SEASON = 2026
BRAZIL_TEAM_ID = 6
FINISHED = {"FT", "AET", "PEN"}

TEAM_EN_TO_ID = {
    "Brazil": "team-brasil",
    "Morocco": "team-marrocos",
    "Haiti": "team-haiti",
    "Scotland": "team-escocia",
    "Argentina": "team-argentina",
    "France": "team-franca",
    "Germany": "team-alemanha",
}

TEAM_FLAGS = {
    "team-brasil": "🇧🇷",
    "team-marrocos": "🇲🇦",
    "team-haiti": "🇭🇹",
    "team-escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
}


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "jogador"


def af_get(path: str, params: dict, api_key: str) -> dict:
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{AF_BASE}{path}?{qs}"
    req = urllib.request.Request(url, headers={"x-apisports-key": api_key})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def node(nid: str, ntype: str, label: str, **extra):
    return {"id": nid, "type": ntype, "label": label, "source": "api", **extra}


def edge(fr: str, to: str, rel: str, **extra):
    return {"from": fr, "to": to, "rel": rel, "source": "api", **extra}


def seed_schedule():
    """Calendário previsto do Grupo C (antes dos jogos ou sem API)."""
    matches = [
        {
            "id": "match-2026-gc1",
            "label": "Brasil × Marrocos",
            "status": "scheduled",
            "fase": "Grupo C — Rodada 1",
            "data": "2026-06-13",
            "local": "MetLife Stadium, Nova Jersey",
            "opponentId": "team-marrocos",
            "opponent": "Marrocos",
        },
        {
            "id": "match-2026-gc2",
            "label": "Brasil × Haiti",
            "status": "scheduled",
            "fase": "Grupo C — Rodada 2",
            "data": "2026-06-19",
            "local": "Lincoln Financial Field, Filadélfia",
            "opponentId": "team-haiti",
            "opponent": "Haiti",
        },
        {
            "id": "match-2026-gc3",
            "label": "Escócia × Brasil",
            "status": "scheduled",
            "fase": "Grupo C — Rodada 3",
            "data": "2026-06-24",
            "local": "Hard Rock Stadium, Miami",
            "opponentId": "team-escocia",
            "opponent": "Escócia",
        },
    ]
    nodes = [
        node("team-brasil", "Time", "Brasil", bandeira="🇧🇷", nacionalidade="Brasil"),
        node("team-marrocos", "Time", "Marrocos", bandeira="🇲🇦"),
        node("team-haiti", "Time", "Haiti", bandeira="🇭🇹"),
        node("team-escocia", "Time", "Escócia", bandeira="🏴󠁧󠁢󠁳󠁣󠁴󠁿"),
        node("wc-2026", "Edicao", "Copa 2026", ano=2026),
    ]
    edges = []
    for m in matches:
        mid = m["id"]
        nodes.append(node(
            mid, "Partida", m["label"],
            placar="—", fase=m["fase"], data=m["data"], local=m["local"],
            status=m["status"],
        ))
        opp = m["opponentId"]
        edges.extend([
            edge("team-brasil", mid, "enfrentou"),
            edge(opp, mid, "enfrentou"),
            edge(mid, "wc-2026", "disputou"),
        ])
    return matches, nodes, edges


def build_from_fixture(fx_item: dict, events: list, lineups: list) -> tuple[list, list, dict]:
    fx = fx_item.get("fixture") or {}
    teams = fx_item.get("teams") or {}
    goals = fx_item.get("goals") or {}
    league = fx_item.get("league") or {}
    venue = fx.get("venue") or {}

    home = teams.get("home") or {}
    away = teams.get("away") or {}
    home_name = home.get("name", "")
    away_name = away.get("name", "")
    home_id = TEAM_EN_TO_ID.get(home_name, f"team-{slugify(home_name)}")
    away_id = TEAM_EN_TO_ID.get(away_name, f"team-{slugify(away_name)}")

    fixture_id = fx.get("id")
    mid = f"match-af-{fixture_id}"
    gh = goals.get("home")
    ga = goals.get("away")
    placar = f"{home_name} {gh}×{ga} {away_name}" if gh is not None and ga is not None else f"{home_name} × {away_name}"

    status_short = ((fx.get("status") or {}).get("short") or "").upper()
    finished = status_short in FINISHED

    match_meta = {
        "id": mid,
        "fixtureId": fixture_id,
        "label": placar,
        "status": "finished" if finished else "live" if status_short else "scheduled",
        "fase": league.get("round", ""),
        "data": (fx.get("date") or "")[:10],
        "local": ", ".join(filter(None, [venue.get("name"), venue.get("city")])),
        "placar": f"{gh}×{ga}" if gh is not None else "—",
    }

    nodes = [
        node(home_id, "Time", home_name, bandeira=TEAM_FLAGS.get(home_id, "")),
        node(away_id, "Time", away_name, bandeira=TEAM_FLAGS.get(away_id, "")),
        node("wc-2026", "Edicao", "Copa 2026", ano=AF_SEASON),
        node(mid, "Partida", placar, placar=match_meta["placar"], fase=match_meta["fase"],
             data=match_meta["data"], local=match_meta["local"], status=match_meta["status"],
             fixture_id=fixture_id),
    ]
    if venue.get("name"):
        vid = f"venue-{slugify(venue['name'])}"
        nodes.append(node(vid, "Estadio", venue["name"], cidade=venue.get("city", "")))
    else:
        vid = None

    edges = [
        edge(home_id, mid, "enfrentou"),
        edge(away_id, mid, "enfrentou"),
        edge(mid, "wc-2026", "disputou"),
    ]
    if vid:
        edges.append(edge(mid, vid, "realizada_em"))

    home_team_api_id = home.get("id")
    brazil_is_home = home_name == "Brazil"

    for lu in lineups or []:
        team_info = lu.get("team") or {}
        is_brazil = team_info.get("name") == "Brazil"
        coach = lu.get("coach") or {}
        if coach.get("name"):
            cid = f"coach-{slugify(coach['name'])}"
            nodes.append(node(cid, "Tecnico", coach["name"]))
            edges.append(edge(cid, mid, "tecnico_da_partida"))

        for bucket, rel_base in (("startXI", "jogou_na_partida"), ("substitutes", "entrou_em")):
            for entry in lu.get(bucket) or []:
                pl = (entry.get("player") or {})
                pname = pl.get("name")
                if not pname:
                    continue
                pid = f"player-{slugify(pname)}"
                if not any(n["id"] == pid for n in nodes):
                    nodes.append(node(pid, "Jogador", pname, selecao="Brasil" if is_brazil else away_name if is_brazil is False else ""))
                rel = rel_base if bucket == "startXI" else "entrou_em"
                edges.append(edge(pid, mid, rel, titular=bucket == "startXI"))

    for ev in events or []:
        etype = (ev.get("type") or "").lower()
        detail = (ev.get("detail") or "").lower()
        player = (ev.get("player") or {}).get("name")
        assist = (ev.get("assist") or {}).get("name")
        minute = (ev.get("time") or {}).get("elapsed")
        if not player:
            continue
        pid = f"player-{slugify(player)}"
        if not any(n["id"] == pid for n in nodes):
            nodes.append(node(pid, "Jogador", player))
        if etype == "goal" and "missed" not in detail:
            edges.append(edge(pid, mid, "marcou_gol", minuto=minute,
                              penalty="penalty" in detail, own_goal="own" in detail))
        elif etype == "card":
            edges.append(edge(pid, mid, "recebeu_cartao", minuto=minute,
                              cartao="yellow" if "yellow" in detail else "red"))
        if assist:
            aid = f"player-{slugify(assist)}"
            if not any(n["id"] == aid for n in nodes):
                nodes.append(node(aid, "Jogador", assist))
            edges.append(edge(aid, mid, "deu_assistencia", minuto=minute))

    return nodes, edges, match_meta


def sync_from_api(api_key: str) -> dict:
    fixtures_resp = af_get("/fixtures", {
        "league": AF_LEAGUE,
        "season": AF_SEASON,
        "team": BRAZIL_TEAM_ID,
    }, api_key)

    items = fixtures_resp.get("response") or []
    all_nodes: dict[str, dict] = {}
    all_edges: list[dict] = []
    matches_meta: list[dict] = []
    seen_edge = set()

    def add_node(n: dict):
        all_nodes[n["id"]] = {**all_nodes.get(n["id"], {}), **n}

    def add_edge(e: dict):
        key = (e["from"], e["to"], e["rel"])
        if key in seen_edge:
            return
        seen_edge.add(key)
        all_edges.append(e)

    for item in items:
        fx = item.get("fixture") or {}
        fid = fx.get("id")
        if not fid:
            continue
        status = ((fx.get("status") or {}).get("short") or "").upper()
        events, lineups = [], []
        if status in FINISHED or status in {"1H", "2H", "HT", "ET", "PEN", "LIVE"}:
            try:
                ev_resp = af_get("/fixtures/events", {"fixture": fid}, api_key)
                events = ev_resp.get("response") or []
            except urllib.error.HTTPError:
                pass
            try:
                lu_resp = af_get("/fixtures/lineups", {"fixture": fid}, api_key)
                lineups = lu_resp.get("response") or []
            except urllib.error.HTTPError:
                pass
        nodes, edges, meta = build_from_fixture(item, events, lineups)
        for n in nodes:
            add_node(n)
        for e in edges:
            add_edge(e)
        matches_meta.append(meta)

    if not matches_meta:
        matches, nodes, edges = seed_schedule()
        return {
            "meta": {
                "version": "1.0",
                "generated": date.today().isoformat(),
                "source": "seed",
                "status": "awaiting_matches",
                "nodeCount": len(nodes),
                "edgeCount": len(edges),
                "matchCount": len(matches),
            },
            "matches": matches,
            "nodes": nodes,
            "edges": edges,
        }

    matches_meta.sort(key=lambda m: m.get("data") or "")
    return {
        "meta": {
            "version": "1.0",
            "generated": datetime.now(timezone.utc).isoformat(),
            "source": "api-football",
            "status": "live",
            "nodeCount": len(all_nodes),
            "edgeCount": len(all_edges),
            "matchCount": len(matches_meta),
        },
        "matches": matches_meta,
        "nodes": list(all_nodes.values()),
        "edges": all_edges,
    }


def main():
    api_key = (
        os.environ.get("APIFOOTBALL_API_KEY")
        or os.environ.get("APISPORTS_KEY")
        or ""
    ).strip()

    if api_key:
        print("Sincronizando com API-Football...")
        payload = sync_from_api(api_key)
    else:
        print("Sem chave API — gerando seed do calendario Grupo C.")
        matches, nodes, edges = seed_schedule()
        payload = {
            "meta": {
                "version": "1.0",
                "generated": date.today().isoformat(),
                "source": "seed",
                "status": "awaiting_matches",
                "nodeCount": len(nodes),
                "edgeCount": len(edges),
                "matchCount": len(matches),
            },
            "matches": matches,
            "nodes": nodes,
            "edges": edges,
        }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    m = payload["meta"]
    print(f"OK: {m['nodeCount']} nos, {m['edgeCount']} arestas, {m['matchCount']} jogos -> {OUT}")


if __name__ == "__main__":
    main()
