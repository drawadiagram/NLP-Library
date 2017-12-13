# Split up a text file based on some regex, like "CHAPTER" or something like that

import re

src_file = '/home/mason/topics/hist.txt'

f = open(src_file)
p = re.compile('CHAPTER [A-Z]*')

def write_line_to_chapter(line, chap_num):
    with open('hist-%03d.txt' % chap_num, 'a+') as g:
        g.write(line)

with open('/home/mason/topics/hist.txt') as f:
    part = 0
    for line in f:
        if not p.match(line):
            write_line_to_chapter(line, part)
            continue
        else:
            part += 1
            write_line_to_chapter(line, part)
            continue
