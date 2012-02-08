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
    lang = '_' + sys.argv[-1]
    if lang=='_en':lang=''
else:
    lang='_zh'

#MIN_SIZE = 1200
MIN_SIZE = 800

def do_replacements(html, types='html'):
    # highlight ruby code
    pass

    # replace gitlinks
    def _1(m):
        p1 = m.groups()[0]
        p2 = m.groups()[0].replace('git-', 'git ')
        return "<a href=\"http://www.kernel.org/pub/software/scm/git/docs/%s.html\">%s</a>" % (p1, p2)
    html = re.sub(r'linkgit:(.*?)\[\d\]', _1, html)
    
    # replace figures
    html = re.sub(r'\[fig:(.*?)\]', r'<div class="center"><img src="images/figure/\1.png"></div>', html)
    
    # fix images in pdf
    html = html.replace('src="images', 'src="assets/images')
    
    # replace/remove gitcasts
    # bug? html no has [gitcast:xxx](yyy)
##    def _2(m):
##        print '---------\n\n'
##        if types == 'html':
##            match = re.match(r'gitcast:(.*?)\]\((.*?)\)', m.group())
##            print 'xx', match
##            if match:
##                cast = match.groups()[0].replace('_', '%2D')
##                code =  ('''<div class="gitcast">
##        <embed src="http://gitcasts.com/flowplayer/FlowPlayerLight.swf?config=%7Bembedded%3Atrue%2CbaseURL%3A%27http%3A%2F%2Fgitcasts%2Ecom%2Fflowplayer%27%2CvideoFile%3A%27http%3A%2F%2Fmedia%2Egitcasts%2Ecom%2F'''
##                + cast + 
##                '''%2Eflv%27%2CautoBuffering%3Afalse%2CautoPlay%3Afalse%7D" width="620" height="445" scale="noscale" bgcolor="111111" type="application/x-shockwave-flash" allowFullScreen="true" allowScriptAccess="always" allowNetworking="all" pluginspage="http://www.macromedia.com/go/getflashplayer"></embed>
##        <br>''' +  match.groups()[1] + '''
##        </div>''')
##        else:
##            return ''
##    html = re.sub(r'\[gitcast:.*?\]\(.*?\)', _2, html)
    return html

def main():
    ins = re.compile(r'\s*Insert\s+(\d+fig\d+).png')
    i = 0
    for root,dirs,files in os.walk('text%s' % lang):
        for name in files:
            if name.endswith('.markdown'):
                fn = os.path.join(root, name)
                html = markdown.markdown(open(fn, 'rb').read().decode('utf-8','replace'))
                html = do_replacements(html)
                open('%s-%s.html' % (root.replace('\\','_').replace('/','_'), name),
                     'wb').write(html.encode('utf-8'))
                print '-> %s-%s.html' % (root.replace('\\','_').replace('/','_'), name)
                i += 1
    print 'count:', i
if __name__ == '__main__':
    main()
