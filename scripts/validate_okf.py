#!/usr/bin/env python3
"""Validate the EcoDome wiki as an OKF v0.2 bundle.

OKF conformance (SPEC §11, plus the shape of families in §5 and §10 when
present) is reported separately from this repository's stricter lint.
The lint requires titles, sources, resolved internal links, index
coverage, and a few other maintainer rules documented in AGENTS.md.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install it with: python -m pip install -r requirements-dev.txt", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = REPO_ROOT / "wiki"
RESERVED = {"index.md", "log.md"}
STATUSES = {"draft", "stable", "deprecated"}
OPERATIONS = {
    "Initialization",
    "Ingest",
    "Update",
    "Query",
    "Lint",
    "Deprecation",
    "Creation",
}
ACTOR_RE = re.compile(
    r"^(?:human:[A-Za-z0-9._-]+|process:[A-Za-z0-9._-]+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$"
)
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INDEX_ENTRY_RE = re.compile(r"^\* \[([^\]]+)\]\(([^)]+)\) - (.+)$")
LOG_ENTRY_RE = re.compile(r"^\* \*\*([A-Za-z][A-Za-z ]*)\*\*: .+$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
FOOTNOTE_RE = re.compile(r"\[\^([A-Za-z0-9_-]+)\](?!:)")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([A-Za-z0-9_-]+)\]:", re.MULTILINE)


def split_frontmatter(text: str) -> tuple[dict | None, str, bool]:
    if not text.startswith("---\n"):
        return None, text, False
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    raw = text[4:end]
    body = text[end + 5 :]
    loaded = yaml.safe_load(raw)
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ValueError("frontmatter is not a mapping")
    return loaded, body, True


def parse_time(value: object, label: str, errors: list[str], where: str) -> None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            errors.append(f"{where}: {label} must include a UTC offset")
        return
    if not isinstance(value, str) or not ISO_RE.match(value):
        errors.append(f"{where}: {label} must be an ISO 8601 datetime with a UTC offset")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{where}: {label} is not a real datetime")


def check_actor(value: object, label: str, errors: list[str], where: str) -> None:
    if not isinstance(value, str) or not ACTOR_RE.match(value):
        errors.append(
            f"{where}: {label} must use the OKF actor form "
            "'agent/model', 'human:name', or 'process:name'"
        )


def as_verified_list(value: object) -> list | None:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return value
    return None


def strip_fences(body: str) -> str:
    return FENCE_RE.sub("", body)


def local_target(resource: str, source: Path, bundle: Path) -> Path | None:
    if resource.startswith(("http://", "https://", "mailto:")):
        return None
    if resource.startswith("/"):
        return bundle / resource.lstrip("/")
    return (source.parent / resource).resolve()


def resolve_md_link(destination: str, source: Path, bundle: Path) -> Path | None:
    destination = destination.split("#", 1)[0]
    if not destination or destination.startswith(("http://", "https://", "mailto:")):
        return None
    if destination.startswith("/"):
        return bundle / destination.lstrip("/")
    return (source.parent / destination).resolve()


def iter_markdown(bundle: Path) -> list[Path]:
    return sorted(path for path in bundle.rglob("*.md") if path.is_file())


def validate(bundle: Path) -> list[str]:
    errors: list[str] = []
    bundle = bundle.resolve()
    if not bundle.is_dir():
        return [f"{bundle} is not a directory"]

    concepts: dict[Path, tuple[dict, str]] = {}
    for path in iter_markdown(bundle):
        rel = path.relative_to(bundle).as_posix()
        text = path.read_text(encoding="utf-8")
        try:
            data, body, has_fm = split_frontmatter(text)
        except ValueError as exc:
            errors.append(f"okf: {rel}: {exc}")
            continue

        if path.name in RESERVED:
            if path.name == "index.md":
                errors.extend(check_index(path, bundle, data, body, has_fm))
            else:
                errors.extend(check_log(path, bundle, text, has_fm))
            continue

        if not has_fm or data is None:
            errors.append(f"okf: {rel}: concept is missing YAML frontmatter")
            continue
        concept_type = data.get("type")
        if not isinstance(concept_type, str) or not concept_type.strip():
            errors.append(f"okf: {rel}: frontmatter type must be a non-empty string")
        else:
            errors.extend(check_families(rel, data, body, path, bundle))
            errors.extend(check_project_lint(rel, data, body, path, bundle))
            concepts[path] = (data, body)

    errors.extend(check_indexes_cover_directory(bundle))
    errors.extend(check_index_entries_match(bundle, concepts))
    errors.extend(check_orphans(bundle, concepts))
    return errors


def check_families(rel: str, data: dict, body: str, path: Path, bundle: Path) -> list[str]:
    errors: list[str] = []
    where = f"okf: {rel}"

    if "status" in data and data["status"] not in STATUSES:
        errors.append(f"{where}: status must be draft, stable, or deprecated")
    if "stale_after" in data:
        parse_time(data["stale_after"], "stale_after", errors, where)

    generated = data.get("generated")
    if generated is not None:
        if not isinstance(generated, dict) or "by" not in generated:
            errors.append(f"{where}: generated.by is required when generated is present")
        else:
            check_actor(generated.get("by"), "generated.by", errors, where)
            if "at" in generated:
                parse_time(generated.get("at"), "generated.at", errors, where)

    if "verified" in data:
        events = as_verified_list(data["verified"])
        if events is None:
            errors.append(f"{where}: verified must be a mapping or a list of mappings")
        else:
            for index, event in enumerate(events, start=1):
                if not isinstance(event, dict) or "by" not in event or "at" not in event:
                    errors.append(f"{where}: verified entry {index} needs by and at")
                    continue
                check_actor(event.get("by"), f"verified[{index}].by", errors, where)
                parse_time(event.get("at"), f"verified[{index}].at", errors, where)

    if "sources" in data:
        sources = data["sources"]
        if not isinstance(sources, list):
            errors.append(f"{where}: sources must be a list")
        else:
            for index, source in enumerate(sources, start=1):
                if not isinstance(source, dict) or not isinstance(source.get("resource"), str):
                    errors.append(f"{where}: sources[{index}].resource is required")
                    continue
                if "id" in source and not isinstance(source["id"], str):
                    errors.append(f"{where}: sources[{index}].id must be a string")
                if "last_modified" in source:
                    parse_time(source["last_modified"], f"sources[{index}].last_modified", errors, where)

    if "usage_window" in data:
        window = data["usage_window"]
        if not isinstance(window, dict) or "from" not in window or "to" not in window:
            errors.append(f"{where}: usage_window needs from and to")
        else:
            parse_time(window.get("from"), "usage_window.from", errors, where)
            parse_time(window.get("to"), "usage_window.to", errors, where)

    if data.get("type") == "Attested Computation":
        if not isinstance(data.get("runtime"), str) or not data["runtime"].strip():
            errors.append(f"{where}: Attested Computation requires runtime")
        parameters = data.get("parameters")
        if parameters is not None:
            if not isinstance(parameters, list):
                errors.append(f"{where}: parameters must be a list")
            else:
                for index, parameter in enumerate(parameters, start=1):
                    if not isinstance(parameter, dict) or not {"name", "type", "required"} <= set(parameter):
                        errors.append(f"{where}: parameters[{index}] needs name, type, and required")
        for key in ("executor", "attester"):
            block = data.get(key)
            if block is None:
                continue
            if not isinstance(block, dict) or not isinstance(block.get("resource"), str):
                errors.append(f"{where}: {key}.resource is required when {key} is present")
        computation = data.get("computation")
        if computation is None:
            if not computation_fence(body):
                errors.append(f"{where}: inline Attested Computation needs one fenced block under # Computation")
        elif not isinstance(computation, str):
            errors.append(f"{where}: computation must be a path")

    return errors


def computation_fence(body: str) -> bool:
    match = re.search(r"^# Computation\s*$", body, re.MULTILINE)
    if not match:
        return False
    section = body[match.end() :]
    next_heading = re.search(r"^# ", section, re.MULTILINE)
    if next_heading:
        section = section[: next_heading.start()]
    return len(re.findall(r"```", section)) == 2


def check_project_lint(rel: str, data: dict, body: str, path: Path, bundle: Path) -> list[str]:
    errors: list[str] = []
    where = f"lint: {rel}"
    for key in ("title", "description"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{where}: {key} is required")
        elif key == "description" and "\n" in value:
            errors.append(f"{where}: description must be a single line")
    if data.get("status") not in STATUSES:
        errors.append(f"{where}: status is required (draft, stable, or deprecated)")
    tags = data.get("tags")
    if not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag for tag in tags):
        errors.append(f"{where}: tags must be a non-empty list of strings")
    generated = data.get("generated")
    if not isinstance(generated, dict) or "by" not in generated or "at" not in generated:
        errors.append(f"{where}: generated.by and generated.at are required")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{where}: at least one sources entry is required")
        sources = []

    prose = strip_fences(body)
    cited = set(FOOTNOTE_RE.findall(prose))
    defined = set(FOOTNOTE_DEF_RE.findall(body))
    source_ids = set()
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            continue
        source_id = source.get("id")
        if isinstance(source_id, str):
            source_ids.add(source_id)
        resource = source.get("resource")
        if not isinstance(resource, str):
            continue
        target = local_target(resource, path, bundle)
        if target is None:
            if source.get("sha256"):
                errors.append(f"{where}: sources[{index}].sha256 is set on a URL")
            continue
        if not target.is_file():
            errors.append(f"{where}: sources[{index}].resource does not resolve: {resource}")
            continue
        try:
            target.resolve().relative_to(bundle)
            outside_bundle = False
        except ValueError:
            outside_bundle = True
        digest = source.get("sha256")
        if outside_bundle and not isinstance(digest, str):
            errors.append(f"{where}: raw file source {resource} needs sha256")
        elif isinstance(digest, str) and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            errors.append(f"{where}: sha256 does not match {resource}")

    unknown = sorted(cited - source_ids)
    if unknown:
        errors.append(f"{where}: footnotes do not match sources ids: {', '.join(unknown)}")
    missing_defs = sorted(cited - defined)
    if missing_defs:
        errors.append(f"{where}: footnotes missing definitions: {', '.join(missing_defs)}")
    uncited = sorted(source_ids - cited)
    if uncited:
        errors.append(f"{where}: sources ids never cited: {', '.join(uncited)}")

    for destination in LINK_RE.findall(prose):
        target = resolve_md_link(destination, path, bundle)
        if target is None:
            continue
        if not target.exists():
            errors.append(f"{where}: broken link ({destination})")

    for key in ("executor", "attester"):
        block = data.get(key)
        if isinstance(block, dict) and isinstance(block.get("resource"), str):
            target = local_target(block["resource"], path, bundle)
            if target is not None and not target.exists():
                errors.append(f"{where}: {key}.resource does not resolve: {block['resource']}")
    computation = data.get("computation")
    if isinstance(computation, str):
        target = local_target(computation, path, bundle)
        if target is not None and not target.is_file():
            errors.append(f"{where}: computation does not resolve: {computation}")
    return errors


def check_index(path: Path, bundle: Path, data: dict | None, body: str, has_fm: bool) -> list[str]:
    rel = path.relative_to(bundle).as_posix()
    errors: list[str] = []
    is_root = path.parent == bundle
    if is_root:
        if not has_fm or data is None:
            errors.append(f"okf: {rel}: bundle-root index must declare okf_version")
        else:
            extra = set(data) - {"okf_version"}
            if extra:
                errors.append(f"okf: {rel}: root index frontmatter may only contain okf_version")
            version = data.get("okf_version")
            if version not in {"0.2", 0.2}:
                errors.append(f"okf: {rel}: okf_version must be \"0.2\"")
    elif has_fm:
        errors.append(f"okf: {rel}: only the bundle-root index may have frontmatter")
    errors.extend(check_links_exist(path, bundle, body, f"lint: {rel}"))
    return errors


def check_log(path: Path, bundle: Path, text: str, has_fm: bool) -> list[str]:
    rel = path.relative_to(bundle).as_posix()
    errors: list[str] = []
    if has_fm:
        errors.append(f"okf: {rel}: log files do not have frontmatter")
    dates: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            date = line[3:].strip()
            if not DATE_RE.match(date):
                errors.append(f"okf: {rel}:{line_number}: date headings must be YYYY-MM-DD")
            else:
                dates.append(date)
        elif line.startswith("* "):
            match = LOG_ENTRY_RE.match(line)
            if not match:
                errors.append(f"lint: {rel}:{line_number}: log bullet must start with **Operation**:")
            elif match.group(1) not in OPERATIONS:
                errors.append(f"lint: {rel}:{line_number}: unknown log operation {match.group(1)}")
    if dates != sorted(dates, reverse=True):
        errors.append(f"okf: {rel}: date sections must be newest first")
    if len(dates) != len(set(dates)):
        errors.append(f"okf: {rel}: duplicate date headings")
    errors.extend(check_links_exist(path, bundle, text, f"lint: {rel}"))
    return errors


def check_links_exist(path: Path, bundle: Path, text: str, where: str) -> list[str]:
    errors = []
    for destination in LINK_RE.findall(strip_fences(text)):
        target = resolve_md_link(destination, path, bundle)
        if target is not None and not target.exists():
            errors.append(f"{where}: broken link ({destination})")
    return errors


def check_indexes_cover_directory(bundle: Path) -> list[str]:
    errors: list[str] = []
    directories = [bundle] + sorted(path for path in bundle.rglob("*") if path.is_dir())
    for directory in directories:
        concepts = sorted(
            path.name for path in directory.glob("*.md") if path.name not in RESERVED
        )
        subdirs = sorted(path.name for path in directory.iterdir() if path.is_dir() and not path.name.startswith("."))
        needs_index = bool(concepts or subdirs)
        index = directory / "index.md"
        if needs_index and not index.exists():
            rel = directory.relative_to(bundle).as_posix()
            errors.append(f"lint: {rel or '.'}: directory needs an index.md")
            continue
        if not index.exists():
            continue
        listed = index_targets(index)
        for name in concepts:
            if name not in listed and f"./{name}" not in listed:
                rel = (directory / name).relative_to(bundle).as_posix()
                errors.append(f"lint: {rel}: not listed in {index.relative_to(bundle).as_posix()}")
        for name in subdirs:
            if f"{name}/" not in listed and f"{name}/index.md" not in listed:
                errors.append(
                    f"lint: {index.relative_to(bundle).as_posix()}: missing subdirectory entry {name}/"
                )
    return errors


def index_targets(index: Path) -> set[str]:
    targets = set()
    for line in index.read_text(encoding="utf-8").splitlines():
        match = INDEX_ENTRY_RE.match(line)
        if match:
            targets.add(match.group(2))
    return targets


def check_index_entries_match(bundle: Path, concepts: dict[Path, tuple[dict, str]]) -> list[str]:
    errors: list[str] = []
    by_rel = {path.relative_to(bundle).as_posix(): data for path, (data, _) in concepts.items()}
    for index in bundle.rglob("index.md"):
        for line_number, line in enumerate(index.read_text(encoding="utf-8").splitlines(), start=1):
            match = INDEX_ENTRY_RE.match(line)
            if not match:
                if line.startswith("* "):
                    errors.append(
                        f"lint: {index.relative_to(bundle).as_posix()}:{line_number}: "
                        "index bullet must be '* [Title](target) - description'"
                    )
                continue
            title, target, description = match.groups()
            if target.endswith("/") or target.endswith("/index.md"):
                directory = (index.parent / target).resolve()
                if not directory.is_dir():
                    errors.append(
                        f"lint: {index.relative_to(bundle).as_posix()}:{line_number}: "
                        f"missing directory {target}"
                    )
                continue
            concept_path = (index.parent / target).resolve()
            try:
                rel = concept_path.relative_to(bundle).as_posix()
            except ValueError:
                errors.append(
                    f"lint: {index.relative_to(bundle).as_posix()}:{line_number}: "
                    f"{target} is outside the bundle"
                )
                continue
            data = by_rel.get(rel)
            if data is None:
                if not concept_path.is_file():
                    errors.append(
                        f"lint: {index.relative_to(bundle).as_posix()}:{line_number}: "
                        f"missing concept {target}"
                    )
                continue
            if title != data.get("title"):
                errors.append(
                    f"lint: {rel}: index title {title!r} != frontmatter title {data.get('title')!r}"
                )
            if description != data.get("description"):
                errors.append(
                    f"lint: {rel}: index description does not match frontmatter description"
                )
    return errors


def check_orphans(bundle: Path, concepts: dict[Path, tuple[dict, str]]) -> list[str]:
    inbound = {path: 0 for path in concepts}
    for path, (_, body) in concepts.items():
        for destination in LINK_RE.findall(strip_fences(body)):
            target = resolve_md_link(destination, path, bundle)
            if target in inbound and target != path:
                inbound[target] += 1
    errors = []
    for path, count in inbound.items():
        if count == 0:
            errors.append(f"lint: {path.relative_to(bundle).as_posix()}: no inbound concept link")
    return errors


def self_test() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        bundle = root / "wiki"
        (bundle / "notes").mkdir(parents=True)
        (bundle / "index.md").write_text(
            "---\nokf_version: \"0.2\"\n---\n\n# Demo\n\n# Notes\n\n"
            "* [Notes](notes/) - Nested notes.\n",
            encoding="utf-8",
        )
        (bundle / "log.md").write_text(
            "# Directory Update Log\n\n## 2026-11-23\n* **Initialization**: Created the fixture.\n",
            encoding="utf-8",
        )
        (bundle / "notes" / "index.md").write_text(
            "# Notes\n\n"
            "* [Hello](hello.md) - A greeting concept.\n"
            "* [Echo](echo.md) - A reply concept.\n",
            encoding="utf-8",
        )
        hello = (
            "---\n"
            "type: Note\n"
            "title: Hello\n"
            "description: A greeting concept.\n"
            "status: draft\n"
            "tags: [demo]\n"
            "generated: { by: cursor-cloud-agent/grok-4.7, at: \"2026-11-23T00:00:00Z\" }\n"
            "sources:\n"
            "  - { id: spec, resource: https://example.com/spec, title: Spec }\n"
            "---\n\nSee the [echo](echo.md) and the [spec](https://example.com/spec).[^spec]\n\n"
            "[^spec]: Spec\n"
        )
        echo = hello.replace("type: Note", "type: Reply").replace("title: Hello", "title: Echo").replace(
            "description: A greeting concept.", "description: A reply concept."
        ).replace("[echo](echo.md)", "[hello](hello.md)")
        (bundle / "notes" / "hello.md").write_text(hello, encoding="utf-8")
        (bundle / "notes" / "echo.md").write_text(echo, encoding="utf-8")
        good = validate(bundle)
        if good:
            failures.append("valid fixture failed: " + "; ".join(good))

        broken = bundle / "notes" / "hello.md"
        broken.write_text(broken.read_text(encoding="utf-8").replace("type: Note\n", ""))
        if not any("type" in error for error in validate(bundle)):
            failures.append("missing type was accepted")

        broken.write_text(
            "---\n"
            "type: Note\n"
            "title: Hello\n"
            "description: A greeting concept.\n"
            "status: draft\n"
            "tags: [demo]\n"
            "generated: { by: cursor-cloud-agent/grok-4.7, at: \"2026-11-23T00:00:00Z\" }\n"
            "sources:\n"
            "  - { id: spec, resource: https://example.com/spec, title: Spec }\n"
            "---\n\n[Missing](/missing.md).[^spec]\n\n[^spec]: Spec\n",
            encoding="utf-8",
        )
        if not any("broken link" in error for error in validate(bundle)):
            failures.append("broken link was accepted")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the EcoDome OKF wiki.")
    parser.add_argument("--bundle", type=Path, default=BUNDLE_ROOT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        failures = self_test()
        if failures:
            print("\n".join(failures))
            return 1
        print("self-test passed")
        return 0
    errors = validate(args.bundle)
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} error(s)")
        return 1
    concept_count = sum(1 for path in iter_markdown(args.bundle) if path.name not in RESERVED)
    print(f"OKF bundle {args.bundle} conforms ({concept_count} concepts, internal links resolve)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
