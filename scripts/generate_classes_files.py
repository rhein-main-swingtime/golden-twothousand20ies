import os
import json
from pprint import pprint

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
LANGS = {'de': 'Deutsch',
         'en': 'English'}
MD_HEADER = (
"""---
title: '{title}'
taxonomy:
    category:
        - calendar
visible: false
---\n\n""")
SITE = 'https://rmswing.de/{lang}/classes-2'


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

    # iframe contents
    content += f'<iframe src="{data["embed_template"]}" style="border-width:0" width="100%" height="800" frameborder="0" scrolling="no"></iframe>\n\n'
    # gather calendar ids and insert into iframe src string
    ids = [source['embed_id'] for source in data['sources'].values()]
    colors = [data['color_tmp'].format(hex=source['color']) for source in data['sources'].values()]
    content = content.format(
        sources=data['sources_sep'].join(ids),
        colors=''.join(colors),
        lang=lang)
    
    # custom lang switcher
    for key, lang_name in LANGS.items():
        if key == lang:
            content += f' [**{lang_name}**]({SITE.format(lang=key)})'
        else:
            content += f' [{lang_name}]({SITE.format(lang=key)})'
    content += '<br>'

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
        cal_id = source_nfo['short_id']
        if '@' not in cal_id:
            cal_id = data['calendar_id_template'].format(short_id=cal_id)
        calurl = data['direct_url_template'].format(cal_id=cal_id)
        
        subcal_entry = f'* [{name}]({calurl})'
        if 'area' in source_nfo:
            subcal_entry += ' - ' + source_nfo['area']
        subcals.append(subcal_entry)
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