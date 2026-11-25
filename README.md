# EcoDome Charlottesville knowledge wiki

This repository is a public, LLM-maintained wiki for the [EcoDome Charlottesville](wiki/project.md) project: a proposed immersive dome, the April 2027 pilot described in the community deck, and the spatial-simulator specification.

It follows Andrej Karpathy's [LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern and stores the wiki in [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). OKF decides the file format. The pattern decides the workflow: raw sources stay immutable, and agents compile them into interlinked concept pages.

The pages are a starting synthesis. They are `draft` and unverified until a person checks them. Trust is recorded in frontmatter, not implied by the prose.

A generated graph of the same pages is published from `main` at <https://agento3.github.io/cville-ecodome/>. It is rebuilt by `scripts/build_site.py` whenever the wiki changes. Do not edit the graph by hand.

## Layout

```text
raw/          Immutable sources. Agents read them and do not edit them.
wiki/         OKF bundle. Start at wiki/index.md.
  index.md    Section catalog. The root file declares okf_version.
  log.md      Append-only history, newest day first.
AGENTS.md     Instructions for agents: ingest, query, and lint.
scripts/validate_okf.py
```

| Source | Filed as |
| --- | --- |
| Spatial Simulator EARS specification, v1.0 | `raw/ecodome-spatial-simulator-ears-v1.0.txt` |
| Community notes, November 2026 | `raw/ecodome-charlottesville-context-2026-11.md` |
| AI Explorers slide deck (24 pages) | `raw/ecodome-ai-explorers-presentation.pdf` |
| Official site, accessed 2026-11-23 | `raw/ecodome-official-site-2026-11-23.md` |
| CanvasRebel founder interview, April 10, 2025 | `raw/canvasrebel-founder-interview-2025-04-10.md` |
| Alignable listing, accessed 2026-11-23 | `raw/alignable-ecodome-cville-2026-11-23.md` |
| Virginia compilation, Ecodome Cville, LLC | `raw/opencorpdata-ecodome-cville-llc-2026-11-23.md` |
| Virginia compilation, Ecodome Foundation | `raw/opencorpdata-ecodome-foundation-2026-11-23.md` |
| IX Art Park website, accessed 2026-11-23 | `raw/ix-art-park-website-2026-11-23.md` |
| C-VILLE Weekly note on the IX Nest exhibit, 2016 | `raw/cville-weekly-ix-nest-2016.md` |
| Spatial-simulator prototype links, 2026-11-23 | `raw/simulator-prototype-links-2026-11-23.md` |

The deck is also published as [Google Slides](https://docs.google.com/presentation/d/1_2WxQJjcp8bBibTe3YFr8n5Iuy0UZx7G6TorSFdZV4M). The PDF is in `raw/` so the wiki still has the deck if that link changes. It is about 7.2 MB, under GitHub's file limit. Most of the type is in the images; the wiki was written by reading the rendered slides.

Concept links in page bodies are file-relative and include `.md`, so GitHub can open them. Frontmatter `sources.resource` stays bundle-absolute, such as `/sources/ears-spec.md`, because that field is for agents rather than GitHub's renderer. The indexes use ordinary relative links.

## How to contribute

People curate sources and ask questions. Agents do the bookkeeping.

1. Add an original file under `raw/`. Leave filed files unchanged.
2. Ask an agent to ingest it. The agent follows [AGENTS.md](AGENTS.md): summarize the source, update the concepts it affects, refresh the indexes, and append `wiki/log.md`.
3. Ask questions in natural language. A good answer is filed back into `wiki/` so the next person does not start from the raw files.
4. Ask for a lint pass when pages might have drifted. The agent looks for contradictions, stale dates, orphan pages, and missing links.

Keep the repository public-safe. Concept pages use project facts, first names, and roles. They do not add surnames, contact details, private locations, or personal quotations, and they do not identify people in photographs. Details of that rule are in AGENTS.md.

No license is set for this repository yet.

## Checks

OKF's own conformance rules are permissive about broken links. This repo's check is stricter: frontmatter, indexes, the log, source hashes, and internal links must all hold.

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_okf.py
python wiki/references/attesters/feet-to-meters.py
python wiki/references/attesters/pilot-budget.py
```

GitHub Actions runs the same commands on every push and pull request. The two attesters re-run the sanctioned calculations for the 50-foot baseline (15.24 m) and the deck's $175,000 budget sum.

## Reading the wiki

Open [wiki/index.md](wiki/index.md) and follow a section. The project overview is [wiki/project.md](wiki/project.md). The April 2027 pilot, the dome dimensions, the spatial simulator, the prototypes, and the open questions each have their own pages.
