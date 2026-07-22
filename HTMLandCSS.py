""" This file contains all the HTML / CSS strings for the different card types """

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
	function getScript(path, altURL) {
		return new Promise((resolve, reject) => {
			let script = document.createElement("script");
			script.onload = resolve;
			script.onerror = function() {
				let script_online = document.createElement("script");
				script_online.onload = resolve;
				script_online.onerror = reject;
				script_online.src = altURL;
				document.head.appendChild(script_online);
			}
			script.src = path;
			document.head.appendChild(script);
		})
	}

	function getCSS(path, altURL) {
		return new Promise((resolve, reject) => {
			var css = document.createElement('link');
			css.setAttribute('rel', 'stylesheet');
			css.type = 'text/css';
			css.onload = resolve;
			css.onerror = function() {
				var css_online = document.createElement('link');
				css_online.setAttribute('rel', 'stylesheet');
				css_online.type = 'text/css';
				css_online.onload = resolve;
				css_online.onerror = reject;
				css_online.href = altURL;
				document.head.appendChild(css_online);
			}
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

front = """

<div id="front"><pre>{{Front}}</pre></div>

<script>
	var getResources = [
		getCSS("_katex.css", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"),
		getCSS("_highlight.css", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/default.min.css"),
		getScript("_highlight.js", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/highlight.min.js"),
		getScript("_katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js"),
		getScript("_auto-render.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/auto-render-cdn.js"),
		getScript("_markdown-it.min.js", "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js"),
                getScript("_markdown-it-mark.js","https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/_markdown-it-mark.js")
	];
        Promise.all(getResources).then(() => getScript("_mhchem.js", "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/mhchem.min.js")).then(render).catch(show);

""" + CARD_RENDER_HELPERS + """


	function render() {
		markdown("front");
		renderMath("front");
		show();
	}

	function show() {
		document.getElementById("front").style.visibility = "visible";
	}

</script>
"""

back = """

<div id="front"><pre>{{Front}}</pre></div>

<hr id=answer>

<div id="back"><pre>{{Back}}</pre></div>

<script>
	var getResources = [
		getCSS("_katex.css", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"),
		getCSS("_highlight.css", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/default.min.css"),
		getScript("_highlight.js", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/highlight.min.js"),
		getScript("_katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js"),
		getScript("_auto-render.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/auto-render-cdn.js"),
		getScript("_markdown-it.min.js", "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js"),
		getScript("_markdown-it-mark.js","https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/_markdown-it-mark.js")
	];
        Promise.all(getResources).then(() => getScript("_mhchem.js", "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/mhchem.min.js")).then(render).catch(show);
	
""" + CARD_RENDER_HELPERS + """

	function render() {
		markdown("front");
		renderMath("front");
		markdown("back");
		renderMath("back");
		show();
	}

	function show() {
		document.getElementById("front").style.visibility = "visible";
		document.getElementById("back").style.visibility = "visible";
	}
</script>
"""

front_cloze = """

<div id="front"><pre>{{cloze:Text}}</pre></div>

<script>
	var getResources = [
		getCSS("_katex.css", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"),
		getCSS("_highlight.css", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/default.min.css"),
		getScript("_highlight.js", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/highlight.min.js"),
		getScript("_katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js"),
		getScript("_auto-render.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/auto-render-cdn.js"),
		getScript("_markdown-it.min.js", "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js"),
		getScript("_markdown-it-mark.js","https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/_markdown-it-mark.js")
	];
        Promise.all(getResources).then(() => getScript("_mhchem.js", "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/mhchem.min.js")).then(render).catch(show);
	
""" + CARD_RENDER_HELPERS + """

	function render() {
		markdown("front");
		renderMath("front");
		show();
	}
	function show() {
		document.getElementById("front").style.visibility = "visible";
	}
</script>
"""

back_cloze = """

<div id="back"><pre>{{cloze:Text}}</pre></div><br>
<div id="extra"><pre>{{Back Extra}}</pre></div>

<script>
	var getResources = [
		getCSS("_katex.css", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"),
		getCSS("_highlight.css", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/default.min.css"),
		getScript("_highlight.js", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/highlight.min.js"),
		getScript("_katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js"),
		getScript("_auto-render.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/auto-render-cdn.js"),
		getScript("_markdown-it.min.js", "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js"),
		getScript("_markdown-it-mark.js","https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/_markdown-it-mark.js")
	];
        Promise.all(getResources).then(() => getScript("_mhchem.js", "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/mhchem.min.js")).then(render).catch(show);
	
""" + CARD_RENDER_HELPERS + """

	function render() {
		markdown("back");
		renderMath("back");
		markdown("extra");	
		renderMath("extra");
		show();
	}

	function show() {
		document.getElementById("back").style.visibility = "visible";
		document.getElementById("extra").style.visibility = "visible";
	}
</script>

"""
css = """

.card {
  --ctp-base: #eff1f5;
  --ctp-mantle: #e6e9ef;
  --ctp-surface0: #ccd0da;
  --ctp-surface1: #bcc0cc;
  --ctp-text: #4c4f69;
  --ctp-subtext1: #5c5f77;
  --ctp-blue: #1e66f5;
  --ctp-lavender: #7287fd;
  --ctp-mauve: #8839ef;
  --ctp-pink: #ea76cb;
  --ctp-red: #d20f39;
  --ctp-yellow: #df8e1d;
  --ctp-peach: #fe640b;
  --ctp-green: #40a02b;
  --ctp-teal: #179299;
  --ctp-maroon: #e64553;
  --ctp-overlay0: #9ca0b0;
  font-family: arial;
  font-size: 20px;
  color: var(--ctp-text);
  background-color: var(--ctp-base);
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
#front, #back, #extra {
	visibility: hidden;
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
a {
  color: var(--ctp-blue);
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
.cloze {
  color: var(--ctp-red);
  font-weight: bold;
}
.nightMode.card,
.nightMode .card {
  --ctp-base: #1e1e2e;
  --ctp-mantle: #181825;
  --ctp-surface0: #313244;
  --ctp-surface1: #45475a;
  --ctp-text: #cdd6f4;
  --ctp-subtext1: #bac2de;
  --ctp-blue: #89b4fa;
  --ctp-lavender: #b4befe;
  --ctp-mauve: #cba6f7;
  --ctp-pink: #f5c2e7;
  --ctp-red: #f38ba8;
  --ctp-yellow: #f9e2af;
  --ctp-peach: #fab387;
  --ctp-green: #a6e3a1;
  --ctp-teal: #94e2d5;
  --ctp-maroon: #eba0ac;
  --ctp-overlay0: #6c7086;
  color: var(--ctp-text);
  background-color: var(--ctp-base);
}
.nightMode table,
.nightMode th,
.nightMode td {
  border-color: var(--ctp-surface1);
}
.nightMode code {
  background-color: var(--ctp-mantle);
  color: var(--ctp-text);
}
.nightMode pre code,
.nightMode .hljs {
  background-color: var(--ctp-mantle);
  color: var(--ctp-text);
  border-color: var(--ctp-surface0);
}
.nightMode .cloze {
  color: var(--ctp-red);
  font-weight: bold;
}
.nightMode blockquote {
  color: var(--ctp-subtext1);
  border-left-color: var(--ctp-surface0);
}
.nightMode mark {
  background-color: var(--ctp-yellow);
  color: #11111b;
}
.nightMode a {
  color: var(--ctp-blue);
}
"""
