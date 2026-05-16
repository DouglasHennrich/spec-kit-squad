#!/usr/bin/env python3
"""Build the catalog submission issue body from extension.yml and the template."""

import os
import sys

import jinja2
import yaml


def load_extension(path="extension.yml"):
    with open(path) as f:
        return yaml.safe_load(f)


def render(template_path, ext, env, output_path):
    loader = jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(template_path)))
    jenv = jinja2.Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    template = jenv.get_template(os.path.basename(template_path))
    content = template.render(
        ext=ext,
        version=env["VERSION"],
        tag=env["TAG"],
        date=env["DATE"],
        download_url=env["DOWNLOAD_URL"],
    )
    with open(output_path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    template = sys.argv[1] if len(sys.argv) > 1 else ".github/templates/catalog-submission.md.j2"
    output = sys.argv[2] if len(sys.argv) > 2 else "/tmp/catalog-submission-final.md"

    ext = load_extension("extension.yml")
    render(template, ext, os.environ, output)
    print(f"Written to {output}")
