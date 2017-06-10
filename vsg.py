#!/usr/bin/env python3
# A super minimal static site generator
# Written by Samadi van Koten

import sys
from warnings import warn
if sys.version_info < (3, 2):
    raise RuntimeError("This script requires Python 3.2 or greater (3.4.1 minimum recommended)")
elif sys.version_info < (3, 4, 1):
    warn("This script may run incorrectly on versions of Python less than 3.4.1", RuntimeWarning)


import re
import os
from distutils import dir_util # Weird place for a recursive directory copy...
from collections import namedtuple
import cinje # Template engine
import markdown
import frontmatter

# User-defined modules
sys.path.insert(0, "") # Allow importing from the current directory

import template # Yes, cinje is just that awesome

# Configuration
import types
defaults = types.ModuleType("vsg.defaults")
defaults.extensions = {
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.sane_lists",
        }

defaults.dirs = types.SimpleNamespace()
defaults.dirs.content = "content"
defaults.dirs.output = "output"
defaults.dirs.assets = {"assets"}

sys.modules["vsg.defaults"] = sys.modules["defaults"] = defaults
import config
del sys.modules["vsg.defaults"], sys.modules["defaults"]

markdown_translator = markdown.Markdown(extensions=config.extensions)

class Page:
    def __init__(self,
            fn, prefix=config.dirs.content,
            children=[], md=markdown_translator):

        if hasattr(fn, "path"): # Handle DirEntry objects
            fn = fn.path

        page = frontmatter.load(fn)
        self._meta = page.metadata

        # Convert the markdown to HTML
        self.body = md.convert(page.content)
        md.reset() # Resetting improves speed, apparently

        # Create the output path
        self.path = fn.lstrip(prefix).rstrip("md") + "html"

        self.children = children

    def __contains__(self, name):
        return name in self._meta or name in dir(self)

    def __getattr__(self, name):
        return self._meta[name] if name in self._meta else None

def read_pages(content=config.dirs.content):
    content = os.path.normcase(os.path.normpath(content))

    def read_subdir(d):
        assert d.is_dir()

        index_path = os.path.join(d.path, "index.md")
        if not os.path.isfile(index_path):
            print(d.path + " does not contain index.md; skipping")

        children = []
        for de in os.scandir(d.path):
            if de.is_dir():
                children.extend(read_subdir(de))
                continue

            if de.name != "index.md":
                children.append(Page(de, content))

        yield Page(index_path, content, children)

    for de in os.scandir(content):
        if de.is_dir():
            yield from read_subdir(de)
            continue

        # Check if it's a markdown file
        if not de.name.endswith(".md"):
            print(fn + ": Not a markdown file")
            continue

        yield Page(de, content)

def save_pages(pages,
        output=config.dirs.output,
        assets=config.dirs.assets):

    for page in pages:
        # Render the template with the Page object
        out_html = "".join(template.render(config, page))

        # Can't use os.path.join because page.path is absolute
        outpath = os.path.normpath(output + page.path)

        # Create the parent directory if necessary
        outdir = os.path.dirname(outpath)
        os.makedirs(outdir, exist_ok=True)

        # Write the HTML to the output file
        with open(outpath, "w") as f:
            f.write(out_html)

        # Recurse through tree
        if page.children:
            save_pages(page.children, output, assets)

def build(pages=None,
        output=config.dirs.output,
        assets=config.dirs.assets):

    if not pages:
        pages = config.pages

    if isinstance(assets, str):
        assets = {assets}

    # Create the output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)

    # Recursively copy the assets directories into the output directory
    for d in assets:
        dir_util.copy_tree(d,
                os.path.join(output, os.path.basename(d)),
                update=1)

    save_pages(pages, output, assets)

if __name__=="__main__":
    config.pages = list(read_pages())
    build()

