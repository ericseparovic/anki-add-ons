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
- Generated final card templates from a shared Python builder.
- Moved card CSS out to `_card.css` while keeping Anki model CSS updates unchanged.

Remaining:

- Improve paste cleanup, which is still regex-based.
- Consider separating editor preview JavaScript if future changes make it necessary.

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
- Evaluated `editor.web.eval`; keep it for now because it works on Anki 26.05 and no safer editor-specific replacement is needed without a concrete bug.

Remaining:

- None for current compatibility scope.

Recommendation:

- Revisit editor integration only if Anki changes the editor DOM/API or a concrete preview bug appears.

## Phase 5: Resources, Dependencies, And Security

Status: partial.

Purpose:

- Improve offline behavior, resource management, and security posture.

Completed:

- Removed CDN fallback from final card templates; cards now load bundled local resources only.
- Improved `_add_file()` so bundled media resources replace stale copies safely.
- Removed broad `shutil.rmtree()` media-folder deletes from `update()`.
- Kept `html:true` enabled to preserve existing behavior.

Remaining:

- Define a versioning strategy for copied media resources.
- Decide whether `$...$` should be configurable for compatibility mode.
- Update bundled dependencies one library at a time with manual Anki validation.

Recommendation:

- Continue by updating bundled dependencies one library at a time, starting with the lowest-risk library.

## Phase 6: Tests And Release Prep

Status: partial.

Purpose:

- Make changes safer and prepare for publishing or packaging.

Remaining:

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

Completed:

- Added automated render-contract tests for resource loading, math delimiters, code-block protection, Cloze preservation, mark support, dark mode CSS, preview exports, template fields, and media-delete safety.
- Created initial `CHANGELOG.md`.

## Recommended Next Work

1. Phase 5 dependencies: update bundled libraries one at a time with manual Anki validation.
2. Phase 5 resources: decide whether copied media resources need explicit versioning.
3. Phase 6 release prep: finalize manual testing instructions.
