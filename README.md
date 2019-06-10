https://img.shields.io/pypi/v/foliantcontrib.admonitions.svg

# Admonitions preprocessor for Foliant

Preprocessor which tries to make admonitions syntax available for most backends.

Admonitions are decorated fragments of text which indicate a warning, notice, tip, etc.

We use [rST-style syntax for admonitions](https://python-markdown.github.io/extensions/admonition/) which is already supported by mkdocs backend with `admonition` extension turned on. This preprocessor makes this syntax work for pandoc and slate backends.

## Installation

```bash
$ pip install foliantcontrib.admonitions
```

## Config

Just add `admonitions` into your preprocessors list. Right now the preprocessor doesn't have any options:

```yaml
preprocessors:
    - admonitions
```

## Usage

Add an admonition to your Markdown file:

```
!!! warning "optional admonition title"
    Admonition text.

    May be several paragraphs.
```

### Notes for slate

Slate has its own admonitions syntax of three types: `notice` (blue notes), `warning` (red warnings) and `success` (green notes). If another type is supplied, slate draws a blue note but without the "i" icon.

Admonitions preprocessor transforms some of the general admonition types into slate's for convenience (so you could use `error` type to display same kind of note in both slate and mkdocs). These translations are indicated in the table below:

original type | translates to
------------- | -------------
error         | warning
danger        | warning
caution       | warning
info          | notice
note          | notice
tip           | notice
hint          | notice

