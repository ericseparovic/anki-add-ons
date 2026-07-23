# Changelog

## Unreleased

### Changed

- Disabled `$...$` as a KaTeX delimiter to avoid breaking normal text such as `$500`, `$HOME`, shell scripts, PHP, and jQuery.
- Changed final card rendering to process Markdown before KaTeX and ignore KaTeX inside `pre` and `code`.
- Preserved Cloze spans while cleaning pasted HTML.
- Added Catppuccin light/dark card styling and Highlight.js styling.
- Migrated editor integration to modern Anki hooks and APIs.
- Updated final card templates to use only bundled local resources, with no CDN fallback.
- Updated media resource copying so bundled files replace stale media-folder copies safely.
- Removed broad media-folder deletes from `update()`.
- Refactored final card templates through a shared Python builder and moved card CSS to `_card.css`.
- Kept `html:true` enabled to preserve existing behavior.
- Evaluated `editor.web.eval` and kept it because the current preview works on Anki 26.05 and no concrete replacement is required.

### Added

- `README.md` with development install, compatibility notes, and project structure.
- `ROADMAP.md` with current phase status and next work.
- `TESTING.md` with manual regression checks.
- `tests/test_render_contract.py` with automated render-contract checks.
