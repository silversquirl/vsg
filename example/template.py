# encoding: cinje

:def navbar pages, current
<nav>
  :for p in sorted(pages, key=lambda p: p.order or 0)
    <a&{href=p.path, class_=("active" if p == current else None)}>
      ${p.title}
      :if p.children
        #{''.join(navbar(p.children, current))}
      :end
    </a>
  :end
</nav>
:end

:def render site, page

<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta name="description"&{content=site.description}>
    <meta name="subject"&{content=site.topic}>
    <meta name="rating" content="General">

    <link href="humans.txt" rel="author">

    <title>
      :if page.title
        ${page.title} |
      :end
      ${site.name}
    </title>
    <link&{href=site.root} rel="index">

    <link href="/assets/css/normalize.css" rel="stylesheet">
    <link href="/assets/css/main.css" rel="stylesheet">
  </head>

  <body>
    #{''.join(navbar(site.pages, page))}

    <main>
    #{page.body}
    </main>

    <footer>
      <a href="http://www.vultr.com/?ref=6873807">
        <img src="/assets/images/vultr-badge.svg" id="vultrimg">
      </a>
    </footer>
  </body>
</html>

:end

# vim: ft=cinje ts=2 sw=2

