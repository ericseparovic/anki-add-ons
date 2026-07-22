import json
import os
import shutil

from .HTMLandCSS import HTMLforEditor, front, back, front_cloze, back_cloze, css
from aqt import gui_hooks, mw
import anki

MODEL_NAME = 'KaTeX and Markdown'
ADDON_PACKAGE = mw.addonManager.addonFromModule(__name__)
ADDON_WEB_PATH = f"/_addons/{ADDON_PACKAGE}"

mw.addonManager.setWebExports(__name__, r".*\.(css|js|ttf|woff|woff2)")


def markdownPreview(editor):
    """ This function runs when the user opens the editor, creates the markdown preview area """
    note_type = editor.note.note_type()
    if note_type and note_type["name"] in [MODEL_NAME + " Basic", MODEL_NAME + " Cloze"]:
        field_names = [field["name"] for field in note_type["flds"]]
        editor_js = HTMLforEditor.replace("__ADDON_WEB_PATH__", ADDON_WEB_PATH)
        editor_js = editor_js.replace("__FIELD_NAMES__", json.dumps(field_names))
        editor.web.eval(editor_js)
        editor.web.eval("""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerText = `
                #markdown-area {
                    --ctp-base: #eff1f5;
                    --ctp-mantle: #e6e9ef;
                    --ctp-surface0: #ccd0da;
                    --ctp-surface1: #bcc0cc;
                    --ctp-text: #4c4f69;
                    --ctp-subtext1: #5c5f77;
                    --ctp-blue: #1e66f5;
                    --ctp-mauve: #8839ef;
                    --ctp-pink: #ea76cb;
                    --ctp-red: #d20f39;
                    --ctp-yellow: #df8e1d;
                    --ctp-peach: #fe640b;
                    --ctp-green: #40a02b;
                    --ctp-teal: #179299;
                    --ctp-maroon: #e64553;
                    --ctp-overlay0: #9ca0b0;
                    color: var(--ctp-text);
                    background-color: var(--ctp-base);
                    border-radius: 8px;
                }
                .nightMode #markdown-area,
                #markdown-area.nightMode {
                    --ctp-base: #1e1e2e;
                    --ctp-mantle: #181825;
                    --ctp-surface0: #313244;
                    --ctp-surface1: #45475a;
                    --ctp-text: #cdd6f4;
                    --ctp-subtext1: #bac2de;
                    --ctp-blue: #89b4fa;
                    --ctp-mauve: #cba6f7;
                    --ctp-pink: #f5c2e7;
                    --ctp-red: #f38ba8;
                    --ctp-yellow: #f9e2af;
                    --ctp-peach: #fab387;
                    --ctp-green: #a6e3a1;
                    --ctp-teal: #94e2d5;
                    --ctp-maroon: #eba0ac;
                    --ctp-overlay0: #6c7086;
                }
                table, th, td {
                    border: 1px solid var(--ctp-surface1);
                    border-collapse: collapse;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: var(--ctp-text);
                    line-height: 1.25;
                    margin: 1em 0 0.5em;
                }
                h1 {
                    color: var(--ctp-mauve);
                    font-size: 1.55em;
                    border-bottom: 2px solid var(--ctp-mauve);
                    padding-bottom: 0.2em;
                }
                h2 {
                    color: var(--ctp-blue);
                    font-size: 1.35em;
                    border-left: 5px solid var(--ctp-blue);
                    padding-left: 0.5em;
                }
                h3 {
                    color: var(--ctp-green);
                    font-size: 1.2em;
                    border-left: 4px solid var(--ctp-green);
                    padding-left: 0.45em;
                }
                h4 {
                    color: var(--ctp-peach);
                    font-size: 1.08em;
                    border-left: 4px solid var(--ctp-peach);
                    padding-left: 0.45em;
                }
                h5 {
                    color: var(--ctp-pink);
                    font-size: 0.98em;
                    border-left: 3px solid var(--ctp-pink);
                    padding-left: 0.4em;
                }
                h6 {
                    color: var(--ctp-subtext1);
                    font-size: 0.9em;
                    border-left: 3px solid var(--ctp-subtext1);
                    padding-left: 0.4em;
                }
                code {
                    background-color: var(--ctp-mantle);
                    color: var(--ctp-text);
                    border-radius: 4px;
                    padding: 0.1em 0.3em;
                }
                pre code {
                    background-color: var(--ctp-mantle);
                    border: 1px solid var(--ctp-surface0);
                    border-radius: 8px;
                    display: block;
                    padding: 20px;
                    overflow: auto;
                }
                pre code.hljs,
                code.hljs,
                .hljs {
                    background-color: var(--ctp-mantle);
                    color: var(--ctp-text);
                }
                .hljs-comment,
                .hljs-quote {
                    color: var(--ctp-overlay0);
                    font-style: italic;
                }
                .hljs-doctag,
                .hljs-keyword,
                .hljs-meta .hljs-keyword,
                .hljs-template-tag,
                .hljs-template-variable,
                .hljs-type,
                .hljs-variable.language_ {
                    color: var(--ctp-mauve);
                }
                .hljs-title,
                .hljs-title.class_,
                .hljs-title.class_.inherited__,
                .hljs-title.function_ {
                    color: var(--ctp-blue);
                }
                .hljs-attr,
                .hljs-attribute,
                .hljs-literal,
                .hljs-meta,
                .hljs-number,
                .hljs-operator,
                .hljs-selector-attr,
                .hljs-selector-class,
                .hljs-selector-id,
                .hljs-variable {
                    color: var(--ctp-peach);
                }
                .hljs-regexp,
                .hljs-string,
                .hljs-meta .hljs-string {
                    color: var(--ctp-green);
                }
                .hljs-built_in,
                .hljs-symbol {
                    color: var(--ctp-maroon);
                }
                .hljs-code,
                .hljs-formula,
                .hljs-section {
                    color: var(--ctp-teal);
                }
                .hljs-name,
                .hljs-selector-pseudo,
                .hljs-selector-tag {
                    color: var(--ctp-red);
                }
                .hljs-subst {
                    color: var(--ctp-text);
                }
                .hljs-deletion {
                    color: var(--ctp-red);
                }
                .hljs-addition {
                    color: var(--ctp-green);
                }
                .hljs-emphasis {
                    font-style: italic;
                }
                .hljs-strong {
                    font-weight: 700;
                }
                blockquote {
                    color: var(--ctp-subtext1);
                    border-left: 4px solid var(--ctp-surface0);
                    padding-left: 12px;
                }
                mark {
                    background-color: var(--ctp-yellow);
                    color: var(--ctp-base);
                }
                a {
                    color: var(--ctp-blue);
                }
                .cloze {
                    color: var(--ctp-red);
                    font-weight: bold;
                }`;
            document.head.appendChild(style);
        """)
    else: # removes the markdown preview
        editor.web.eval("""
					var area = document.getElementById('markdown-area');
					if(area) area.remove();
        """)


gui_hooks.editor_did_load_note.append(markdownPreview)


def create_model_if_necessary():
    """ 
    Runs when the user opens Anki, creates the two card types and also handles updating
    the card types CSS and HTML if the addon has a pending update
    """
    model = mw.col.models.by_name(MODEL_NAME + " Basic")
    model_cloze = mw.col.models.by_name(MODEL_NAME + " Cloze")

    if not model:
        create_model()
    if not model_cloze:
        create_model_cloze()

    update()


def create_model():
    """ Creates the Basic Card type """
    m = mw.col.models
    model = m.new(MODEL_NAME + " Basic")

    field = m.newField("Front")
    m.addField(model, field)

    field = m.newField("Back")
    m.addField(model, field)

    template = m.newTemplate(MODEL_NAME + " Basic")
    template['qfmt'] = front
    template['afmt'] = back
    model['css'] = css

    m.addTemplate(model, template)
    m.add(model)
    m.save(model)


def create_model_cloze():
    """ Creates the Cloze Card type """
    m = mw.col.models
    model = m.new(MODEL_NAME + " Cloze")
    model["type"] = anki.consts.MODEL_CLOZE

    field = m.newField("Text")
    m.addField(model, field)

    field = m.newField("Back Extra")
    m.addField(model, field)

    template = m.newTemplate(MODEL_NAME + " Cloze")
    template['qfmt'] = front_cloze
    template['afmt'] = back_cloze
    model['css'] = css

    m.addTemplate(model, template)
    m.add(model)
    m.save(model)


def update():
    """ Updates the card types the addon has a pending update """
    model = mw.col.models.by_name(MODEL_NAME + " Basic")
    model_cloze = mw.col.models.by_name(MODEL_NAME + " Cloze")

    if model:
        model['tmpls'][0]['qfmt'] = front
        model['tmpls'][0]['afmt'] = back
        model['css'] = css
        mw.col.models.save(model)

    if model_cloze:
        model_cloze['tmpls'][0]['qfmt'] = front_cloze
        model_cloze['tmpls'][0]['afmt'] = back_cloze
        model_cloze['css'] = css
        mw.col.models.save(model_cloze)

    if os.path.isdir(os.path.join(mw.col.media.dir(), "_katex")):
        shutil.rmtree(os.path.join(mw.col.media.dir(), "_katex"))

    if os.path.isdir(os.path.join(mw.col.media.dir(), "_markdown-it")):
        shutil.rmtree(os.path.join(mw.col.media.dir(), "_markdown-it"))

    addon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    _add_file(os.path.join(addon_path, "_katex.min.js"), "_katex.min.js")
    _add_file(os.path.join(addon_path, "_katex.css"), "_katex.css")
    _add_file(os.path.join(addon_path, "_auto-render.js"), "_auto-render.js")
    _add_file(os.path.join(addon_path, "_markdown-it.min.js"),
              "_markdown-it.min.js")
    _add_file(os.path.join(addon_path, "_highlight.css"), "_highlight.css")
    _add_file(os.path.join(addon_path, "_highlight.js"), "_highlight.js")
    _add_file(os.path.join(addon_path, "_mhchem.js"), "_mhchem.js")
    _add_file(os.path.join(addon_path, "_markdown-it-mark.js"),
              "_markdown-it-mark.js")

    for katex_font in os.listdir(os.path.join(addon_path, "fonts")):
        _add_file(os.path.join(addon_path, "fonts", katex_font), katex_font)


def _add_file(path, filename):
    if not os.path.isfile(os.path.join(mw.col.media.dir(), filename)):
        mw.col.media.add_file(path)


gui_hooks.profile_did_open.append(create_model_if_necessary)
