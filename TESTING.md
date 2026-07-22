# Manual Testing Checklist

Use this checklist after changing templates, rendering order, CSS, or bundled assets.

## Setup

1. Close Anki completely.
2. Start Anki from a terminal:

```bash
anki
```

3. Use the development add-on symlink:

```text
~/.local/share/Anki2/addons21/markdownkatexdev
```

4. Create or update notes using these note types:

```text
KaTeX and Markdown Basic
KaTeX and Markdown Cloze
```

## Compatibility Smoke Test

1. Start Anki from the terminal.
2. Open `Tools` -> `Add-ons`.
3. Confirm `Markdown and KaTeX Support` is enabled.
4. Open `Add` and select `KaTeX and Markdown Basic`.
5. Switch to `KaTeX and Markdown Cloze`.

Expected result:

- Anki starts without Python errors in the terminal.
- Both note types are available.
- Opening the editor does not show add-on errors.
- The add-on remains enabled on Anki 26.05 or newer compatible builds.
- The terminal does not show `byName is deprecated` or `model is deprecated` from this add-on.
- The terminal does not show Content Security Policy errors for `_highlight.js`, `_katex.min.js`, `_auto-render.js`, `_markdown-it.min.js`, `_markdown-it-mark.js`, or `_mhchem.js`.

## Basic Card Regression Test

Paste this into `Front` of a `KaTeX and Markdown Basic` note:

````markdown
# H1 Title

## H2 Section

### H3 Subsection

#### H4 Detail

##### H5 Small Detail

###### H6 Note

Text with **bold**, *italic*, ==marked text==, and `inline code`.

> Blockquote with Catppuccin styling.

| Language | Supported |
|---|---:|
| Java | yes |
| C | yes |
| C++ | yes |

Inline math: \(x + 1 = 2\)

Display math:

$$
E = mc^2
$$

Display math with brackets:

\[
\int_0^1 x^2 dx = \frac{1}{3}
\]

Literal dollar text: $500, $HOME, $PATH, $user, $(command), $("#app").

```bash
# Bash should keep dollar variables literal
echo $HOME
price="$500"
```

```java
public class Main {
    public static void main(String[] args) {
        String price = "$500";
        System.out.println(price);
    }
}
```

```c
#include <stdio.h>

int main(void) {
    printf("Hello C\n");
    return 0;
}
```

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values = {1, 2, 3};
    std::cout << "Hello C++" << std::endl;
    return 0;
}
```
````

Expected result:

- Headings `h1` through `h6` have distinct Catppuccin styling.
- Markdown renders normally.
- KaTeX renders `\(...\)`, `$$...$$`, and `\[...\]`.
- Literal `$` text stays literal.
- Code blocks use Catppuccin Highlight.js colors.
- Code blocks do not render KaTeX inside `pre` or `code`.
- No raw `<span class="katex">` or other generated HTML is visible.

## Cloze Regression Test

Paste this into `Text` of a `KaTeX and Markdown Cloze` note:

````markdown
# Cloze Test

The capital of France is {{c1::Paris}}.

The language with `std::vector` is {{c2::C++}}.

Markdown: **bold**, *italic*, and ==marked text==.

Inline math: \(a^2 + b^2 = c^2\)

Display math:

$$
E = mc^2
$$

```java
public class ClozeExample {
    private String answer = "$HOME is literal";
}
```
````

Paste this into `Back Extra`:

````markdown
Extra explanation with **Markdown**.

\[
a^2 + b^2 = c^2
\]
````

Expected result:

- Cloze deletion is hidden on the front.
- Cloze deletion is revealed on the back.
- `.cloze` styling is preserved.
- Markdown, KaTeX, and code highlighting still work.
- `$HOME` remains literal inside code.

## Preview Listener Test

1. Open a Basic note using the add-on note type.
2. Type in one of the fields and watch the Markdown preview update.
3. Switch to another note and back several times.
4. Type again.

Expected result:

- Preview updates once per keypress.
- The editor does not become progressively slower.
- No repeated rendering or flickering is visible.
- No JavaScript errors appear in the terminal.

## Editor Preview Field Test

1. Open a `KaTeX and Markdown Basic` note.
2. Type Markdown and math in `Front`.
3. Type different Markdown and math in `Back`.
4. Confirm the preview shows both fields with `Front` and `Back` headings.
5. Open a `KaTeX and Markdown Cloze` note.
6. Type content in `Text` and `Back Extra`.

Expected result:

- Preview renders content from all visible fields.
- Basic and Cloze editor previews both work.
- Missing or empty fields do not break the editor.
- No JavaScript CSP errors appear in the terminal.

## Theme Test

Run the Basic and Cloze tests in both light and dark Anki themes.

Expected result:

- Light mode uses Catppuccin Latte colors.
- Dark mode uses Catppuccin Mocha colors.
- Code, tables, blockquotes, marks, links, and cloze text remain readable.

## Developer Verification

Run before committing:

```bash
python -m py_compile HTMLandCSS.py __init__.py
git diff --check
```

Expected result:

- Python files compile without errors.
- `git diff --check` reports no whitespace errors.
