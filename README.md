# IPA Plist Generator (ipapro)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Sponsor @fulaq](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=ff69b4)](https://github.com/sponsors/fulaq)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**A robust, intelligent utility for automatically generating manifest (`.plist`) files for Over-The-Air (OTA) installations directly from an `.ipa` link.**

Engineered to streamline developer workflows, `ipapro` eliminates the time-consuming and error-prone process of manually creating `.plist` files.

![demo.gif](https://i.imgur.com/your-demo.gif)
*(Note: Replace this link with an actual screen recording of your tool in action for maximum professional impact.)*

---

## Overview

Distributing in-house or testing applications for iOS often requires a manifest `.plist` file to manage the OTA installation. This process typically involves manually extracting metadata such as the `bundle-identifier`, `bundle-version`, and `title` from the `.ipa` archive.

**ipapro** fully automates this workflow. It features an adaptive fetching mechanism that intelligently chooses the best strategy:

1.  **Ultra-fast Mode:** Attempts to read metadata from the remote URL by fetching only a few kilobytes of data, without downloading the entire file.
2.  **Reliable Mode:** If the server does not support partial fetching, it seamlessly falls back to a standard download method, guaranteeing 100% success.

The result is a tool that is both exceptionally fast and absolutely reliable, allowing you to focus on what matters: development.

## Key Features

-   🚀 **Adaptive Fetching:** Intelligently uses HTTP Range Requests for maximum speed and automatically falls back when necessary, ensuring universal server compatibility.
-   🧩 **Automatic Metadata Extraction:** Accurately parses the `bundle-identifier`, `bundle-version`, and `title` directly from the IPA archive.
-   ⚡ **High Performance:** Minimizes network and memory usage, delivering near-instant results on supported servers.
-   📂 **Smart File Naming:** Automatically generates a `.plist` filename that matches the input `.ipa` for easy organization.
-   ⚙️ **Built for Automation:** Perfect for integration into CI/CD pipelines, build scripts, and other automated workflows.
-   Minimal **Dependencies:** Requires only the `requests` library for easy setup and execution anywhere.

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/fulaq/ipapro.git
    cd ipapro
    ```

2.  **Install Dependencies:**
    ```bash
    pip install requests
    ```
    *(Alternatively, `pip install -r requirements.txt` if you create a requirements file.)*

## Usage

The syntax is clean and straightforward. Simply provide a direct URL to your signed `.ipa` file.

#### **Basic Syntax:**

```bash
python ipapro.py [IPA_URL]
```

#### **Example:**

```bash
python ipapro.py https://github.com/Nyasami/Ksign/releases/download/v1.5/Ksign.ipa
```

#### **Output:**

The tool processes the URL and generates a perfectly formatted `Ksign.plist` in the same directory.

```
[*] Processing URL: https://github.com/Nyasami/Ksign/releases/download/v1.5/Ksign.ipa
[!] Ultra-fast mode failed: Server does not support range requests.
[*] Switching to standard download mode. This may take a moment...
[*] Standard download mode successful!
[*] Metadata extracted successfully:
    - Title: Ksign
    - Bundle ID: com.apple.Ksign
    - Version: 1.5

[SUCCESS] Plist generation complete: 'Ksign.plist'
```

#### **Options:**
-   `-o, --output`: Specify a custom output filename.
    ```bash
    python ipapro.py [IPA_URL] -o MyAwesomeApp.plist
    ```

---

## Licensing

`ipapro` is available under a **dual-license** model.

#### **Community License (AGPL v3)**
For personal use, non-commercial, and open-source projects, `ipapro` is free to use under the **GNU Affero General Public License v3.0**.

#### **Commercial License**
If you intend to use `ipapro` in proprietary, closed-source commercial products, services, or internal workflows, **you must purchase a commercial license.**

A commercial license grants you the freedom to use the software without the obligations of the AGPL v3 and includes priority support.

To purchase a commercial license, please contact us at: **[fulaq.dev@gmail.com](mailto:fulaq.dev@gmail.com)**

## Contributing & Support

-   **Report Bugs or Request Features:** Please open an [Issue](https://github.com/fulaq/ipapro/issues) on GitHub.
-   **Sponsor the Project:** If this tool provides value to you or your company, please consider [sponsoring its development](https://github.com/sponsors/fulaq) to support ongoing maintenance and new features.

---

© 2025, Fulaq. All rights reserved.
