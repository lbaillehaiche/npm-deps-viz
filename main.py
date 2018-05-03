#!/usr/bin/env python3

import json
import urllib.request
import sys

if len(sys.argv) < 2:
    exit()


contents = urllib.request.urlopen("https://registry.npmjs.org/" + sys.argv[1]).read()
objs = json.loads(contents.decode("utf-8"))

already_done = {sys.argv[1]}
last_version = objs['versions'][objs['dist-tags']['latest']]
stack = {}
if 'dependencies' in last_version:
    stack = {dep for dep in last_version['dependencies']}
print("digraph {")
for elem in stack:
    print(sys.argv[1].replace('-', '_').replace('.', '') + " -> " + elem.replace('-', '_').replace('.', ''))
else:
    print(sys.argv[1].replace('-', '_').replace('.', ''))

while len(stack) > 0:
    package = stack.pop()
    contents = urllib.request.urlopen("https://registry.npmjs.org/" + package).read()
    objs = json.loads(contents.decode("utf-8"))
    last_version = objs['versions'][objs['dist-tags']['latest']]
    already_done.add(package)
    if 'dependencies' in last_version:
        tmp = {dep for dep in last_version['dependencies']}
        for elem in tmp:
            print(package.replace('-', '_').replace('.', '') + " -> " + elem.replace('-', '_').replace('.', ''))
        stack = stack | (tmp - already_done)

print("}")
