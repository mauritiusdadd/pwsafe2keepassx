#!/usr/bin/python

import sys
from xml.dom import minidom


class Converter(object):

    def __init__(self, filename):
        self.url = filename

    def convert(self):
        inp_f = open(self.url, 'r')

        data = inp_f.readlines()
        inp_f.close()

        # xml document model
        doc = minidom.Document()

        root = doc.createElement('database')
        doc.appendChild(root)

        for line in data:

            if '"' not in line:
                continue

            fields = line.split('\t')

            if len(fields) < 6:
                continue

            # uuid = fields[0].strip('"') # unused
            group = fields[1].strip('" ')
            name = fields[2].strip('" ')
            login = fields[3].strip('" ')
            passwd = fields[4].strip('" ')
            notes = fields[5].strip('" \n')

            group_node = doc.createElement('group')
            root.appendChild(group_node)

            # <group>
            group_title_node = doc.createElement('title')
            group_node.appendChild(group_title_node)
            group_title_node.appendChild(doc.createTextNode(group))

            # one <entry> per <group>
            entry_node = doc.createElement('entry')
            group_node.appendChild(entry_node)

            # <entry> -> <title>
            entry_title_node = doc.createElement('title')
            entry_title_node.appendChild(doc.createTextNode(name))
            entry_node.appendChild(entry_title_node)

            # <entry> -> <username>
            entry_uname_node = doc.createElement('username')
            entry_uname_node.appendChild(doc.createTextNode(login))
            entry_node.appendChild(entry_uname_node)

            # <entry> -> <password>
            entry_passwd_node = doc.createElement('password')
            entry_passwd_node.appendChild(doc.createTextNode(passwd))
            entry_node.appendChild(entry_passwd_node)

            # <entry> -> <comments>
            entry_comment_node = doc.createElement('comment')
            entry_comment_node.appendChild(doc.createTextNode(notes))
            entry_node.appendChild(entry_comment_node)

        print('<!DOCTYPE KEEPASSX_DATABASE>')
        print(root.toprettyxml(' ', '\n'))

if __name__ == "__main__":

    try:
        ifname = sys.argv[1]
    except IndexError:
        print("Input file name required")
        sys.exit(1)

    cc = Converter(ifname)
    cc.convert()
