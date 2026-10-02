# python-package-template

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for
bootstrapping Python packages with a standardized project structure and
configuration.

## Usage

### Inside an already cloned (empty) repo

```bash
git clone git@github.com:<you>/<newproj>.git && cd <newproj>
cookiecutter gh:jhunufernandes/python-package-template -o .
```

Keep `generate_into_current_dir` = `yes`: the generated files land directly in
the repo root, no extra folder.

### Generating a new project folder

```bash
cd ~/development
cookiecutter gh:jhunufernandes/python-package-template
```

Answer `no` to `generate_into_current_dir`: a folder named after the project is
created. Then:

```bash
cd <project_slug>
git init
gh repo create <repo> --source . --push
```

## Resulting structure

```
<project_name>/
├── .github/
│   ├── settings.yml        repo + branch protection settings (Settings App)
│   ├── CODEOWNERS          required reviewers
│   ├── SECURITY.md         security policy
│   └── workflows/          auto, deploy, docs, release, tests
├── src/<project_slug>/     the importable package
└── pyproject.toml
```

## Template's own tests

The template repository ships smoke tests (in `tests/`, not part of the
generated project) that render the template and verify the output:

```bash
python -m unittest discover -v
```
