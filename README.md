# ReDiLEEP Website

This repository contains the source for the ReDiLEEP public website. The site is built with [Quarto](https://quarto.org/) and published with GitHub Pages via the workflow in `.github/workflows/publish-site.yml`.

## Submitting New Content

The easiest way to submit new website content, such as a news item, event notice, vacancy update, partner update, or correction to existing text, is to open a GitHub issue (see below for how to do this).

For a new news item, please include as much of the following as possible:

- proposed title;
- short summary, one or two sentences;
- full text, or bullet points that can be turned into text;
- preferred publication date;
- relevant category, for example `recruitment`, `funding`, `event`, `training`, or `network`;
- image suggestion, if any;
- links that should be included;
- contact person for checking details before publication.

You do not need to write the item in Quarto format. Plain text in the issue is fine. If the content is time-sensitive, include the deadline or desired publication date in the issue title.

The content will be reviewed and then posted.

## Using Github Issues

To create an issue:

1. Go to this repository on GitHub.
2. Click the **Issues** tab.
3. Click **New issue**.
4. Give the issue a short, clear title.
5. Describe the requested change, including the page URL or page name if relevant.
6. Assign the issue to one of the available team members.
7. Click **Submit new issue**.

GitHub's own instructions are here: [Creating an issue - GitHub Docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).

Once the public GitHub repository URL is final, this README can include a direct link to the repository's issue form, usually:

```text
https://github.com/<owner>/<repository>/issues/new
```
If opening a GitHub issue is not possible, email Owen with the proposed change.

## Suggesting Changes

The preferred way to propose changes to the website or its content is to open a GitHub issue in this repository. An issue is a good place to request text edits, report broken links, suggest new pages, flag outdated information, or discuss website structure before someone edits the source files.

After the metadata, write the news post in Markdown/Quarto text. The website will rebuild automatically after the change is committed and pushed to `main`.

