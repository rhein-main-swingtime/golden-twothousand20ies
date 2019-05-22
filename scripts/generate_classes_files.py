import os
import json
from pprint import pprint

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
MD_HEADER = (
"""---
title: '{title}'
taxonomy:
    category:
        - calendar
---\n\n""")



def main():
    with open(os.path.join(THIS_DIR, 'classes_calendars.json')) as file_obj:
        data = json.load(file_obj)
    
    for lang in ('de', 'en'):
        create_md(lang, data)

def create_md(lang, data):
    content = MD_HEADER.format(title=data['title'][lang])
    content += f'<iframe src="{data["embed_template"]}" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>'

    ids = [source['embed_id'] for source in data['sources'].values()]
    content = content.format(sources=data['sources_sep'].join(ids))

    data_dir = os.path.join(THIS_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    md_path = os.path.join(data_dir, f'frame.{lang}.md')
    with open(md_path, 'w', encoding='utf8') as file_obj:
        file_obj.write(content)


if __name__ == '__main__':
    main()