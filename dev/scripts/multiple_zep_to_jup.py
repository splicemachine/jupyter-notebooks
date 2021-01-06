for i in os.listdir('./zep_training_notebooks/notebook'):
    if ('2' in i):
        d = f'./zep_training_notebooks/notebook/{i}'
        file = os.listdir(f'{d}')[0]
        title = os.popen(f'cat {d}/{file} | grep name').read().split('\n')[0].replace('"name":','').strip()
        if('%md' not in title and '{' not in title):
            title = title.replace('",','.ipynb"')
            print(title)
            a,b,c = title.split('/')
            os.system(f'python convert.py {d}/note.json {a.strip()}"/"{b.strip()}"/"{c.strip()}')
