# Public Website Data

The files in this directory are curated public extracts from the two local proposal PDFs in `info_to_populate_with/`.

The PDFs are intentionally ignored by Git and should remain outside the public repository. The public site should use these tabular files instead. Each row includes a compact `source` note so facts can be checked against the local PDFs without publishing the PDFs themselves.

Run `python3 build_scripts/render_pages_from_data.py` after editing the CSV files to refresh the generated Quarto partials in `_generated/`.
