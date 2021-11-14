"""Usage: python3 type_tree.py [type_xml_file]"""

import sys
import json
import xml.etree.ElementTree as ET
import queue


def type_xml2dict(type_xml_fp: str) -> list[dict]:
    tid = 1
    types = []
    tree = ET.parse(type_xml_fp)
    root = tree.getroot()
    nodes = queue.Queue()
    nodes.put((root, 0, 0))

    while not nodes.empty():
        node, parent_tid, parent_depth = nodes.get()
        for child in node:
            child_depth = parent_depth + 1
            if 'color' not in child.attrib:
                child.attrib['color'] = node.attrib['color']
            child_type = {
                'id':     tid,
                'name':   child.tag,
                'depth':  child_depth,
                'parent': parent_tid,
                'color':  child.attrib['color']
            }
            types.append(child_type)
            nodes.put((child, tid, child_depth))
            tid += 1

    return types


if __name__ == '__main__':
    types = type_xml2dict(sys.argv[1])
    json.dump(types, open('type.json', 'w'))
