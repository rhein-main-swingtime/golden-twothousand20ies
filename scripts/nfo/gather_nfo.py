import os
import json


def main():
    p = r'C:\Users\eric\io\prj\rmst\code'
    face_group = 'https://facebook.com/groups/'
    face_public = '🌎'
    face_closed = '🔒'
    homepage = '🌐'
    file_name = 'default.{}.md'
    data = {}

    for lang in ('de', 'en'):
        file_path = os.path.join(p, file_name.format(lang))
        cat = ''
        
        with open(file_path, encoding='utf8') as fobj:
            for line in fobj:
                if line.startswith('###'):
                    cat = line.strip('###').strip()
                    print('cat: "%s"' % cat)
                    data.setdefault(cat, [])
                if line.startswith('*'):
                    this = {}
                    line = line.strip('*').strip()
                    if ' - ' in line:
                        line, this['desc'] = line.split(' - ', 1)
                    if '](' in line:
                        name, url = line.split('](', 1)
                        if homepage in name:
                            name = name.replace(homepage, '')
                            url_key = 'homepage'
                        else:
                            url_key = 'url'
                        this['name'] = name.strip('[ ')
                        if url.startswith(face_group):
                            if face_closed in url:
                                this['public'] = False
                                url = url.replace(face_closed, '')
                            elif face_public in url:
                                this['public'] = True
                                url = url.replace(face_public, '')
                            url = url.strip(') ')
                            try:
                                this['face_group'] = url[len(face_group):]
                            except ValueError:
                                this[url_key] = url
                        else:
                            if homepage in url:
                                url = url.replace(homepage, '')
                                this['homepage'] = url
                            this[url_key] = url.strip(') ')
                    data[cat].append(this)
    
    with open(os.path.join(p, 'data.json'), 'w') as fobj:
        json.dump(data, fobj, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
