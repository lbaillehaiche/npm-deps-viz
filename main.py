#!/usr/bin/env python3

import json
import urllib.request
import sys
from graphviz import Digraph
import os


if len(sys.argv) < 2:
    exit()
graph = Digraph(comment="deps", format='png')
contents = urllib.request.urlopen("https://registry.npmjs.org/" + sys.argv[1]).read()
objs = json.loads(contents.decode("utf-8"))
already_done = {sys.argv[1]}
last_version = objs['versions'][objs['dist-tags']['latest']]
stack = {}
if 'dependencies' in last_version:
    stack = {dep for dep in last_version['dependencies']}
graph.node(sys.argv[1])
for elem in stack:
    graph.edge(sys.argv[1], elem)
while len(stack) > 0:
    package = stack.pop()
    contents = urllib.request.urlopen("https://registry.npmjs.org/" + package).read()
    objs = json.loads(contents.decode("utf-8"))
    last_version = objs['versions'][objs['dist-tags']['latest']]
    graph.node(package)
    already_done.add(package)
    if 'dependencies' in last_version:
        tmp = {dep for dep in last_version['dependencies']}
        for elem in tmp:
            graph.edge(package, elem)
        stack = stack | (tmp - already_done)
graph.render('output')
os.remove('output')
