import os, sys
import re
import csv
import json
import html
import nbformat
import codecs
# from aws.s3 import S3
#from StringIO import StringIO

MD = re.compile(r'%md*')
# there's probably a smarter way to do this regex such that PYSPARK and SPARK don't have overlap but this will work for now
PYSPARK = re.compile(r'%spark.pyspark*')
SPARK = re.compile(r'%spark*')
SPLICE = re.compile(r'%splicemachine*')
# UNKNOWN_MAGIC = re.compile(r'%\w+\s')
HTML = re.compile(r'%html\s')

def read_io(path):
    """Reads the contents of a local or S3 path into a StringIO.
    """
    note = StringIO()
    if path.startswith("s3://"):
        s3 = S3(env='prod')
        for line in s3.read(path):
            note.write(line)
            note.write("\n")
    else:
        with open(path) as local:
            for line in local.readlines():
                note.write(line)

    note.seek(0)

    return note

def table_cell_to_html(cell):
    """Formats a cell from a Zeppelin TABLE as HTML.
    """
    if HTML.match(cell):
        # the contents is already HTML
        return cell
    else:
        return html.escape(cell)

def table_to_html(tsv):
    """Formats the tab-separated content of a Zeppelin TABLE as HTML.
    """
    io = StringIO.StringIO(tsv)
    reader = csv.reader(io, delimiter="\t")
    fields = reader.next()
    column_headers = "".join([ "<th>" + name + "</th>" for name in fields ])
    lines = [
            "<table>",
            "<tr>{column_headers}</tr>".format(column_headers=column_headers)
        ]
    for row in reader:
        lines.append("<tr>" + "".join([ "<td>" + table_cell_to_html(cell) + "</td>" for cell in row ]) + "</tr>")
    lines.append("</table>")
    return "\n".join(lines)

def convert_json(json_str):
    """Converts a Zeppelin note from JSON to a Jupyter NotebookNode.
    """
    return convert_parsed(json.loads(json_str))

def convert_parsed(zeppelin_note):
    """Converts a Zeppelin note from parsed JSON to a Jupyter NotebookNode.
    """
    notebook_name = zeppelin_note['name']

    # adding the default SPLICEMACHINE cells at the top
    cells = [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "os.environ['JDBC_HOST'] = 'jrtest01-splice-hregion'\n"
            ]
        }, 
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# setup-- \n",
                "import os\n",
                "import pyspark\n",
                "from splicemachine.spark.context import PySpliceContext\n",
                "from pyspark.conf import SparkConf\n",
                "from pyspark.sql import SparkSession\n",
                "\n",
                "# make sure pyspark tells workers to use python3 not 2 if both are installed\n",
                "os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'\n",
                "jdbc_host = os.environ['JDBC_HOST']\n",
                "\n",
                "conf = pyspark.SparkConf()\n",
                "sc = pyspark.SparkContext(conf=conf)\n", 
                "\n",
                "spark = SparkSession.builder.config(conf=conf).getOrCreate()\n",
                "'''jdbc:splice://{FRAMEWORKNAME}-proxy.marathon.mesos:1527/splicedb;user=splice;password=admin'''\n",
                "\n",
                "splicejdbc=f'jdbc:splice://{jdbc_host}:1527/splicedb;user=splice;password=admin'\n", 
                "\n",
                "splice = PySpliceContext(spark, splicejdbc)\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "%%sql\n",
                "%defaultDatasource jdbc:splice://jrtest01-splice-hregion:1527/splicedb;user=splice;password=admin"
            ]
        }
    ]
    index = 0
    for paragraph in zeppelin_note['paragraphs']:
        code = paragraph.get('text')
        if not code:
            continue

        code = code.lstrip()

        cell = {}

        if MD.match(code):
            cell['cell_type'] = 'markdown'
            cell['metadata'] = {}
            # code.replace('%md', ' %%markdown')
            cell['source'] = code.lstrip('%md').lstrip("\n") # remove '%md'
        elif PYSPARK.match(code):
            cell['cell_type'] = 'code'
            cell['execution_count'] = index
            cell['metadata'] = {}
            cell['outputs'] = []
            cell['source'] = code.lstrip('%spark.pyspark')

        elif SPARK.match(code):
            cell['cell_type'] = 'code'
            cell['execution_count'] = index
            cell['metadata'] = {}
            cell['outputs'] = []
            cell['source'] = '%%scala ' + code.lstrip('%spark')

        elif SPLICE.match(code):
            cell['cell_type'] = 'code'
            cell['execution_count'] = index
            cell['metadata'] = {}
            cell['outputs'] = []
            cell['source'] = '%%sql ' + code.lstrip('%splicemachine')

        else:
            cell['cell_type'] = 'code'
            cell['execution_count'] = index
            cell['metadata'] = {'autoscroll': 'auto'}
            cell['outputs'] = []
            cell['source'] = code

        cells.append(cell)
        '''
        -----------------------------------------------------------
        # I don't really care about rendering the results of a cell to be completely honest-- we can check if this works if we want but at first glance it doesn't look like it

        result = paragraph.get('results')
        if cell['cell_type'] == 'code' and result:
            if result['code'] == 'SUCCESS':
                result_type = result.get('type')
                output_by_mime_type = {}
                if result_type == 'TEXT':
                    output_by_mime_type['text/plain'] = result['msg']
                elif result_type == 'HTML':
                    output_by_mime_type['text/html'] = result['msg']
                elif result_type == 'TABLE':
                    output_by_mime_type['text/html'] = table_to_html(result['msg'])

                cell['outputs'] = [{
                    'output_type': 'execute_result',
                    'metadata': {},
                    'execution_count': index,
                    'data': output_by_mime_type
                }]
        '''

        index += 1

    notebook = nbformat.from_dict({
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.7.3"
            },
            "toc": {
                "base_numbering": 1,
                "nav_menu": {},
                "number_sections": False,
                "sideBar": False,
                "skip_h1_title": False,
                "title_cell": "Table of Contents",
                "title_sidebar": "Contents",
                "toc_cell": False,
                "toc_position": {},
                "toc_section_display": False,
                "toc_window_display": False
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2,
        "cells" : cells,
    })

    return (notebook_name, notebook)

def write_notebook(notebook_name, notebook, path=None):
    """Writes a NotebookNode to a file created from the notebook name.

    If path is None, the output path will be created the notebook name in the current directory.
    """
    filename = path
    if not filename:
        filename = notebook_name + '.ipynb'
        if os.path.exists(filename):
            for i in range(1, 1000):
                filename = notebook_name + ' (' + str(i) + ').ipynb'
                if not os.path.exists(filename):
                    break
                if i == 1000:
                    raise RuntimeError('Cannot write %s: versions 1-1000 already exist.' % (notebook_name,))

    with codecs.open(filename, 'w', encoding='UTF-8') as io:
        nbformat.write(notebook, io)

    return filename

if __name__ == '__main__':
    num_args = len(sys.argv)

    zeppelin_note_path = None
    target_path = None
    if num_args == 2:
        zeppelin_note_path = sys.argv[1]
    elif num_args == 3:
        zeppelin_note_path = sys.argv[1]
        target_path = sys.argv[2]

    if not zeppelin_note_path:
        print('Usage: jupyter-zeppelin </path/to/zeppelin_note.json> </target/path/notebook.ipynb>')
        exit()

    json_str= open(zeppelin_note_path).read().encode('UTF-8')

    name, content = convert_json(json_str)
    write_notebook(name, content, target_path)
