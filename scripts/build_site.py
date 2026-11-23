#!/usr/bin/env python3
"""Build the static EcoDome knowledge graph from the OKF wiki.

Nodes are concept pages. Edges are markdown links between concepts, plus
`sources` entries that point at another concept. Nothing in the output is
hand-maintained: edit `wiki/` and run this script again.

    python scripts/build_site.py --base /cville-ecodome/ --out dist
    python scripts/build_site.py --base / --out dist   # local preview
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import markdown
import validate_okf

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE = REPO_ROOT / "wiki"
SITE = REPO_ROOT / "site"
REPO = "AgentO3/cville-ecodome"
GITHUB_BLOB = f"https://github.com/{REPO}/blob/main"

TYPE_COLORS = {
    "Project": "#e3a008",
    "Venue": "#3d9a78",
    "Structure": "#3d8bfd",
    "Experience": "#7b6cff",
    "Pilot": "#e07a3d",
    "Budget": "#d4a017",
    "Product": "#1aa6b7",
    "Architecture": "#3d7ea6",
    "Requirement Set": "#6a9cff",
    "Prototype": "#c26dbe",
    "Tool": "#6b8f71",
    "Value": "#d36b8f",
    "Plan": "#c4846c",
    "Question": "#c9a227",
    "Source Summary": "#8d99a6",
    "Attested Computation": "#2bbbad",
    "Reference": "#7f9c96",
    "Organization": "#5c8a72",
    "Timeline": "#b08d57",
    "Event": "#d08a4c",
    "Media": "#6e8caf",
    "Comparable": "#4e9a84",
}
FALLBACK_COLORS = ["#6c8ebf", "#b07d62", "#6a9a6a", "#a67c9a", "#7a8c5a", "#8a6a4f"]
MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "sane_lists", "footnotes"],
    output_format="html",
)
LINK_WITH_LABEL = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")


def color_for(type_name: str) -> str:
    if type_name in TYPE_COLORS:
        return TYPE_COLORS[type_name]
    return FALLBACK_COLORS[sum(ord(char) for char in type_name) % len(FALLBACK_COLORS)]


def as_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        text = value.isoformat()
        return text.replace("+00:00", "Z")
    return str(value)


def trust_tier(data: dict) -> str:
    verified = data.get("verified")
    if not verified:
        return "unverified"
    events = verified if isinstance(verified, list) else [verified]
    actors = [str(event.get("by", "")) for event in events if isinstance(event, dict)]
    if any(actor.startswith("human:") for actor in actors):
        return "human-reviewed"
    if actors:
        return "machine-confirmed"
    return "unverified"


def concept_id(rel: str) -> str:
    return rel[:-3] if rel.endswith(".md") else rel


def page_href(concept: str) -> str:
    return f"pages/{concept}.html"


def github_href(repo_rel: str) -> str:
    return f"{GITHUB_BLOB}/{repo_rel}"


def load_concepts(bundle: Path) -> dict[str, tuple[dict, str, Path]]:
    concepts: dict[str, tuple[dict, str, Path]] = {}
    for path in validate_okf.iter_markdown(bundle):
        if path.name in validate_okf.RESERVED:
            continue
        data, body, has_fm = validate_okf.split_frontmatter(path.read_text(encoding="utf-8"))
        if not has_fm or not isinstance(data, dict) or not data.get("type"):
            continue
        rel = path.relative_to(bundle).as_posix()
        concepts[concept_id(rel)] = (data, body, path)
    return concepts


def concept_for_path(target: Path, bundle: Path, concepts: dict) -> str | None:
    if not target.is_file() or target.suffix != ".md" or target.name in validate_okf.RESERVED:
        return None
    try:
        rel = target.resolve().relative_to(bundle.resolve()).as_posix()
    except ValueError:
        return None
    concept = concept_id(rel)
    return concept if concept in concepts else None


def public_source(resource: str, source_path: Path, bundle: Path, concepts: dict) -> dict:
    title = resource
    entry = {"resource": resource}
    if resource.startswith(("http://", "https://")):
        entry["href"] = resource
        entry["kind"] = "url"
        return entry
    target = validate_okf.local_target(resource, source_path, bundle)
    concept = concept_for_path(target, bundle, concepts) if target is not None else None
    if concept:
        entry["href"] = page_href(concept)
        entry["concept"] = concept
        entry["kind"] = "concept"
        return entry
    if target is not None and target.is_file():
        try:
            rel = target.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
        except ValueError:
            rel = None
        if rel:
            entry["href"] = github_href(rel)
            entry["kind"] = "file"
            return entry
    entry["kind"] = "unresolved"
    return entry


def build_graph(concepts: dict[str, tuple[dict, str, Path]], bundle: Path) -> dict:
    nodes = []
    link_pairs: set[tuple[str, str]] = set()
    cite_pairs: set[tuple[str, str]] = set()
    for concept, (data, body, path) in concepts.items():
        prose = validate_okf.strip_fences(body)
        for destination in validate_okf.LINK_RE.findall(prose):
            target = validate_okf.resolve_md_link(destination, path, bundle)
            if target is None:
                continue
            other = concept_for_path(target, bundle, concepts)
            if other and other != concept:
                link_pairs.add((concept, other))
        for source in data.get("sources") or []:
            if not isinstance(source, dict):
                continue
            resource = source.get("resource")
            if not isinstance(resource, str):
                continue
            target = validate_okf.local_target(resource, path, bundle)
            other = concept_for_path(target, bundle, concepts) if target is not None else None
            if other and other != concept:
                cite_pairs.add((concept, other))

    degree: dict[str, int] = {concept: 0 for concept in concepts}
    for source, target in link_pairs | cite_pairs:
        degree[source] += 1
        degree[target] += 1

    for concept, (data, _body, path) in sorted(concepts.items()):
        generated = data.get("generated") if isinstance(data.get("generated"), dict) else {}
        sources = []
        for source in data.get("sources") or []:
            if not isinstance(source, dict) or not isinstance(source.get("resource"), str):
                continue
            item = public_source(source["resource"], path, bundle, concepts)
            item["id"] = source.get("id")
            item["title"] = source.get("title") or item["resource"]
            sources.append(item)
        wiki_rel = path.relative_to(bundle).as_posix()
        nodes.append(
            {
                "id": concept,
                "title": data.get("title") or concept,
                "description": data.get("description") or "",
                "type": data.get("type"),
                "status": data.get("status") or "stable",
                "tags": data.get("tags") or [],
                "trust": trust_tier(data),
                "generated_by": generated.get("by"),
                "generated_at": as_text(generated.get("at")),
                "stale_after": as_text(data.get("stale_after")),
                "resource": data.get("resource"),
                "sources": sources,
                "color": color_for(str(data.get("type"))),
                "size": min(64, 26 + degree[concept] * 3),
                "section": concept.split("/", 1)[0] if "/" in concept else "root",
                "github": github_href(f"wiki/{wiki_rel}"),
                "page": page_href(concept),
            }
        )

    edges = [
        {"source": source, "target": target, "kind": "link"}
        for source, target in sorted(link_pairs)
    ]
    edges.extend(
        {"source": source, "target": target, "kind": "cites"}
        for source, target in sorted(cite_pairs - link_pairs)
    )
    return {"nodes": nodes, "edges": edges}


def rewrite_links(body: str, path: Path, bundle: Path, concepts: dict) -> str:
    def replace(match: re.Match) -> str:
        label, dest = match.group(1), match.group(2)
        anchor = ""
        bare = dest
        if "#" in dest:
            bare, frag = dest.split("#", 1)
            anchor = "#" + frag
        if not bare or bare.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        target = validate_okf.resolve_md_link(bare, path, bundle)
        if target is None:
            return match.group(0)
        concept = concept_for_path(target, bundle, concepts)
        if concept:
            return f"[{label}]({page_href(concept)}{anchor})"
        if target.is_file():
            try:
                rel = target.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
            except ValueError:
                return match.group(0)
            return f"[{label}]({github_href(rel)}{anchor})"
        return match.group(0)

    return LINK_WITH_LABEL.sub(replace, body)


def render_body(body: str) -> str:
    MD.reset()
    rendered = MD.convert(body)
    return rendered.replace(
        '<a href="http',
        '<a target="_blank" rel="noopener" href="http',
    )


def neighbor_lists(concept: str, edges: list[dict], titles: dict[str, str]) -> str:
    groups = {
        "Links": [edge["target"] for edge in edges if edge["source"] == concept and edge["kind"] == "link"],
        "Also cites": [edge["target"] for edge in edges if edge["source"] == concept and edge["kind"] == "cites"],
        "Linked from": [edge["source"] for edge in edges if edge["target"] == concept],
    }
    parts = []
    for heading, ids in groups.items():
        unique = list(dict.fromkeys(ids))
        if not unique:
            continue
        items = "".join(
            f'<li><a href="{html.escape(page_href(item))}">{html.escape(titles.get(item, item))}</a></li>'
            for item in unique
        )
        parts.append(f"<h2>{heading}</h2><ul>{items}</ul>")
    return "\n".join(parts)


def write_pages(out: Path, concepts: dict, graph: dict, base: str) -> None:
    template = (SITE / "templates" / "page.html").read_text(encoding="utf-8")
    titles = {node["id"]: node["title"] for node in graph["nodes"]}
    by_id = {node["id"]: node for node in graph["nodes"]}
    for concept, (data, body, path) in concepts.items():
        node = by_id[concept]
        rewritten = rewrite_links(body, path, BUNDLE, concepts)
        page = template
        replacements = {
            "@@BASE@@": html.escape(base, quote=True),
            "@@TITLE@@": html.escape(node["title"]),
            "@@TYPE@@": html.escape(str(node["type"])),
            "@@COLOR@@": html.escape(node["color"]),
            "@@TRUST@@": html.escape(node["trust"]),
            "@@STATUS@@": html.escape(str(node["status"])),
            "@@DESCRIPTION@@": html.escape(node["description"]),
            "@@GITHUB@@": html.escape(node["github"], quote=True),
            "@@GRAPH@@": html.escape(f"index.html#{concept}", quote=True),
            "@@BODY@@": render_body(rewritten),
            "@@NEIGHBORS@@": neighbor_lists(concept, graph["edges"], titles),
            "@@GENERATED@@": html.escape(
                " ".join(
                    part
                    for part in [node.get("generated_by") or "", node.get("generated_at") or ""]
                    if part
                )
                or "not recorded"
            ),
        }
        for token, value in replacements.items():
            page = page.replace(token, value)
        destination = out / "pages" / f"{concept}.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(page, encoding="utf-8")


def write_index(out: Path, base: str) -> None:
    template = (SITE / "templates" / "index.html").read_text(encoding="utf-8")
    (out / "index.html").write_text(template.replace("@@BASE@@", html.escape(base, quote=True)), encoding="utf-8")


def copy_static(out: Path) -> None:
    for folder in ("assets", "vendor"):
        source = SITE / folder
        target = out / folder
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)


def check_graph(graph: dict) -> list[str]:
    errors = []
    ids = {node["id"] for node in graph["nodes"]}
    if not ids:
        errors.append("graph has no nodes")
    for edge in graph["edges"]:
        if edge["source"] not in ids or edge["target"] not in ids:
            errors.append(f"dangling edge {edge['source']} -> {edge['target']}")
        if edge["kind"] not in {"link", "cites"}:
            errors.append(f"unknown edge kind {edge['kind']}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the EcoDome knowledge-graph site from wiki/.")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "dist")
    parser.add_argument("--base", default="/cville-ecodome/", help="Site base path. Use / for a local server at the root.")
    args = parser.parse_args()
    base = args.base if args.base.endswith("/") else args.base + "/"
    concepts = load_concepts(BUNDLE.resolve())
    graph = build_graph(concepts, BUNDLE.resolve())
    errors = check_graph(graph)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    out = args.out.resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "graph.json").write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    copy_static(out)
    write_index(out, base)
    write_pages(out, concepts, graph, base)
    print(f"nodes={len(graph['nodes'])} edges={len(graph['edges'])} pages={len(concepts)} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
