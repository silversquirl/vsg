# vsg

A tiny static site generator.

## What?

vsg is a static site generator I originally wrote for
[vIRC's website][virc-site]. It is now planned to be used for the next
version of [Torbay Tech Jam's][ttj] website as well.

Templates are written in [cinje][cinje], content is written in
[Markdown][md].

[virc-site]: https://www.virc.org.uk/
[ttj]: https://torbaytechjam.org.uk/
[cinje]: https://github.com/marrow/cinje
[md]: https://daringfireball.net/projects/markdown/basics

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

- Sites have an output directory
- Sites have one main template, stored in `template.py`
- Sites have content written in Markdown, stored in files with the
  extension `.md` (**not** `.markdown`)
- Sites have static content such as CSS and images, stored in the
  "assets" directories. These directories are copied into the output
  directory, so use paths beginning with their names (eg. `assets/file`)
  to reference files stored in them.
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

Let's go through how to create a new vsg site from scratch.

To start with, create a Git repository to version control your site:

    mkdir my-site
    cd my-site
    git init

Next up, add vsg's repo as a submodule and symlink `vsg.py` into the
root of your site as `build.py`:

    git submodule add https://github.com/vktec/vsg.git
    ln -s vsg/vsg.py build.py

Now, install vsg's dependencies. You _can_ do it with a virtualenv,
but for the purposes of this README, we'll just do it as a user-level
PyPi installation:

    pip install --user -U -r ./vsg/requirements.txt

(Make sure to use the Python 3 version of the `pip` utility on your
system - otherwise vsg **won't** see the installed dependencies!)

Now put configuration in `config.py` and write a template in
`template.py`. Feel free to look at `example/template.py` for reference.

Create directories for content and static assets:

    mkdir content assets

Now create `content/index.md`, which will become the homepage.

And, last but not least, build the site:

    ./build.py

