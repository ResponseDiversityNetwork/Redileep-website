# GitHub Pages Deployment

This repository builds the Quarto website automatically with GitHub Actions and publishes the rendered files to the `gh-pages` branch.

## GitHub Pages Settings

In the GitHub repository, go to **Settings > Pages** and use:

- **Source:** Deploy from a branch
- **Branch:** `gh-pages`
- **Folder:** `/ (root)`
- **Custom domain:** `redileep.eu`

The workflow in `.github/workflows/publish-site.yml` renders the site from `main`, writes the GitHub Pages custom-domain file for `redileep.eu`, and replaces the contents of the `gh-pages` branch with the rendered `_site` output.

## DNS

The apex domain `redileep.eu` should point to GitHub Pages using GitHub's Pages A records. The `www.redileep.eu` hostname should normally be configured by the domain manager as a CNAME to the GitHub Pages hostname for this organisation.

As of the custom-domain configuration, `_quarto.yml` sets:

```yaml
website:
  site-url: "https://redileep.eu"
```

This gives the rendered site the correct canonical public URL.
