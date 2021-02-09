def render_markdown_template(md_template, context):
    """Populates and renders a markdown template."""
    env = Environment()
    template = env.from_string(md_template)
    rendered_md = template.render(context=context)
    return rendered_md
