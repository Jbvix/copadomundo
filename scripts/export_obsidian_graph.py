#!/usr/bin/env python3
"""
Exporta obsidian-vault/*.md → data/worldcup-graph.json
Uso: python scripts/export_obsidian_graph.py
"""

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "obsidian-vault"
OUT = ROOT / "data" / "worldcup-graph.json"

SKIP_DIRS = {"_templates"}
SKIP_FILES = {"README.md"}

WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_simple_yaml(block: str) -> dict:
    """Parser YAML mínimo (sem dependências externas)."""
    data = {}
    key = None
    buf = []

    def flush():
        nonlocal key, buf
        if key is None:
            return
        raw = "\n".join(buf).strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            data[key] = [] if not inner else [
                int(x.strip()) if x.strip().isdigit() else x.strip().strip('"').strip("'")
                for x in inner.split(",")
            ]
        elif raw.lower() in ("true", "false"):
            data[key] = raw.lower() == "true"
        elif raw.isdigit():
            data[key] = int(raw)
        else:
            data[key] = raw.strip('"').strip("'")
        key, buf = None, []

    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" in line and not line.startswith(" "):
            flush()
            k, _, v = line.partition(":")
            key = k.strip()
            rest = v.strip()
            if rest:
                buf = [rest]
            else:
                buf = []
        else:
            buf.append(line)
    flush()
    return data


def label_from_meta(meta: dict, stem: str, body: str = "") -> str:
    if meta.get("type") == "Indice":
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1:
            return h1.group(1).strip()
    for k in ("nome_pt", "nome", "placar", "ano"):
        if k in meta and meta[k]:
            return str(meta[k])
    if meta.get("type") == "Edicao" and meta.get("ano"):
        return f"Copa {meta['ano']}"
    return stem.replace("-", " ")


def collect_notes():
    notes = []
    for path in sorted(VAULT.rglob("*.md")):
        if path.name in SKIP_FILES:
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        m = FRONTMATTER.match(text)
        meta = parse_simple_yaml(m.group(1)) if m else {}
        body = text[m.end():] if m else text
        stem = path.stem
        nid = meta.get("id") or f"note-{stem.lower()}"
        ntype = meta.get("type") or "Nota"
        label = label_from_meta(meta, stem, body)
        links = [g[1] or g[0] for g in WIKI_LINK.findall(body)]
        notes.append({
            "path": str(path.relative_to(VAULT)),
            "stem": stem,
            "id": nid,
            "type": ntype,
            "label": label,
            "meta": meta,
            "links": links,
        })
    return notes


def build_alias_map(notes):
    alias = {}
    for n in notes:
        keys = {n["stem"], n["id"], n["label"]}
        meta = n["meta"]
        for k in ("nome_pt", "nome", "nome_en", "selecao"):
            if meta.get(k):
                keys.add(str(meta[k]))
        for k in keys:
            alias[k.strip()] = n["id"]
            alias[k.strip().lower()] = n["id"]
    return alias


def resolve_link(target: str, alias: dict) -> str | None:
    t = target.strip()
    if t in alias:
        return alias[t]
    tl = t.lower()
    if tl in alias:
        return alias[tl]
    # tentativa: normalizar espaços/hífens
    norm = t.replace(" ", "-")
    if norm in alias:
        return alias[norm]
    if norm.lower() in alias:
        return alias[norm.lower()]
    return None


def infer_rel(source: dict, target: dict) -> str:
    st, tt = source["type"], target["type"]
    if st == "Jogador" and tt == "Time":
        return "jogou_em"
    if st == "Jogador" and tt == "Clube":
        return "atua_no_clube"
    if st == "Jogador" and tt == "Partida":
        return "marcou_em"
    if st == "Time" and tt == "Edicao":
        return "participou_de"
    if st == "Partida" and tt == "Edicao":
        return "disputou"
    if st == "Partida" and tt == "Time":
        return "enfrentou"
    if st == "Tecnico" and tt == "Time":
        return "tecnico_de"
    if st == "Time" and tt == "Time":
        return "rival_historico"
    if st == "Indice" and tt in ("Time", "Partida", "Edicao"):
        return "referencia"
    return "relacionado"


def main():
    notes = collect_notes()
    alias = build_alias_map(notes)
    id_set = {n["id"] for n in notes}

    nodes = []
    for n in notes:
        node = {
            "id": n["id"],
            "type": n["type"],
            "label": n["label"],
            "path": n["path"],
        }
        for k, v in n["meta"].items():
            if k not in ("type", "id") and k not in node:
                node[k] = v
        nodes.append(node)

    edges = []
    seen = set()
    for n in notes:
        src = n["id"]
        for link in n["links"]:
            tgt = resolve_link(link, alias)
            if not tgt or tgt == src or tgt not in id_set:
                continue
            key = (src, tgt)
            if key in seen:
                continue
            seen.add(key)
            target_note = next(x for x in notes if x["id"] == tgt)
            edges.append({
                "from": src,
                "to": tgt,
                "rel": infer_rel(n, target_note),
                "label": link,
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": {
            "version": "1.0",
            "generated": date.today().isoformat(),
            "source": "obsidian-vault",
            "nodeCount": len(nodes),
            "edgeCount": len(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(nodes)} nos, {len(edges)} arestas -> {OUT}")


if __name__ == "__main__":
    main()
