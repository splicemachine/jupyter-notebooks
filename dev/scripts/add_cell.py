import os
import json
for i in os.listdir():
    if '.' not in i: # It's a directory
        print(f'In {i}')
        for sub_folder in os.listdir(f'./{i}'):
            print(f'In {i}/{sub_folder}')
            for note in os.listdir(f'./{i}/{sub_folder}'):
                print(f'checking ./{i}/{sub_folder}/{note}')
                if 'ipynb' in note: #make sure not another sub folder
                    fi = open(f'./{i}/{sub_folder}/{note}')
                    data = json.load(fi)
                    # Replace this cell with the cell that you want to add to every notebook
                    cell = {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": [
                            "import os\n",
                            "os.environ['JDBC_HOST'] = 'jr1000-splice-hregion'"
                        ]
                    }
                    data['cells'].insert(0,cell)
                    with open(f'./{i}/{sub_folder}/{note}','w') as f:
                        json.dump(data, f, indent=4)
