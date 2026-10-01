#!/bin/sh
# Flattens the generated project into the directory where cookiecutter was run,
# so it can be used inside an already cloned repo (e.g. one created from
# jhunufernandes/github-template) without nesting.
#
# Existing files are merged instead of failing:
#   - .gitignore: generated rules are appended to the existing file
#   - directories (e.g. .github): contents are merged
#   - other files: generated version wins
{% if cookiecutter.generate_into_current_dir == "yes" -%}
generated_dir="$(pwd)"
dest="$(dirname "$generated_dir")"

if [ -f "$dest/.gitignore" ] && [ -f .gitignore ]; then
  printf '\n# --- Python (python-package-template) ---\n' >> "$dest/.gitignore"
  cat .gitignore >> "$dest/.gitignore"
  rm -f .gitignore
fi

cp -R ./. "$dest/"
cd "$dest" || exit 1
rm -rf -- "$generated_dir"
{%- endif %}
