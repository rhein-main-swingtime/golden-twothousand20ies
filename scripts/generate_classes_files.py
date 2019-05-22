import os
import json
from pprint import pprint

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
LANGS = ('de', 'en')
MD_HEADER = (
"""---
title: '{title}'
taxonomy:
    category:
        - calendar
---\n\n""")


def main():
    class_data = json_load(os.path.join(THIS_DIR, 'classes_calendars.json'))
    area_data = json_load(os.path.join(THIS_DIR, 'areas.json'))
    data_dir = os.path.join(THIS_DIR, '_ data')
    os.makedirs(data_dir, exist_ok=True)

    for lang in LANGS:
        print(f'processing lang {lang}...')
        create_md(data_dir, lang, class_data, area_data)
        

def create_md(data_dir, lang, data, area):
    content = MD_HEADER.format(title=data['title'][lang])
    content += f'<iframe src="{data["embed_template"]}" style="border-width:0" width="100%" height="800" frameborder="0" scrolling="no"></iframe>'

    # gather calendar ids and insert into iframe src string
    ids = [source['embed_id'] for source in data['sources'].values()]
    content = content.format(sources=data['sources_sep'].join(ids))

    # assemble are shorthands
    areas_in_use = set(source['area'] for source in data['sources'].values())
    area_assembly = set()
    for area_name, key in area['areas'].items():
        for area_in_use in areas_in_use:
            if area_name in area_in_use:
                area_assembly.add(f'**{key}** {area_name}')
    print(area_assembly)
    content += '\n\n{label}: {areas}'.format(
        label=area['label'][lang],
        areas=', '.join(area_assembly))
    print(area['label'][lang])
    
    # calendar source summary
    subcals = []
    for name, source_nfo in data['sources'].items():
        calurl = data['direct_url_template'].format(short_id=source_nfo['short_id'])
        subcals.append(f'* [{name}]({calurl})')
    content += '\n\n{title}:\n{subcals}'.format(
        title=data['sub_calendar_title'][lang],
        subcals='\n'.join(subcals))

    md_path = os.path.join(data_dir, f'frame.{lang}.md')
    with open(md_path, 'w', encoding='utf8') as file_obj:
        file_obj.write(content)


def json_load(path):
    with open(path, encoding='utf8') as file_obj:
        return json.load(file_obj)

if __name__ == '__main__':
    main()