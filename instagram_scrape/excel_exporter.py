import pandas as pd
from pandas import ExcelWriter
import os.path

def export(names, comments, label, url):
    print(url)
    name_file='instagram_scrape/komentar/'+url+'.xlsx'
    fname =name_file
    temp = {}
    temp_names = []
    temp_comments = []
    temp_label=[]
    if os.path.isfile(fname):
        saved = pd.read_excel(fname)
        temp_names.extend(saved['name'])
        temp_comments.extend(saved['comment'])
        temp_label.extend(saved['Label'])
    temp_names.extend(names)
    temp_comments.extend(comments)
    temp_label.extend(label)
    temp.update({'name': temp_names, 'comment': temp_comments,'Label':temp_label})
    df = pd.DataFrame(temp)
    writer = ExcelWriter(fname)
    df.to_excel(writer, 'Arif Kurniawan', index=False)
    writer.save()