#!/usr/bin/env python3
"""Render Quarto partials from the public CSV data layer."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "_generated"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write(name: str, body: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(body.rstrip() + "\n", encoding="utf-8")


def split_items(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def section_header(title: str) -> str:
    return f"## {title}\n\n"


def render_index() -> None:
    facts = {row["key"]: row["value"] for row in read_csv("site_facts.csv")}
    body = f"""::: {{.section}}
::: {{.intro-lead}}
## A European doctoral network for response diversity

ReDiLEEP brings together universities, research institutes, policy bodies, NGOs, and industry partners to train doctoral candidates in the science and application of response diversity for resilient ecosystems.
:::

::: {{.fact-list}}
**{facts["doctoral_candidates"]}** doctoral candidates  
**{facts["listed_organisations"]}** listed organisations  
**{facts["response_diversity_network_members"]}** Response Diversity Network members
:::
:::

::: {{.section .band}}
## What The Network Will Do

::: {{.text-list}}
::: {{.text-item}}
### Research

{facts["scientific_objective_2"]}
:::

::: {{.text-item}}
### Training

{facts["training_objective_2"]}
:::

::: {{.text-item}}
### Impact

{facts["scientific_objective_3"]}
:::
:::
:::
"""
    write("index.md", body)


def render_about() -> None:
    facts = {row["key"]: row["value"] for row in read_csv("site_facts.csv")}
    wps = read_csv("work_packages.csv")
    body = """::: {.section}
::: {}
## Aim

The network will train doctoral researchers to work across disciplinary and sector boundaries, with a focus on how response diversity supports socio-ecological resilience under environmental stress. The programme combines 13 linked research projects, network-wide schools, secondments, and shared supervision.
:::

::: {}
## Approach

ReDiLEEP links field evidence, experimental systems, quantitative modelling, synthesis, and policy engagement. The network is built to help doctoral researchers move confidently between data, theory, communication, and real-world application.
:::
:::

::: {.section .band}
## Objectives

::: {.text-list}
"""
    for key in ("scientific_objective_1", "scientific_objective_2", "scientific_objective_3"):
        body += f"::: {{.text-item}}\n### {key.replace('_', ' ').title().replace('Scientific Objective ', 'S')}\n\n{facts[key]}\n:::\n\n"
    body += "::: \n:::\n\n::: {.section .text-list}\n## Work Packages\n\n"
    for wp in wps:
        body += f"::: {{.text-item .wide-item}}\n### {wp['wp']}: {wp['title']}\n\n{wp['objectives']}\n\n**Lead:** {wp['lead']} | **Months:** {wp['start_month']}-{wp['end_month']} | **Doctoral projects:** {wp['dcs_involved']}\n:::\n\n"
    body += ":::"
    write("about.md", body)


def render_research() -> None:
    projects = read_csv("projects.csv")
    wps = read_csv("work_packages.csv")
    body = "::: {.section .text-list}\n"
    for wp in wps[:3]:
        body += f"::: {{.text-item .wide-item}}\n## {wp['wp']}: {wp['title']}\n\n{wp['objectives']}\n\n{wp['tasks']}\n:::\n\n"
    body += ":::\n\n::: {.section .band}\n## Doctoral Projects\n\n::: {.project-list .text-list}\n"
    for row in projects:
        body += f"**{row['dc']}, {row['host']}:** {row['title']}  \n{row['summary']}  \n*Focus:* {row['methods_or_focus']}\n\n"
    body += ":::\n:::\n"
    write("research.md", body)


def render_training() -> None:
    events = read_csv("training_events.csv")
    body = "::: {.section .text-list}\n"
    for row in events:
        ects = "" if row["ects"] == "0" else f" | {row['ects']} ECTS"
        body += f"::: {{.text-item .wide-item}}\n## {row['event']}\n\n**{row['kind']} | Month {row['month']} | Lead: {row['lead']}{ects}**  \n{row['description']}\n:::\n\n"
    body += ":::\n"
    write("training.md", body)


def render_partners() -> None:
    rows = read_csv("partners.csv")
    counts = Counter(row["category"] for row in rows)
    body = "::: {.section .partner-list}\n"
    for row in rows:
        body += f"::: {{.partner-entry}}\n### {row['name']}\n\n**{row['short_name']} | {row['category']} | {row['country']}**  \n{row['department_or_unit']}  \nScientist in charge: {row['scientist_in_charge'] or 'to be confirmed'}.  \n{row['role']}\n:::\n\n"
    body += f""":::

::: {{.section .band}}
## Consortium Snapshot

The public data layer currently lists {counts['Beneficiary']} beneficiaries, {counts['Associated partner']} associated partners, and {counts['Associated partner linked to beneficiary']} associated partner linked to a beneficiary.
:::
"""
    write("partners.md", body)


def render_vacancies() -> None:
    projects = read_csv("projects.csv")
    supervisors = {row["dc"]: row for row in read_csv("supervisors.csv")}
    body = """::: {.section}
::: {}
## Recruitment Status

Recruitment details are being prepared. This page will include eligibility requirements, application links, deadlines, salary and contract information, host institution contacts, and final project descriptions.

[Contact the network](contact.qmd){.btn .btn-primary}
:::

::: {.callout-panel}
### MSCA Mobility Rule

Doctoral Network recruitment normally includes MSCA eligibility and mobility requirements. Add the official wording here after the vacancy calls are approved.
:::
:::

::: {.section .band}
## Planned Doctoral Projects

::: {.project-list}
"""
    for row in projects:
        sup = supervisors.get(row["dc"], {})
        body += f"**{row['dc']}, {row['host']}:** {row['title']}  \nHost: {row['host']}; PhD-awarding entity: {row['phd_awarding_entity']}; planned start month: {row['planned_start_month']}.  \nMain supervisor: {sup.get('main_supervisor', 'to be confirmed')}. Co-supervisor(s): {sup.get('co_supervisors', 'to be confirmed')}.\n\n"
    body += ":::\n:::\n"
    write("vacancies.md", body)


def render_tables() -> None:
    deliverables = read_csv("deliverables.csv")
    milestones = read_csv("milestones.csv")
    body = section_header("Deliverables")
    body += "| No. | Title | WP | Lead | Due month |\n|---|---|---:|---|---:|\n"
    for row in deliverables:
        body += f"| {row['no']} | {row['title']} | {row['wp']} | {row['lead']} | {row['due_month']} |\n"
    body += "\n" + section_header("Milestones")
    body += "| No. | Title | WP | Lead | Due month |\n|---|---|---|---|---:|\n"
    for row in milestones:
        body += f"| {row['no']} | {row['title']} | {row['related_wp']} | {row['lead']} | {row['due_month']} |\n"
    write("deliverables_and_milestones.md", body)


def main() -> None:
    render_index()
    render_about()
    render_research()
    render_training()
    render_partners()
    render_vacancies()
    render_tables()


if __name__ == "__main__":
    main()
