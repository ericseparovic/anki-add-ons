""" This file contains all the HTML / CSS strings for the different card types """

HTMLforEditor = """
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

        var fields = document.getElementById('fields');
        if (fields !== null) {
			keyupFunc = function() {
				var text = '# Field 1\\n' + fields.children[0].children[1].shadowRoot.children[2].innerHTML;
				text += "\\n# Field 2\\n" + fields.children[1].children[1].shadowRoot.children[2].innerHTML;
				render(text);
			}

			document.body.appendChild(area);
		}
        
        else {
			var fields = document.getElementsByClassName('fields')[0];
        
			keyupFunc = function() {
				var text = '# Field 1\\n' + fields.children[0].getElementsByClassName("rich-text-editable")[0].shadowRoot.children[2].innerHTML;
				text += "\\n# Field 2\\n" + fields.children[1].getElementsByClassName("rich-text-editable")[0].shadowRoot.children[2].innerHTML;
				render(text);
			}

			fields.appendChild(area);
		}


        var getResources = [
					getCSS("_katex.css", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"),
					getCSS("_highlight.css", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/default.min.css"),
					getScript("_highlight.js", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/highlight.min.js"),
					getScript("_katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js"),
					getScript("_auto-render.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/auto-render-cdn.js"),
					getScript("_markdown-it.min.js", "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js"),
                                        getScript("_markdown-it-mark.js","https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/_markdown-it-mark.js")
					
				];

				main = function() {
									keyupFunc();
									document.addEventListener('keyup', keyupFunc);
				}

                                Promise.all(getResources).then(() => getScript("_mhchem.js", "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/mhchem.min.js")).then(main);
				

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
					area.innerHTML = text.replace(/&lt;\/span&gt;/gi,"\\\\");
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
					str = str.replace(/<[\/]?pre[^>]*>/gi, "");
					str = str.replace(/<br\s*[\/]?[^>]*>/gi, "\\n");
					str = str.replace(/<div[^>]*>/gi, "\\n");
					// Thanks Graham A!
					str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\/span>/gi, "$1")
					str.replace(/<\/div[^>]*>/g, "\\n");
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
				css.onerror = reject;
				css_online.href = altURL;
				document.head.appendChild(css_online);
			}
			css.href = path;
			document.head.appendChild(css);
		});
	}


	function render() {
		markdown("front");
		renderMath("front");
		show();
	}

	function show() {
		document.getElementById("front").style.visibility = "visible";
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
		document.getElementById(ID).innerHTML = text.replace(/&lt;\/span&gt;/gi,"\\\\");
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
		str = str.replace(/<[\/]?pre[^>]*>/gi, "");
		str = str.replace(/<br\s*[\/]?[^>]*>/gi, "\\n");
		str = str.replace(/<div[^>]*>/gi, "\\n");
		// Thanks Graham A!
		str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\/span>/gi, "$1")
		str.replace(/<\/div[^>]*>/g, "\\n");
		return replaceHTMLElementsInString(str);
	}

	function replaceHTMLElementsInString(str) {
		str = str.replace(/&nbsp;/gi, " ");
		str = str.replace(/&tab;/gi, "	");
		str = str.replace(/&gt;/gi, ">");
		str = str.replace(/&lt;/gi, "<");
		return str.replace(/&amp;/gi, "&");
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
		document.getElementById(ID).innerHTML = text.replace(/&lt;\/span&gt;/gi,"\\\\");
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
		str = str.replace(/<[\/]?pre[^>]*>/gi, "");
		str = str.replace(/<br\s*[\/]?[^>]*>/gi, "\\n");
		str = str.replace(/<div[^>]*>/gi, "\\n");
		// Thanks Graham A!
		str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\/span>/gi, "$1")
		str.replace(/<\/div[^>]*>/g, "\\n");
		return replaceHTMLElementsInString(str);
	}

	function replaceHTMLElementsInString(str) {
		str = str.replace(/&nbsp;/gi, " ");
		str = str.replace(/&tab;/gi, "	");
		str = str.replace(/&gt;/gi, ">");
		str = str.replace(/&lt;/gi, "<");
		return str.replace(/&amp;/gi, "&");
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
	function render() {
		markdown("front");
		renderMath("front");
		show();
	}
	function show() {
		document.getElementById("front").style.visibility = "visible";
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
		document.getElementById(ID).innerHTML = text.replace(/&lt;\/span&gt;/gi,"\\\\");
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
		str = str.replace(/<[\/]?pre[^>]*>/gi, "");
		str = str.replace(/<br\s*[\/]?[^>]*>/gi, "\\n");
		str = str.replace(/<div[^>]*>/gi, "\\n");
		// Thanks Graham A!
		str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\/span>/gi, "$1")
		str.replace(/<\/div[^>]*>/g, "\\n");
		return replaceHTMLElementsInString(str);
	}

	function replaceHTMLElementsInString(str) {
		str = str.replace(/&nbsp;/gi, " ");
		str = str.replace(/&tab;/gi, "	");
		str = str.replace(/&gt;/gi, ">");
		str = str.replace(/&lt;/gi, "<");
		return str.replace(/&amp;/gi, "&");
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
		document.getElementById(ID).innerHTML = text.replace(/&lt;\/span&gt;/gi,"\\\\");
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
		str = str.replace(/<[\/]?pre[^>]*>/gi, "");
		str = str.replace(/<br\s*[\/]?[^>]*>/gi, "\\n");
		str = str.replace(/<div[^>]*>/gi, "\\n");
		// Thanks Graham A!
		str = str.replace(/<span(?![^>]*class=["'][^"']*\\bcloze\\b[^"']*["'])[^>]*>(.*?)<\/span>/gi, "$1")
		str.replace(/<\/div[^>]*>/g, "\\n");
		return replaceHTMLElementsInString(str);
	}

	function replaceHTMLElementsInString(str) {
		str = str.replace(/&nbsp;/gi, " ");
		str = str.replace(/&tab;/gi, "	");
		str = str.replace(/&gt;/gi, ">");
		str = str.replace(/&lt;/gi, "<");
		return str.replace(/&amp;/gi, "&");
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
  display: block;
  padding: 20px;
  overflow: auto;
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
