# Markdown and KaTeX Support

Anki add-on that provides note types with Markdown, KaTeX, Highlight.js code blocks, mhchem support, and Cloze-compatible rendering.

This repository is the development copy. The original installed add-on must not be edited directly.

## Note Types

- `KaTeX and Markdown Basic`
- `KaTeX and Markdown Cloze`

## Supported Syntax

Markdown features include headings, lists, tables, links, blockquotes, inline code, fenced code blocks, embedded HTML, and `==marked text==`.

KaTeX delimiters enabled by default:

```text
$$...$$
\(...\)
\[...\]
```

`$...$` is intentionally disabled because it conflicts with normal text such as `$500`, `$HOME`, shell scripts, PHP, and jQuery.

## Development Install

The development add-on is installed through this symlink:

```text
~/.local/share/Anki2/addons21/markdownkatexdev -> /home/erichy/Work/anki-markdown-katex-improved
```

Start Anki from a terminal while testing:

```bash
anki
```

Expected add-on path in Anki:

```text
addons21/markdownkatexdev
```

## Compatibility

- Tested with Anki `26.05`.
- Metadata targets modern Anki with `min_point_version: 20`.
- Editor assets are exported through `/_addons/...` to comply with Anki's Content Security Policy.
- The editor preview uses `aqt.gui_hooks` and modern note/model APIs.

## Bundled Dependencies

- Current bundled versions are legacy versions kept for stability.
- A direct upgrade to newer KaTeX, markdown-it, Highlight.js, markdown-it-mark, and mhchem builds broke rendering and was reverted.
- Dependency upgrades should be handled one library at a time with manual Anki validation.

## Current Design Decisions

- Keep existing note type names for now: `KaTeX and Markdown Basic` and `KaTeX and Markdown Cloze`.
- Do not rename note types to `KaTeX and Markdown Improved` yet, because existing notes and templates may depend on the current names.
- If renaming is desired later, it should be handled as a separate migration task.
- Keep `html:true` enabled to preserve existing behavior; disabling it would be a separate breaking-change decision.
- Final card templates load bundled local resources only; CDN fallback was removed to preserve offline behavior and privacy.

## Manual Testing

Use `TESTING.md` after changes to templates, rendering order, CSS, bundled assets, or editor preview behavior.

Developer checks before committing:

```bash
python -m py_compile HTMLandCSS.py __init__.py
python -m unittest discover -s tests
python -m json.tool meta.json
git diff --check
```

## Important Files

- `__init__.py`: Anki hooks, model creation/update, editor preview injection, media asset copying.
- `HTMLandCSS.py`: editor preview JavaScript, card-template generation, and shared render helpers.
- `_card.css`: card CSS injected into Anki note types through `model['css']`.
- `_highlight.css`: Catppuccin Highlight.js theme.
- `CHANGELOG.md`: unreleased change summary.
- `tests/test_render_contract.py`: automated render-contract checks for sensitive behavior.
- `TESTING.md`: manual regression checklist.
- `ROADMAP.md`: current implementation roadmap.
- `palanificacion.md`: historical planning and project analysis.

## Known Remaining Work

- Continue separating editor preview code if a future change requires it.
- Update bundled dependencies one library at a time with regression testing.
- Expand automated tests when dependency updates add new edge cases.
- Prepare release/package only when requested.
