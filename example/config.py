from defaults import *

name = "Hello, vsg!"
description = "A test website for the vsg static site generator"
topic = "Not much"
root = "http://localhost:8000/"

# An example of how to enable more Markdown extensions
extensions.add("markdown.extensions.toc")
# You can also disable them, using extensions.remove

# dirs.assets can contain files as well as directories
dirs.assets.add("test.txt")

