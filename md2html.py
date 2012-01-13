#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  only use python markdown module convert markdown to html

'''

import sys
import os
import re
import markdown

if len(sys.argv) > 1:
    lang = sys.argv[-1]
else:
    lang='zh'

def main():
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    if not os.path.isdir('html_%s' % lang):
        os.mkdir('html_%s' % lang)
    ins = re.compile(r'\s*Insert\s+(\d+fig\d+).png')
    i = 0
    for root,dirs,files in os.walk('text_%s' % lang):
        for name in files:
            if name.endswith('.markdown'):
                fn = os.path.join(root, name)
                if not os.path.isdir('tmp/%s' % root):
                    os.makedirs('tmp/%s' % root)
                f1 = open(fn, 'r')
                f2 = open('tmp/%s' % fn, 'w')
                for line in f1:
                    matches = ins.match(line)
                    if matches:
                        n = 'figures/%s-tn.png' % matches.group(1)
                        line = "![%s](%s)\n" % (n, n)
                    f2.write(line)
                f1.close()
                f2.close()
                markdown.markdownFromFile(
                    input=f2.name, 
                    output='html_zh/%s-%s.html' % (root.replace('\\','_').replace('/','_'), name))
                print '-> html_zh/%s-%s.html' % (root.replace('\\','_').replace('/','_'), name)
                i += 1
    print 'count:', i
if __name__ == '__main__':
    main()
