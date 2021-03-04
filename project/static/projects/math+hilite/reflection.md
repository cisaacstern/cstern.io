For reasons of visibility and organization, I keep detailed technical walk-throughs on GitHub (e.g. <a href="https://github.com/cisaacstern/nginx-wrapper/blob/main/README.md" target="_blank">the nginx-wrapper README</a>). Sometimes sharing short snippets of mathematical notation and syntax-highlighted code is useful, however, insofar as they illuminate some unique dimension of a project. (See, for example, my post about <a href="https://cstern.io/projects/ufunc-correct">ufunc-correct</a>.)


While adding this functionality was not especially complicated, it was illustrative of some basic themes in Python development. So often I have the thought, "there must be an easy way to do X," and the beauty of Python is that there almost always is.

Adding features is often a matter of quickly identifying which existing tools permit implementation with the lowest-possible overhead. The simpler the better, with the highest priority for built-ins, which minimize dependencies. When that's not an option, the obvious next choice is a well-established extension or third-party library.

For rendering math notation (from LaTeX) and syntax highlighting, the most direct path I found was via the <a href="https://python-markdown.github.io/extensions/code_hilite/" target="_blank">CodeHilite</a> and <a href="https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/" target="_blank">Arithmatex</a> extenstions for Python's standard markdown library. The following pseudo-code illustrates how those extensions are applied to a markdown file before passing it to Flask for page rendering:

```{.python .codehilite}
@app.route('/projects/<title>')
def project(title):
    
    ...
    
    cwd = "static/projects"
    projdir = (cwd, selected['name'])

    md = open_static('%s/%s/reflection.md' % projdir)

    md = markdown.markdown(md, 
            extensions=['codehilite', 'pymdownx.arithmatex'],
            extension_configs = {'pymdownx.arithmatex': 
                                    {'generic' : 'True'}
                                }
    )

    ...

    return render_template('project.html', markdown=md)
```

In the case of Arithmatex, the following MathJax scripts are also be included in the HTML template (with the CDN resources in the header and the inline JS following the body):

```{.html .codehilite}

<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

<script type="text/javascript">
    window.MathJax = {
    tex: {
    inlineMath: [ ["\\(","\\)"] ],
    displayMath: [ ["\\[","\\]"] ],
    processEscapes: true,
    processEnvironments: true
    },
    options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
    }
};
</script>
```
<p>
As simple as this feature is, it did come with some effort of time and a few additional dependencies. In that regard, it serves as a reminder to remain vigilant to the risk of "mission creep" on Python projects. The language and its community provide such a cornucopia of libraries to choose from, but the most elegant (and cost-effective to maintain) projects are likely those which do not chase unecessary features. Time will tell whether syntax-highlighted code blocks and LaTeX rendering survive through to future versions of this site, or go the way of the <a href="https://twitter.com/pradyunsg/status/1367210867524317195?s=20" target="_blank">129,703 lines of code in this Tweet</a>.
</p>