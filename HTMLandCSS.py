""" This file contains HTML strings for the different card types. """

from pathlib import Path


ADDON_DIR = Path(__file__).resolve().parent

HTMLforEditor = """
        if (window.markdownPreviewKeyupFunc) {
            document.removeEventListener('keyup', window.markdownPreviewKeyupFunc);
            window.markdownPreviewKeyupFunc = null;
        }

        var area = document.getElementById('markdown-area');
        if(area) area.remove();
        area = document.createElement('markdown-area');
        area.id = 'markdown-area';
        area.style.display = 'inline-block';
        area.style.overflowY = 'auto';
        area.style.padding = '1%';
        area.style.visibility = 'hidden';
        area.style.width = '98%';
        area.style.height = '100%';

        var markdownPreviewFieldNames = __FIELD_NAMES__;

        var fields = document.getElementById('fields');
        var previewParent = document.body;

        if (fields === null) {
			fields = document.getElementsByClassName('fields')[0];
			previewParent = fields;
		}

		var keyupFunc = function() {
			var text = collectFieldText();
			if (text) {
				render(text);
			}
		}

		if (fields && previewParent) {
			previewParent.appendChild(area);
		}


        var getResources = [
					getKatexCSS("__ADDON_WEB_PATH__/_katex.css"),
					getCSS("__ADDON_WEB_PATH__/_highlight.css"),
					getScript("__ADDON_WEB_PATH__/_highlight.js"),
					getScript("__ADDON_WEB_PATH__/_katex.min.js"),
					getScript("__ADDON_WEB_PATH__/_auto-render.js"),
					getScript("__ADDON_WEB_PATH__/_markdown-it.min.js"),
                                        getScript("__ADDON_WEB_PATH__/_markdown-it-mark.js")
					
				];

				var main = function() {
									keyupFunc();
									window.markdownPreviewKeyupFunc = keyupFunc;
									document.addEventListener('keyup', window.markdownPreviewKeyupFunc);
				}


                                Promise.all(getResources).then(() => getScript("__ADDON_WEB_PATH__/_mhchem.js")).then(main).catch(showFallbackPreview);
				

				function getScript(path) {
					return new Promise((resolve, reject) => {
						let script = document.createElement("script");
						script.onload = resolve;
						script.onerror = reject;
						script.src = path;
						document.head.appendChild(script);
					})
				}

				function getCSS(path) {
					return new Promise((resolve, reject) => {
						var css = document.createElement('link');
						css.setAttribute('rel', 'stylesheet');
						css.type = 'text/css';
						css.onload = resolve;
						css.onerror = reject;
						css.href = path;
						document.head.appendChild(css);
					});
				}

				function getKatexCSS(path) {
					return fetch(path).then(function(response) {
						if (!response.ok) {
							throw new Error('Failed to load KaTeX CSS');
						}
						return response.text();
					}).then(function(cssText) {
						var style = document.createElement('style');
						style.type = 'text/css';
						style.textContent = cssText.replace(/url\\(_/g, 'url(__ADDON_WEB_PATH__/fonts/_');
						document.head.appendChild(style);
					});
				}

				function showFallbackPreview() {
					area.textContent = replaceInString(collectFieldText());
					show();
				}

				function collectFieldText() {
					if (!fields || !fields.children) {
						return '';
					}

					var parts = [];
					for (var i = 0; i < fields.children.length; i++) {
						var html = getFieldHTML(fields.children[i]);
						if (html) {
							var fieldName = markdownPreviewFieldNames[i] || ('Field ' + (i + 1));
							parts.push('# ' + fieldName + '\\n' + html);
						}
					}
					return parts.join('\\n');
				}

				function getFieldHTML(field) {
					if (!field) {
						return '';
					}

					var editables = field.getElementsByClassName('rich-text-editable');
					for (var i = 0; i < editables.length; i++) {
						var html = getShadowHTML(editables[i]);
						if (html) {
							return html;
						}
					}

					if (field.children && field.children.length > 1) {
						var html = getShadowHTML(field.children[1]);
						if (html) {
							return html;
						}
					}

					return getShadowHTML(field);
				}

				function getShadowHTML(element) {
					if (!element || !element.shadowRoot) {
						return '';
					}

					var editable = element.shadowRoot.querySelector('[contenteditable="true"]');
					if (editable) {
						return editable.innerHTML;
					}

					var children = element.shadowRoot.children;
					if (children.length > 2 && children[2].innerHTML !== undefined) {
						return children[2].innerHTML;
					}

					for (var i = 0; i < children.length; i++) {
						if (children[i].innerHTML !== undefined) {
							return children[i].innerHTML;
						}
					}

					return '';
				}

				function render(text) {
					area.textContent = replaceInString(text);
					markdown(text);
					renderMath(text);
					show();
				}

				function show() {
					area.style.visibility = "visible";
				}


				function renderMath(text) {
					renderMathInElement(area, {
						delimiters:  [
								{left: "$$", right: "$$", display: true},
								{left: "\\\\(", right: "\\\\)", display: false},
								{left: "\\\\[", right: "\\\\]", display: true}
						],
						ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
																	throwOnError : false
					});
				}
				function markdown() {
					let md = new markdownit({typographer: true, html:true, highlight: function (str, lang) {
																	if (lang && hljs.getLanguage(lang)) {
																			try {
																					return hljs.highlight(str, { language: lang }).value;
																			} catch (__) {}
																	}

																	return ''; // use external default escaping
															}}).use(markdownItMark);
					text = replaceHTMLElementsInString(area.innerHTML);
					text = protectMathDelimiters(text);
					text = md.render(text);
					text = restoreMathDelimiters(text);
					area.innerHTML = text.replace(/&lt;\\/span&gt;/gi,"\\\\");
				}
				function protectMathDelimiters(str) {
					return str.split("\\\\(").join("ANKI_KATEX_INLINE_OPEN")
						.split("\\\\)").join("ANKI_KATEX_INLINE_CLOSE")
						.split("\\\\[").join("ANKI_KATEX_DISPLAY_OPEN")
						.split("\\\\]").join("ANKI_KATEX_DISPLAY_CLOSE");
				}
				function restoreMathDelimiters(str) {
					return str.split("ANKI_KATEX_INLINE_OPEN").join("\\\\(")
						.split("ANKI_KATEX_INLINE_CLOSE").join("\\\\)")
						.split("ANKI_KATEX_DISPLAY_OPEN").join("\\\\[")
						.split("ANKI_KATEX_DISPLAY_CLOSE").join("\\\\]");
				}
				function replaceInString(str) {
					str = str.replace(/<[/]?pre[^>]*>/gi, "");
					str = str.replace(/<br\\s*[/]?[^>]*>/gi, "\\n");
					str = str.replace(/<div[^>]*>/gi, "\\n");
					// Thanks Graham A!
					str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\\/span>/gi, "$1")
					str = str.replace(/<\\/div[^>]*>/g, "\\n");
					return replaceHTMLElementsInString(str);
				}

				function replaceHTMLElementsInString(str) {
					str = str.replace(/&nbsp;/gi, " ");
					str = str.replace(/&tab;/gi, "	");
					str = str.replace(/&gt;/gi, ">");
					str = str.replace(/&lt;/gi, "<");
					return str.replace(/&amp;/gi, "&");
				}
        """

CARD_RENDER_HELPERS = """
	function getScript(path) {
		return new Promise((resolve, reject) => {
			let script = document.createElement("script");
			script.onload = resolve;
			script.onerror = reject;
			script.src = path;
			document.head.appendChild(script);
		})
	}

	function getCSS(path) {
		return new Promise((resolve, reject) => {
			var css = document.createElement('link');
			css.setAttribute('rel', 'stylesheet');
			css.type = 'text/css';
			css.onload = resolve;
			css.onerror = reject;
			css.href = path;
			document.head.appendChild(css);
		});
	}

	function renderMath(ID) {
		renderMathInElement(document.getElementById(ID), {
			delimiters:  [
  				{left: "$$", right: "$$", display: true},
				{left: "\\\\(", right: "\\\\)", display: false},
				{left: "\\\\[", right: "\\\\]", display: true}
			],
            ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
            throwOnError : false
		});
	}

	function markdown(ID) {
		let md = new markdownit({typographer: true, html:true, highlight: function (str, lang) {
                            if (lang && hljs.getLanguage(lang)) {
                                try {
                                    return hljs.highlight(str, { language: lang }).value;
                                } catch (__) {}
                            }

                            return ''; // use external default escaping
                        }}).use(markdownItMark);
		let text = replaceInString(document.getElementById(ID).innerHTML);
		text = protectMathDelimiters(text);
		text = md.render(text);
		text = restoreMathDelimiters(text);
		document.getElementById(ID).innerHTML = text.replace(/&lt;\\/span&gt;/gi,"\\\\");
	}

	function protectMathDelimiters(str) {
		return str.split("\\\\(").join("ANKI_KATEX_INLINE_OPEN")
			.split("\\\\)").join("ANKI_KATEX_INLINE_CLOSE")
			.split("\\\\[").join("ANKI_KATEX_DISPLAY_OPEN")
			.split("\\\\]").join("ANKI_KATEX_DISPLAY_CLOSE");
	}

	function restoreMathDelimiters(str) {
		return str.split("ANKI_KATEX_INLINE_OPEN").join("\\\\(")
			.split("ANKI_KATEX_INLINE_CLOSE").join("\\\\)")
			.split("ANKI_KATEX_DISPLAY_OPEN").join("\\\\[")
			.split("ANKI_KATEX_DISPLAY_CLOSE").join("\\\\]");
	}

	function replaceInString(str) {
		str = str.replace(/<[/]?pre[^>]*>/gi, "");
		str = str.replace(/<br\\s*[/]?[^>]*>/gi, "\\n");
		str = str.replace(/<div[^>]*>/gi, "\\n");
		// Thanks Graham A!
		str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\\/span>/gi, "$1")
		str = str.replace(/<\\/div[^>]*>/g, "\\n");
		return replaceHTMLElementsInString(str);
	}

	function replaceHTMLElementsInString(str) {
		str = str.replace(/&nbsp;/gi, " ");
		str = str.replace(/&tab;/gi, "	");
		str = str.replace(/&gt;/gi, ">");
		str = str.replace(/&lt;/gi, "<");
		return str.replace(/&amp;/gi, "&");
	}
"""

CARD_RESOURCE_LOADER = """
	var getResources = [
		getCSS("_katex.css"),
		getCSS("_highlight.css"),
		getScript("_highlight.js"),
		getScript("_katex.min.js"),
		getScript("_auto-render.js"),
		getScript("_markdown-it.min.js"),
		getScript("_markdown-it-mark.js")
	];
	Promise.all(getResources).then(() => getScript("_mhchem.js")).then(render).catch(show);
"""


def _render_calls(element_ids):
    return "\n".join(
        f'\t\tmarkdown("{element_id}");\n\t\trenderMath("{element_id}");'
        for element_id in element_ids
    )


def _show_calls(element_ids):
    return "\n".join(
        f'\t\tdocument.getElementById("{element_id}").style.visibility = "visible";'
        for element_id in element_ids
    )


def _card_template(body, render_element_ids, show_element_ids=None):
    if show_element_ids is None:
        show_element_ids = render_element_ids
    return f"""

{body}

<script>
{CARD_RESOURCE_LOADER}
{CARD_RENDER_HELPERS}

	function render() {{
{_render_calls(render_element_ids)}
		show();
	}}

	function show() {{
{_show_calls(show_element_ids)}
	}}
</script>
"""


front = _card_template(
    '<div id="front"><pre>{{Front}}</pre></div>',
    ["front"],
)

back = _card_template(
    '<div id="front"><pre>{{Front}}</pre></div>\n\n<hr id=answer>\n\n<div id="back"><pre>{{Back}}</pre></div>',
    ["front", "back"],
)

front_cloze = _card_template(
    '<div id="front"><pre>{{cloze:Text}}</pre></div>',
    ["front"],
)

back_cloze = _card_template(
    '<div id="back"><pre>{{cloze:Text}}</pre></div><br>\n<div id="extra"><pre>{{Back Extra}}</pre></div>',
    ["back", "extra"],
)

css = (ADDON_DIR / "_card.css").read_text(encoding="utf-8")
