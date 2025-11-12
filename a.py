import requests
import zipfile
import plistlib
import argparse
import io
import re
import os
import sys
from urllib.parse import urlparse

# --- CONFIGURATION ---
DEFAULT_ICON_URL = "https://thumbs2.imgbox.com/e6/a5/qNYLJ1Wz_t.jpeg"
CENTRAL_DIR_CHUNK_SIZE = 65536
REQUEST_TIMEOUT = 15

# --- HELPER FUNCTIONS ---
def find_info_plist_member(zip_info_list):
    """Efficiently finds the Info.plist member in a list of ZipInfo objects."""
    pattern = re.compile(r'Payload/[^/]+\.app/Info\.plist$')
    for member in zip_info_list:
        if pattern.match(member.filename):
            return member
    return None

def process_and_save_plist(ipa_url, info_data, output_file):
    """Extracts metadata and writes the final .plist file."""
    bundle_identifier = info_data['CFBundleIdentifier']
    bundle_version = info_data.get('CFBundleShortVersionString', info_data.get('CFBundleVersion'))
    app_title = info_data.get('CFBundleDisplayName', info_data.get('CFBundleName'))

    print("[*] Metadata extracted successfully:")
    print(f"    - Title: {app_title}\n    - Bundle ID: {bundle_identifier}\n    - Version: {bundle_version}")

    final_plist = {
        'items': [{
            'assets': [
                {'kind': 'software-package', 'url': ipa_url},
                {'kind': 'display-image', 'needs-shine': True, 'url': DEFAULT_ICON_URL}
            ],
            'metadata': {
                'bundle-identifier': bundle_identifier,
                'bundle-version': bundle_version,
                'kind': 'software',
                'title': app_title
            }
        }]
    }

    with open(output_file, "wb") as fp:
        plistlib.dump(final_plist, fp)
    
    print(f"\n[SUCCESS] Plist generation complete: '{output_file}'")

def generate_plist(ipa_url, output_file):
    """
    Main function that attempts the fastest method and falls back to a standard download if needed.
    """
    # --- ATTEMPT 1: ULTRA-FAST MODE (HTTP Range Requests) ---
    try:
        print("[*] Attempting ultra-fast mode (Range Request)...")
        range_header = {'Range': f'bytes=-{CENTRAL_DIR_CHUNK_SIZE}'}
        with requests.get(ipa_url, headers=range_header, stream=True, timeout=REQUEST_TIMEOUT, allow_redirects=True) as r:
            r.raise_for_status()
            content_range = r.headers.get('Content-Range')
            if not content_range or '/' not in content_range:
                # This error triggers the fallback
                raise IOError("Server does not support range requests.")
            
            end_chunk_data = io.BytesIO(r.content)
            
        with zipfile.ZipFile(end_chunk_data) as zf:
            plist_info = find_info_plist_member(zf.infolist())
            if not plist_info:
                raise FileNotFoundError("Info.plist not found in archive directory.")
        
        plist_offset = plist_info.header_offset
        read_len = plist_info.compress_size + len(plist_info.filename) + 2048
        
        plist_range_header = {'Range': f'bytes={plist_offset}-{plist_offset + read_len}'}
        with requests.get(ipa_url, headers=plist_range_header, stream=True, timeout=REQUEST_TIMEOUT) as r:
            r.raise_for_status()
            plist_chunk_data = io.BytesIO(r.content)
            
        with zipfile.ZipFile(plist_chunk_data) as plist_zf:
            with plist_zf.open(plist_info.filename) as plist_file:
                info_data = plistlib.load(plist_file)

        print("[*] Ultra-fast mode successful!")
        process_and_save_plist(ipa_url, info_data, output_file)

    except (IOError, requests.exceptions.HTTPError) as e:
        # --- FALLBACK: STANDARD DOWNLOAD MODE ---
        print(f"[!] Ultra-fast mode failed: {e}")
        print("[*] Switching to standard download mode. This may take a moment...")
        try:
            with requests.get(ipa_url, stream=True, timeout=REQUEST_TIMEOUT, allow_redirects=True) as r:
                r.raise_for_status()
                ipa_data = io.BytesIO(r.content)

            with zipfile.ZipFile(ipa_data) as zf:
                plist_path = find_info_plist_member(zf.infolist())
                if not plist_path:
                    raise FileNotFoundError("Info.plist not found in the downloaded archive.")
                with zf.open(plist_path.filename) as plist_file:
                    info_data = plistlib.load(plist_file)
            
            print("[*] Standard download mode successful!")
            process_and_save_plist(ipa_url, info_data, output_file)

        except Exception as fallback_e:
            print(f"[!!!] FATAL ERROR: Both fast mode and standard download failed.", file=sys.stderr)
            print(f"Details: {fallback_e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A robust and fast OTA .plist generator from an IPA URL."
    )
    parser.add_argument("ipa_url", help="Direct public URL to the signed .ipa file.")
    parser.add_argument("-o", "--output", help="Optional name for the output .plist file.")
    
    args = parser.parse_args()
    
    output_name = args.output
    if not output_name:
        base_name = os.path.basename(urlparse(args.ipa_url).path)
        output_name = os.path.splitext(base_name)[0] + '.plist'

    generate_plist(args.ipa_url, output_name)