import unittest
from pathlib import Path

import HTMLandCSS


ROOT = Path(__file__).resolve().parents[1]


class RenderContractTests(unittest.TestCase):
    def test_card_templates_load_only_local_resources(self):
        for template in (
            HTMLandCSS.front,
            HTMLandCSS.back,
            HTMLandCSS.front_cloze,
            HTMLandCSS.back_cloze,
        ):
            self.assertIn('getScript("_katex.min.js")', template)
            self.assertIn('getScript("_markdown-it.min.js")', template)
            self.assertIn('getScript("_mhchem.js")', template)
            self.assertNotIn('https://', template)

    def test_dollar_delimiter_is_not_enabled(self):
        for template in (
            HTMLandCSS.HTMLforEditor,
            HTMLandCSS.front,
            HTMLandCSS.back,
            HTMLandCSS.front_cloze,
            HTMLandCSS.back_cloze,
        ):
            self.assertIn('{left: "$$", right: "$$", display: true}', template)
            self.assertIn('{left: "\\\\(", right: "\\\\)", display: false}', template)
            self.assertIn('{left: "\\\\[", right: "\\\\]", display: true}', template)
            self.assertNotIn('{left: "$", right: "$"', template)

    def test_katex_ignores_code_blocks(self):
        expected = 'ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]'
        self.assertIn(expected, HTMLandCSS.HTMLforEditor)
        self.assertIn(expected, HTMLandCSS.front)

    def test_markdown_mark_plugin_is_enabled(self):
        for template in (HTMLandCSS.HTMLforEditor, HTMLandCSS.front):
            self.assertIn('.use(markdownItMark)', template)
            self.assertIn('html:true', template)

    def test_cloze_span_cleanup_preserves_cloze_class(self):
        pattern = r'<span\(\?!\[\^>\]\*class=\["\'\]\[\^"\'\]\*\\bcloze\\b'
        self.assertRegex(HTMLandCSS.front, pattern)
        self.assertIn('{{cloze:Text}}', HTMLandCSS.front_cloze)
        self.assertIn('{{cloze:Text}}', HTMLandCSS.back_cloze)

    def test_card_css_keeps_dark_mode_and_mark_styles(self):
        css = HTMLandCSS.css
        self.assertIn('.nightMode.card', css)
        self.assertIn('.nightMode .cloze', css)
        self.assertIn('mark {', css)
        self.assertIn('.cloze {', css)
        self.assertIn('code {', css)

    def test_preview_uses_addon_exports_and_no_cdn(self):
        preview = HTMLandCSS.HTMLforEditor
        self.assertIn('__ADDON_WEB_PATH__/_katex.css', preview)
        self.assertIn('__ADDON_WEB_PATH__/_highlight.js', preview)
        self.assertIn('__ADDON_WEB_PATH__/fonts/_', preview)
        self.assertNotIn('https://', preview)

    def test_preview_clears_when_fields_are_empty(self):
        preview = HTMLandCSS.HTMLforEditor
        self.assertIn('clearPreview();', preview)
        self.assertIn('area.innerHTML = "";', preview)
        self.assertIn('area.style.visibility = "hidden";', preview)

    def test_preview_uses_manual_button(self):
        preview = HTMLandCSS.HTMLforEditor
        init_py = (ROOT / '__init__.py').read_text(encoding='utf-8')
        self.assertIn('gui_hooks.editor_did_init_buttons.append(add_markdown_preview_button)', init_py)
        self.assertIn('editor.addButton(', init_py)
        self.assertIn('label="Preview"', init_py)
        self.assertIn('id="markdown-preview-button"', init_py)
        self.assertIn('window.markdownPreviewRender = updatePreview;', preview)
        self.assertIn('window.markdownPreviewPendingText = null;', preview)
        self.assertIn('window.markdownPreviewRender(window.markdownPreviewPendingText);', preview)
        self.assertIn('var previewParent = document.body;', preview)
        self.assertIn('markdownPreview(editor)', init_py)
        self.assertIn('for field_name, value in editor.note.items():', init_py)
        self.assertIn('parts.append(value)', init_py)
        self.assertNotIn('parts.append(f"# {field_name}', init_py)
        self.assertIn('window.markdownPreviewPendingText = {json.dumps(text)};', init_py)
        self.assertIn('window.markdownPreviewRender(window.markdownPreviewPendingText);', init_py)
        self.assertNotIn("document.addEventListener('keyup'", preview)
        self.assertNotIn('setInterval(updatePreview', preview)

    def test_non_markdown_note_type_removes_preview_area(self):
        init_py = (ROOT / '__init__.py').read_text(encoding='utf-8')
        self.assertIn("document.getElementById('markdown-area')", init_py)
        self.assertIn('window.markdownPreviewRender = null;', init_py)

    def test_generated_templates_keep_expected_fields(self):
        self.assertIn('{{Front}}', HTMLandCSS.front)
        self.assertIn('{{Front}}', HTMLandCSS.back)
        self.assertIn('{{Back}}', HTMLandCSS.back)
        self.assertIn('{{Back Extra}}', HTMLandCSS.back_cloze)

    def test_update_does_not_delete_media_directories(self):
        init_py = (ROOT / '__init__.py').read_text(encoding='utf-8')
        self.assertNotIn('shutil.rmtree', init_py)
        self.assertNotIn('os.rmdir', init_py)

    def test_bundled_dependency_files_exist(self):
        for filename in ('_katex.min.js', '_markdown-it.min.js', '_highlight.js', '_markdown-it-mark.js', '_mhchem.js'):
            self.assertGreater((ROOT / filename).stat().st_size, 0, filename)


if __name__ == '__main__':
    unittest.main()
