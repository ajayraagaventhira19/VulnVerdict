# Dataset

## 1. Dataset Overview

VulnVerdict is a Regulation Copilot (REG) project that collects official regulatory and cybersecurity advisory information to support future retrieval and citation-based answers.

The initial dataset is collected from the official website of the Indian Computer Emergency Response Team (CERT-In).

**Source:** https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST

**Collection date:** 2026-10-23

**Current collection:** 7 HTML files, including 2 listing pages and 5 individual advisory pages.

## 2. Collected Files

| File | Source URL | Count | Licence / Terms | Downloaded on |
|---|---|---:|---|---|
| `PUBADVLIST.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |
| `PUBADVLIST02_2026.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST02&year=2026 | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |
| `PUBVLNOTES02_CIAD-2026-0053.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES02&VLCODE=CIAD-2026-0053 | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |
| `PUBVLNOTES02_CIAD-2026-0052.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES02&VLCODE=CIAD-2026-0052 | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |
| `PUBVLNOTES02_CIAD-2026-0051.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES02&VLCODE=CIAD-2026-0051 | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |
| `PUBVLNOTES02_CIAD-2026-0050.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES02&VLCODE=CIAD-2026-0050 | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |
| `PUBVLNOTES02_CIAD-2026-0049.html` | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES02&VLCODE=CIAD-2026-0049 | 1 HTML document | Official website; reuse terms not yet verified | 2026-10-23 |

**Counting note:** Each HTML file is counted as one document for this inventory. This is not a count of the rendered webpage's visual pages or the amount of advisory content.

## 3. Storage Structure

- `data/raw/` — Full downloaded source files. This directory remains local and is not committed to Git.
- `data/sample/` — A selected sample of 2–3 files for the repository.
- `data/manifest.csv` — Download records, including source URLs, download dates, file sizes, and hashes.
- `url.txt` — List of source URLs used by the downloader.
- `tools/download.py` — Script used to download the listed URLs.
- `tools/count_pages.py` — Script for counting collected HTML documents and PDF pages.

## 4. Collection Method

The initial collection was performed using `tools/download.py` with URLs listed in `url.txt`.

The downloader uses HTTP requests, checks website `robots.txt` permissions, includes a User-Agent header, and records successful downloads in `data/manifest.csv`.

## 5. Dataset Limitations and Next Steps

- This is an initial collection and does not yet meet the target of at least 50 pages or documents.
- The contents of the downloaded HTML files must be checked to confirm that they contain the expected listing and advisory information.
- Applicable website reuse and redistribution terms must be verified before sharing source content.
- The manifest must be checked to ensure that every downloaded file has a corresponding, accurate record.
- A representative sample of 2–3 files must be selected for `data/sample/`.
- Additional relevant official advisories and regulatory documents must be collected to meet the dataset target.

## 6. Reproduction

1. Install the required project dependencies.
2. Add permitted source URLs to `url.txt`.
3. Run `python tools/download.py url.txt`.
4. Run `python tools/count_pages.py` to inspect the collection totals.
5. Review `data/manifest.csv` and `data/raw/` to verify the downloaded files.
