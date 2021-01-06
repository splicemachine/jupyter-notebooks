
# Notes about Markdown Cells in Jupyter

Here's a collection of random notes about working with Markdown and HTML in Jupyter notebooks:

* Using HTML and Markdown Together
* About Headings


## Using HTML and Markdown Together


You can freely use HTML tags within a markdown cell. However, you CANNOT use markdown within an HTML tag.

For example, these are fine:

    ### Markdown Heading
    <p class="noteIcon">This is an HTML paragraph that includes <em>italicized</em> text,  a <span class="underlined">span that's styled with a class</span>, and <span style="color:green;">a colored span</span>.</p>

    A markdown paragraph with *markdown italics* and <em>html italics</em>.

But these are not:

    <p>Here an HTML paragraph that tries to use *markdown italics* but that text won't actually be italicized in the cell because the HTML parser doesn't know about markdown</p>

    <div>
    The & symbol has to be denoted as &amp; or using its Unicode value because we're within an HTML div section here. It will not display correctly in a cell.
    </div>

Markdown is converted into HTML, so you can use html tags within markdown; however, you cannot use markdown within HTML sections


## About Headings

Heading tags (#, ##, ###, ####, ####) should only be used for headings, not for emphasis. This is standard practice for HTML page design, and will become vital if/when Splice Machine has to be accessible, which means that a low-vision or blind person can use these pages via a screen reader. Screen readers depend on headings being used only as headings and on headings having appropriate and sequential nesting.

Use italics for emphasis, and use bold for strong emphasis.
