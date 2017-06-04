# vsg

A tiny static site generator.

## What?

vsg is a static site generator I originally wrote for
[vIRC's website][virc-site]. It is now planned to be used for the next
version of [Torbay Tech Jam's][ttj] website as well.

## Why?

There are loads of static site generators out there. Why write another?

The simple answer is that I find all of them a pain to use. They're
either too restrictive or require huge amounts of effort to set up. Some
of them are so complex that they even come with their own bootstrapping
scripts!

If I want to create a website, I don't want to spend time setting up the
program that's supposed to make things easier for me. vsg requires a
couple of configuration directives (written in Python), a template
(written in Python) and directory containing Markdown files. No complex
setup, no interactive bootstrap scripts, no arbitrary templating
restrictions. Just Python and Markdown.

## Usage

vsg is designed to be very easy to use, as long as you know Python. It
requires no configuration and makes as few assumptions about your site
as possible.

### Assumptions

While I've designed vsg not to make any unnecessary assumptions, it has
to make some:

  - Sites have an output directory named `output`
  - Sites have one main template, stored in `template.py`
  - Sites have content written in Markdown, stored in files with the
    extension `.md` in the directory `content`
  - Sites have static content such as CSS and images, stored in the
    `assets` directory. This directory (**not* its contents) is copied
    into `output`, so use paths beginning with `/assets/` to reference
    files stored in it.
  - Markdown files have optional YAML frontmatter of the following form:

        ---
        this: Is YAML
        you:
          - can
          - use
          - any
          - YAML
          - construct
          - here
        ---

        # Page Title
        This is now **Markdown**!

    Data expressed in frontmatter can be accessed inside the template
    through the page object. See `example/` for an example or the source
    code (`vsg.py`) for full details.

### Getting Started

Here, I'll walk you through how to create a new site using vsg from
scratch.

To start with, create a Git repository to version control your site:

    mkdir my-site
    cd my-site
    git init

Next up, add vsg's repo as a submodule and symlink `vsg.py` into the
root of your site as `build.py`:

    git submodule add https://github.com/vktec/vsg.git
    ln -s vsg/vsg.py build.py

Now create your template in `template.py`. Feel free to look at
`example/template.py` for reference.

Create directories for content and static assets:

    mkdir content assets

Now create `content/index.md`, which will become the homepage.

And, last but not least, build the site:

    ./build.py

[virc-site]: https://www.virc.org.uk/
[ttj]: https://torbaytechjam.org.uk/

