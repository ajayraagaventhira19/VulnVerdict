# VulnVerdict

## Problem

Small IT teams struggle to keep track of security vulnerabilities affecting the software they use. CERT-In publishes security advisories and vulnerability warnings, while the National Vulnerability Database (NVD) contains thousands of CVE records. Manually reviewing these sources and checking software versions takes time, and teams may miss critical vulnerabilities. VulnVerdict helps teams identify potentially affected software versions, prioritise risks by severity, and understand recommended fixes using AI-generated explanations supported by citations to trusted sources.

## Who it is for

- Security analysts and IT administrators at small and medium-sized software companies.
- Developers who need to check their project's software dependencies for known security vulnerabilities.

## Signature feature

**Am I affected?** — Users enter a list of software names and versions, and VulnVerdict matches them against CERT-In advisories and NVD CVE records. It displays potentially affected versions, vulnerability identifiers, severity, recommended fixes, and citations to the original sources.

## Hardest problem (my interview story)

The hardest problem is protecting the AI system from prompt injection and unsafe handling of untrusted security documents. Advisory text and CVE descriptions may contain malicious instructions intended to manipulate the AI into ignoring its rules or revealing sensitive information. I plan to separate retrieved document content from system instructions, validate inputs and outputs, redact sensitive internal hostnames and IP addresses where appropriate, and test the defences using a red-team dataset containing at least 50 attack prompts. I will evaluate the system's ability to resist these attacks while still providing accurate, evidence-backed vulnerability assessments.

## Dataset

| **Source** | **Link** | **Documents** | **Pages** | **Licence / terms** |
| ---------- | -------- | ------------- | --------- | ------------------- |
| CERT-In Public Advisories | [Official website](https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVLIST) | To be collected and counted | To be measured | Verify the applicable website terms and reuse conditions |
| NVD CVE Records | [NVD Data Feeds](https://nvd.nist.gov/vuln/data-feeds) | Target: 20,000+ CVE records | Not applicable to structured records | Review NVD data usage and attribution guidance |

## 10 real questions

See [docs/QUESTIONS.md](https://github.com/ajayraagaventhira19/VulnVerdict/blob/main/docs/QUESTIONS.md).
