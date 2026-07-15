# GitHub Pages Deployment

This repository is configured to build and publish the Quarto website automatically with GitHub Actions.

## Initial GitHub Pages setup

1. Push this repository to GitHub.
2. In the GitHub repository, go to **Settings > Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push to the `main` branch. The workflow in `.github/workflows/publish-site.yml` will render the site and deploy `_site` to GitHub Pages.

The site will first be available at GitHub's Pages URL, usually:

```text
https://<github-user-or-org>.github.io/<repository-name>/
```

## Moving to a custom domain later

When the custom domain is ready:

1. Add the domain in **Settings > Pages > Custom domain**.
2. Add the DNS records recommended by GitHub.
3. Add the final public URL back to `_quarto.yml`, for example:

```yaml
website:
  site-url: "https://redileep.eu"
```

Leaving `site-url` unset for now avoids publishing incorrect canonical URLs while the site is served from the temporary GitHub Pages address.
