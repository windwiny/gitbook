#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  Use python markdown module convert markdown to html

'''

import sys
import os
import re
import time
import markdown

INDEX = '''<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
    <title>git book</title>
  </head>
  <frameset cols="25%%,75%%">
    <frame src="directory_%s.html">
    <frame name="content"src="%s">
    <noframes>
      <body>
      <p>This page uses frames. The current browser you are using does not support frames.</p>
      </body>
    </noframes>
  </frameset>
</html>'''

DIRECTORY = '''<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
    <title>git book</title>
    <style> a { font-size: 0.8em;}; </style>
  </head>
  <body>
    %s
  </body>
</html>'''

htmlbegin = '''<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
    <title>gitbook%s</title>
    <link rel=stylesheet href="assets/stylesheets/style.css">
    <style> body {
      width: 90%%;
      margin: 2em auto 0;
      padding: 0;
      background: #fff;
      -moz-border-radius: 1.5em;
      -webkit-border-radius: 1.5em;
      border-radius: 1.5em; };
    </style>
  </head>
  <body>
'''
htmlend = '''
  </body>
</html>
'''

def writefile(filename, txt):
    if type(txt) == type(u''):
        txt = txt.encode('utf-8')
    if os.path.isfile(filename) and open(filename, 'r').read() == txt:
        print ' -> %s  \t some as old, skip ..' % filename
    else:
        open(filename, 'w').write(txt)
        print ' -> %s' % filename

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

def md2html(lang):
    charpter, section, part = 0, 0, 0
    anchors = []

    i = 0
    fall = open('book%s_%s.html' % (lang, time.strftime('%Y%m%d%H%M%S')), 'wb')
    fall.write(htmlbegin % lang)
    for root,dirs,files in os.walk(lang):
        for name in files:
            if name.endswith('.markdown'):
                fn = os.path.join(root, name)
                html = markdown.markdown(open(fn, 'rb').read().decode('utf-8','replace'))
                html = do_replacements(html)
                html = html.encode('utf-8')

                # add anchors
                htmls = html.split('<h')
                if len(htmls) == 1:
                    print 'info 1 todo'
                    fall.write(html)
                    fall.write('\n')
                else:
                    fall.write(htmls.pop(0))
                    for va in htmls:
                        if not va:
                            print 'Error Format \n'
                            continue
                        fall.write('\n')
                        hl = va[0]
                        title = va[2:va.find('</h')]
                        if hl == '1':
                            section, part = 0, 0
                            charpter += 1
                            ids = 'ch%d' % (charpter)
                            anchors.append((ids, title, charpter, section, part))
                        elif hl == '2':
                            part = 0
                            section += 1
                            ids = 'ch%d-%d' % (charpter, section)
                            anchors.append((ids, title, charpter, section, part))
                        elif hl == '3':
                            part += 1
                            ids = 'ch%d-%d-%d' % (charpter, section, part)
                            anchors.append((ids, title, charpter, section, part))
                        else:
                            print 'info 2 todo', hl
                            fall.write('<h')
                            fall.write(va)
                            continue
                        fall.write('<h%s id="%s"' % (hl, ids))
                        fall.write(va[1:])

                print 'adding', fn
#                open('%s-%s.html' % (root.replace('\\','_').replace('/','_'), name),
#                     'wb').write(html.encode('utf-8'))
#                print '-> %s-%s.html' % (root.replace('\\','_').replace('/','_'), name)
                i += 1
    fall.write(htmlend)
    fall.close()
    print 'count:', i

    # create directory.html
    htmllinks = []
    for anchor, title, ch, se, pa in anchors:
        fn = os.path.split(fn)[1]
        if se == 0:
            htmllinks.append('<b><a href="%s#%s" target="content">%d %s</a></b><br />' %
                (fall.name, anchor, ch, title))
        elif pa == 0:
            htmllinks.append('&nbsp;&nbsp;<a href="%s#%s" target="content">%d.%d %s</a><br />' %
                (fall.name, anchor, ch, se, title))
        else:
            htmllinks.append('&nbsp;&nbsp;&nbsp;&nbsp;<a href="%s#%s" target="content">%d.%d.%d %s</a><br />' %
                (fall.name, anchor, ch, se, pa, title))
    writefile('directory_%s.html' % lang, DIRECTORY % '\n'.join(htmllinks))

    # create index.html
    writefile('index_%s.html' % lang, INDEX % (lang, fall.name))

def main(langs):
    for lang in langs:
        print '%s\nGenerating %s html files\n%s' % ('--' * 30, lang, '--' * 30)
        md2html(lang)

if __name__ == '__main__':
    langs = []
    if len(sys.argv) > 1:
        for d in sys.argv[1:]:
            if os.path.isdir(d):
                langs.append(d)

    if langs:
        main(langs)
    else:
        print 'Syntax:\n  %s langdir [langdir ..] ' % os.path.basename(sys.argv[0])
