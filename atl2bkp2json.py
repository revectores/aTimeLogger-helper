"""Usage: python3 atl2bkp2json.py [backup_file] [type_json_file]"""

import sys
import json
import xml.etree.ElementTree as ET


def extract_logs(atl2bkp_fp: str, type_fp: str) -> list[dict]:
    tree = ET.parse(atl2bkp_fp)
    root = tree.getroot()

    intervals = []
    types = json.load(open(type_fp))
    type_name2id = {t['name']: t['id'] for t in types}

    for group in root.find('categories').findall('group'):
        print(group.find('name').text)
        for category in group.iter('category'):
            name = category.find('name').text
            print('\t' + name)
            for log in category.find('logs').iter('log'):
                interval = log.find('intervals').find('interval')

                intervals.append({
                    'type':     type_name2id[name],
                    'start':    int(interval.find('from').text),
                    'end':      int(interval.find('to').text),
                    'reported': False,
                    'report':   ""
                })

    return intervals


if __name__ == '__main__':
    intervals = extract_logs(sys.argv[1], sys.argv[2])
    json.dump(intervals, open('log.json', 'w'))
