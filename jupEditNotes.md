
# Notes about Markdown Cells in Jupyter

Here's a collection of random notes about working with Markdown and HTML in Jupyter notebooks:

* [Using HTML and Markdown Together](#htmlmark)
* [Link to Anchor in Same Notebook](#intralink)
* [Link to Anchor in Another Notebook](#interlink)


## <a id='htmlmark'>Using HTML and Markdown Together</a>


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

## <a id='intralink'>Link to Anchor in Same Notebook</a>

To create a internal clickable link in the same notebook:

1. Create link
    [To some Internal Section](#section_id)

2. Create destination
    <a id='section_id'></a>

## <a id='interlink'>Link to Anchor in Another Notebook</a>

To create link in one notebook and destination in another notebook.

1. Create link
    [To Some Internal Section](another_notebook.ipynb#section_id2)

2. Create Destination
    <a id='section_id2'></a>

    If the notebook is inside a folder present in the current working directory:
        [To Some Internal Section](TestFolder/another_notebook.ipynb#section_id3)
