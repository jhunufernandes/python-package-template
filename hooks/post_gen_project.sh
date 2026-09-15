#!/bin/sh
# Flattens the generated project into the directory where cookiecutter was run,
# so it can be used inside an already cloned (empty) repo without nesting.
{% if cookiecutter.generate_into_current_dir == "yes" -%}
generated_dir="$(pwd)"
dest="$(dirname "$generated_dir")"
find . -mindepth 1 -maxdepth 1 -exec mv -- {} "$dest/" \;
cd "$dest" || exit 1
rmdir -- "$generated_dir"
{%- endif %}
