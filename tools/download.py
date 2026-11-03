
import csv
import hashlib
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from urllib.robotparser import RobotFileParser

from playwright.sync_api import sync_playwright

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

RAW = Path("data/raw/handbook")
MANIFEST = Path("data/manifest.csv")

DELAY = 2
TIMEOUT = 60000
USER_AGENT = "ExamateStudentProject/1.0"

robots = {}


# --------------------------------------------------
# CHECK ROBOTS.TXT
# --------------------------------------------------

def allowed(url):
    root = "{0.scheme}://{0.netloc}".format(urlparse(url))

    if root not in robots:
        rp = RobotFileParser()
        rp.set_url(root + "/robots.txt")

        try:
            rp.read()
        except Exception as error:
            print("Could not read robots.txt:", error)
            rp = None

        robots[root] = rp

    rp = robots[root]

    # If robots.txt cannot be accessed, skip the URL
    # rather than assuming permission.
    return rp is not None and rp.can_fetch(USER_AGENT, url)


# --------------------------------------------------
# GENERATE UNIQUE PDF FILENAME
# --------------------------------------------------

def name_for(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    advisory_id = params.get("VLCODE", [None])[0]

    if advisory_id:
        return f"CERT-IN_{advisory_id}.pdf"

    # Fallback for other CERT-In pages
    path = parsed.path.strip("/").replace("/", "__")

    if not path:
        path = "homepage"

    site = parsed.netloc.replace(".", "_")

    return f"{site}__{path}.pdf"


# --------------------------------------------------
# CALCULATE SHA256 HASH
# --------------------------------------------------

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# --------------------------------------------------
# LOAD URLS
# --------------------------------------------------

def load_urls(list_file):
    with open(list_file, encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]


# --------------------------------------------------
# MAIN DOWNLOAD FUNCTION
# --------------------------------------------------

def main(list_file):

    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    urls = load_urls(list_file)

    if not urls:
        print("No URLs found in the input file.")
        return

    new_manifest = not MANIFEST.exists()

    downloaded = 0
    skipped = 0
    failed = 0

    with open(
        MANIFEST,
        "a",
        newline="",
        encoding="utf-8"
    ) as mf:

        log = csv.writer(mf)

        if new_manifest:
            log.writerow([
                "file",
                "source_url",
                "downloaded_on",
                "bytes",
                "sha256"
            ])

        with sync_playwright() as playwright:

            browser = playwright.chromium.launch()

            page = browser.new_page(
                user_agent=USER_AGENT
            )

            page.set_default_navigation_timeout(TIMEOUT)

            try:
                for index, url in enumerate(urls, start=1):

                    print(f"\n[{index}/{len(urls)}] Processing:")
                    print(url)

                    # Check URL permission
                    if not allowed(url):
                        print("Blocked or permission not confirmed by robots.txt.")
                        skipped += 1
                        continue

                    output_file = RAW / name_for(url)

                    # Avoid downloading existing files again
                    if output_file.exists():
                        print("Already exists:", output_file)
                        skipped += 1
                        continue

                    try:
                        print("Loading webpage...")

                        response = page.goto(
                            url,
                            wait_until="domcontentloaded",
                            timeout=TIMEOUT
                        )

                        if response is None or not response.ok:
                            print("Failed to load webpage.")
                            failed += 1
                            continue

                        # Wait for JavaScript and fonts
                        page.wait_for_load_state(
                            "load",
                            timeout=TIMEOUT
                        )

                        page.evaluate("""
                            () => document.fonts.ready
                        """)

                        # Small wait for dynamically rendered content
                        page.wait_for_timeout(1000)

                        # Check that meaningful page content exists
                        page_content = page.locator("body").inner_text()

                        if not page_content.strip():
                            print("Page content is empty.")
                            failed += 1
                            continue

                        # Convert webpage into PDF
                        page.pdf(
                            path=str(output_file),
                            format="A4",
                            print_background=True,
                            prefer_css_page_size=True
                        )

                        # Calculate file details
                        file_size = output_file.stat().st_size
                        digest = calculate_hash(output_file)

                        # Record successful download
                        log.writerow([
                            str(output_file),
                            url,
                            date.today().isoformat(),
                            file_size,
                            digest
                        ])

                        mf.flush()

                        downloaded += 1

                        print("PDF saved successfully:", output_file)
                        print("Size:", file_size, "bytes")
                        print("SHA256:", digest)

                    except Exception as error:

                        # Remove incomplete PDF if one was created
                        if output_file.exists():
                            output_file.unlink()

                        print("Failed:", error)
                        failed += 1

                    # Respectful delay between requests
                    time.sleep(DELAY)

            finally:
                browser.close()

    # --------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 45)
    print("CERT-IN PDF CONVERSION COMPLETED")
    print("=" * 45)

    print("Total URLs :", len(urls))
    print("Downloaded :", downloaded)
    print("Skipped    :", skipped)
    print("Failed     :", failed)

    print("\nPDF folder :", RAW)
    print("Manifest   :", MANIFEST)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python tools/download.py urls.txt")
        sys.exit(1)

    main(sys.argv[1])
