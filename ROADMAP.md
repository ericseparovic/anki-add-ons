# Roadmap

This is the current working roadmap. `palanificacion.md` keeps the longer historical analysis.

## Phase 1: Development Base

Status: complete.

Purpose:

- Keep development separate from the original installed add-on.
- Document installation, usage, compatibility decisions, and remaining work.
- Decide whether model names should change.

Completed:

- Development symlink uses `markdownkatexdev`.
- Original installed add-on remains out of scope.
- `TESTING.md` exists with manual regression checks.
- `README.md` documents install, usage, compatibility, and current decisions.
- `ROADMAP.md` exists as the current short-form plan.
- Model naming decision: keep current names for now to avoid migration risk.

Remaining:

- None for Phase 1.

Recommendation:

- Do not rename note types until there is a dedicated migration plan.

## Phase 2: Critical Render Bugs

Status: complete.

Purpose:

- Fix rendering behavior that breaks normal notes.
- Make Markdown, KaTeX, code blocks, dark mode, and Cloze work together.

Completed:

- Disabled `$...$` as a KaTeX delimiter.
- Kept `$$...$$`, `\(...\)`, and `\[...\]` delimiters.
- Changed render order to Markdown first, KaTeX second.
- Prevented KaTeX from rendering inside `pre` and `code`.
- Preserved `span.cloze`.
- Added Catppuccin light/dark styling.

Remaining:

- None for Phase 2.

## Phase 3: Maintainability

Status: partial.

Purpose:

- Reduce duplication and make future fixes safer.

Completed:

- Extracted shared card-render helpers.
- Fixed the `replace` without assignment bug.
- Reduced implicit globals in the editor preview.
- Prevented duplicate preview listeners.

Remaining:

- Refactor `HTMLandCSS.py` more deeply.
- Split large embedded strings into smaller, maintainable modules or assets.
- Improve paste cleanup, which is still regex-based.

Recommendation:

- Do this after resources/security work, because it is larger and riskier.

## Phase 4: Modern Anki Compatibility

Status: partial.

Purpose:

- Keep the add-on working on modern Anki versions.

Completed:

- Migrated legacy hooks to `aqt.gui_hooks`.
- Updated `meta.json` compatibility.
- Replaced deprecated `byName` and `note.model()` APIs.
- Fixed editor preview Content Security Policy errors by using `/_addons/...` assets.
- Fixed KaTeX font paths in the editor preview.
- Made editor preview support more than two fields.
- Editor preview now uses real field names.

Remaining:

- Evaluate whether `editor.web.eval` can be replaced with a more stable editor integration.

Recommendation:

- Keep `editor.web.eval` for now unless it causes a concrete bug. The current behavior works on Anki 26.05.

## Phase 5: Resources, Dependencies, And Security

Status: partial.

Purpose:

- Improve offline behavior, resource management, and security posture.

Completed:

- Removed CDN fallback from final card templates; cards now load bundled local resources only.
- Improved `_add_file()` so bundled media resources replace stale copies safely.

Remaining:

- Avoid broad `shutil.rmtree()` deletes unless strictly needed.
- Define a versioning strategy for copied media resources.
- Decide whether `html:true` should stay enabled, become configurable, or be disabled.
- Decide whether `$...$` should be configurable for compatibility mode.
- Update KaTeX, markdown-it, Highlight.js, and mhchem with regression testing.

Recommendation:

- Continue by avoiding broad deletes. It is concrete, high-value, and easier to verify than dependency upgrades.

## Phase 6: Tests And Release Prep

Status: pending.

Purpose:

- Make changes safer and prepare for publishing or packaging.

Remaining:

- Add automated tests for render-sensitive transformations.
- Create a changelog.
- Finalize manual testing instructions.
- Prepare release/package only when requested.

Minimum automated test cases:

```text
$500 remains literal
$HOME remains literal
$(command) remains literal
$x+1$ is not math unless compatibility mode exists and is enabled
Fenced bash code with $HOME does not render KaTeX
{{c1::text}} preserves .cloze
==marked text== renders as mark
Editor preview assets do not trigger CSP errors
KaTeX fonts resolve under /_addons/.../fonts in preview
```

## Recommended Next Work

1. Phase 5 resources: avoid broad `shutil.rmtree()` deletes.
2. Phase 5 security: decide `html:true` policy.
3. Phase 3 refactor: split `HTMLandCSS.py` after behavior is stable.
4. Phase 6 tests: add automated coverage for rendering edge cases.
5. Phase 5 dependencies: update bundled libraries with regression checks.
