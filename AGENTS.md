# EcoDome wiki maintainer schema

This file is the schema for the EcoDome Charlottesville knowledge wiki. Agents that ingest a source, answer a question, or lint the wiki follow it. Humans read [README.md](README.md) and browse [wiki/index.md](wiki/index.md).

The pattern comes from Andrej Karpathy's [LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): immutable raw sources, an LLM-maintained wiki, and this schema. The file format is [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Where the two overlap, OKF governs format and Karpathy governs workflow.

## Layers

| Layer | Path | Who writes it |
| --- | --- | --- |
| Raw sources | `raw/` | Humans add files. Agents never edit a file after it is filed. |
| OKF bundle | `wiki/` | Agents. Every non-reserved `.md` file is a concept. |
| Schema | `AGENTS.md` | Humans and agents together, when the workflow itself should change. |

`wiki/index.md` and `wiki/log.md` are reserved OKF files, not concepts. The same reservation applies in every subdirectory.

## Public repository

The repository is public. Concept pages carry project facts only.

- Refer to people by first name and role when a source makes that role relevant. Do not add surnames, contact details, account names, addresses, or private locations.
- Do not identify people shown in photographs, including the presentation PDF.
- Do not copy personal quotations. Slide headlines that are the project's own lines may be quoted. A personal mission statement may not.
- Do not transcribe phone numbers, even from a vendor credit.
- If a raw note contains a private-household or minor's detail, leave it out of concept pages. Say in the log that it was omitted. Do not "fix" that by editing the raw file later; file a redacted successor and record the reason.
- Do not invent dates, dimensions, budgets, citations, or URLs. A gap belongs on [wiki/questions/open-questions.md](wiki/questions/open-questions.md).

## Concept format

Each concept is UTF-8 Markdown with YAML frontmatter. `type` is required by OKF. This wiki also requires:

- `title` and a one-sentence `description` (the description is copied into the parent `index.md`)
- `status`: `draft`, `stable`, or `deprecated`. New and unreviewed pages are `draft`. Absent status would mean `stable` under OKF, so set it explicitly.
- `tags`: a non-empty list
- `generated.by` and `generated.at`. Use the actor form `agent/model` (for example `cursor-cloud-agent/grok-4.7`), `human:firstname`, or `process:name`. Timestamps are ISO 8601 with a `Z` offset.
- `sources`: at least one entry. `resource` is a URL, a bundle-absolute path such as `/sources/ears-spec.md`, or a relative path to a raw file. Give each entry an `id`, and cite it with a Markdown footnote whose label is that id.
- `stale_after` when the fact is time-bound or still a proposal. An absolute instant, not a duration.
- `resource` when one URL is the thing the concept describes.

Do not set `verified` until a person or a deterministic process has actually checked the page. Unverified is an honest trust tier. A human review looks like:

```yaml
verified: { by: human:firstname, at: "2026-11-23T00:00:00Z" }
```

A local file source (anything that is not a `.md` concept or a URL) has a `sha256` of its bytes. Source-summary pages are the only concepts that point at `raw/`. Other concepts point at those summaries with `resource: /sources/<id>.md`, so lineage stays inside the bundle.

Concept-to-concept links use OKF bundle-absolute paths: `[April 2027 pilot](/pilot/april-2027.md)`. Index entries use relative links, because OKF indexes are directory listings: `* [Title](page.md) - The description field, copied exactly.`

Type values used here:

| `type` | Use |
| --- | --- |
| `Project` | The effort as a whole |
| `Venue` | A place |
| `Structure` | The physical dome and its dimensions |
| `Experience` | Immersive content and programs |
| `Pilot` | The proposed April 2027 showcase |
| `Budget` | Fundraising figures and sponsor terms |
| `Reference` | Research claims, and the note on how to run a computation |
| `Tool` | An external tool |
| `Product` | The spatial simulator as a product |
| `Architecture` | Simulator structure and states |
| `Requirement Set` | A group of EARS requirements |
| `Prototype` | A build or demonstration that exists |
| `Value` | Community preferences and funding posture |
| `Plan` | Gathering and cadence |
| `Organization` | A legal entity or a set of public roles |
| `Timeline` | A dated public record |
| `Event` | A documented gathering |
| `Media` | Coverage and the lack of it |
| `Comparable` | An existing venue that is not this project |
| `Question` | Open questions and leads |
| `Source Summary` | A filed raw source |
| `Attested Computation` | A sanctioned calculation |

`Attested Computation` follows OKF §10: `runtime`, `parameters`, `executor.resource`, `attester.resource`, and one fenced Python block under `# Computation`. The agent supplies parameter values only. It does not rewrite the fenced code to make a number come out right. Change the computation only when the source figure changes, then re-run the attester.

## Ingest

1. File the original in `raw/` under a stable name. Do not modify it after this step. Record SHA-256.
2. Read the whole source. For a slide deck, render the pages and read the images. A text extract of this deck is not the source.
3. Write or update `wiki/sources/<source>.md` (`type: Source Summary`) with scope, date, and where each claim went.
4. Update every concept the source confirms, contradicts, or extends. A single source should touch the entities it actually speaks about, not a copy of the source pasted into one page.
5. When sources disagree, keep both claims, name both sources, and add the tension to the open-questions page. Do not pick a silent winner.
6. Refresh each affected `index.md` so every sibling concept and subdirectory is listed, with the concept's `title` and `description` copied exactly.
7. Add a log entry. Do not rewrite older entries.
8. Run `python scripts/validate_okf.py` and the attesters in `.github/workflows/okf.yml`.

## Query

1. Read `wiki/index.md`, then the `index.md` of the relevant section, then the concepts. The indexes are the catalog. Do not start from `raw/` unless a concept's sources are insufficient or contradicted.
2. Answer with the concept paths you used and the source ids behind them. Say when a page is `draft`, past `stale_after`, or unverified.
3. File a useful answer back into the wiki: a new concept or an update, plus index and log (`**Query**`). A comparison or synthesis that only lives in chat is a dropped source.

## Lint

Check, and fix what is mechanical:

- Contradictions between concepts, and claims a newer source has superseded. Mark the old claim; do not delete the history from the log.
- `stale_after` instants that have passed.
- Concepts with no inbound link from another concept, and important entities mentioned but lacking a page.
- Index entries that drift from `title` or `description`.
- Broken internal links and footnote ids that do not match `sources`.
- Raw files whose bytes no longer match `sha256` (someone edited an immutable source).
- Gaps that a public, project-level source could fill. Record the gap; do not fill it with an unsourced search result presented as project fact.

OKF consumers must tolerate broken links. This repository's lint does not: `scripts/validate_okf.py` fails the check. That is a maintainer rule, not a change to OKF.

Log a lint pass with `**Lint**`.

## Index and log

Indexes are progressive disclosure (OKF §8). The root index lists the root concept and the sections. Each section index lists that directory. Do not also maintain a second flat catalog; it will drift. An agent answering a question walks the indexes.

`wiki/log.md` is the append-only history in OKF §9 form: a `# Directory Update Log` heading, then `## YYYY-MM-DD` sections, newest first. Inserting a new day at the top is the append. Do not sort the file oldest-first and do not rewrite a past bullet. Bullets start with a bold operation so they can be grepped:

```text
grep '^\* \*\*Ingest\*\*' wiki/log.md
```

Operations: `Initialization`, `Ingest`, `Update`, `Query`, `Lint`, `Deprecation`, `Creation`.

Karpathy's `## [YYYY-MM-DD] ingest | Title` prefix is the same idea. OKF's date heading plus the bold operation is the form this repo uses.

## Commands

```bash
python scripts/validate_okf.py
python scripts/validate_okf.py --self-test
python wiki/references/attesters/feet-to-meters.py
python wiki/references/attesters/pilot-budget.py
```

`PyYAML` is the only dependency (`requirements-dev.txt`). GitHub Actions runs the same commands.
