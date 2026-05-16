#!/usr/bin/env python3
"""
Knowledge Base Extraction Script for Rema App Test Cases.

Parses test case files and generates structured knowledge base markdown files
for use by the rema-app-expert agent and bug-verify skill.

Usage:
    python3 extract_knowledge.py                          # Full extraction
    python3 extract_knowledge.py --feature "Favorite Recipes"  # Single feature
    python3 extract_knowledge.py --validate               # Check freshness
"""

import json
import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = SCRIPT_DIR / "extraction-config.json"

# Patterns for extracting structured info from test cases
SCREEN_PATTERNS = [
    r"(?:Navigate|Go|Switch) to (?:the )?(.+?)(?:\s+screen|\s+tab|\s+page|\s+view)",
    r"User is on (?:the )?(.+?)(?:\s+screen|\s+tab|\s+page|\s+view)",
    r"(?:Open|Launch) (?:the )?(.+?)(?:\s+screen|\s+tab|\s+page|\s+view)",
    r"Navigate to (.+?)(?:\s+checkout|\s+settings)",
]

ELEMENT_PATTERNS = [
    r'(?:Tap|Click|Press|Toggle|Select|Observe|Verify|Check) (?:the |on the |on )?["\']?(.+?)["\']?\s+(?:button|icon|toggle|tab|link|field|selector|bar|menu|item|option|section|area|sheet)',
    r'(?:Tap|Click|Press) ["\'](.+?)["\']',
    r'button (?:labeled|with text|showing) ["\'](.+?)["\']',
    r'(?:button|text) ["\'](.+?)["\']',
]

ACTION_VERB_PATTERNS = [
    r"(Tap|Click|Press|Toggle|Select|Enter|Type|Scroll|Swipe|Navigate|Open|Close|Dismiss|Search|Wait|Observe|Verify|Check|Compare|Force close|Relaunch|Log in|Log out|Grant|Deny)",
]

API_PATTERN = re.compile(
    r"(GET|POST|PUT|DELETE|PATCH)\s+(/\S+)"
)

FEATURE_FLAG_PATTERN = re.compile(
    r"(?:feature\s*flag|flag)\s+(\S+)",
    re.IGNORECASE,
)

PLATFORM_PATTERNS = {
    "ios": re.compile(r"\b(?:iOS|iPhone|iPad|XCUIElement|\.ios\.)\b", re.IGNORECASE),
    "android": re.compile(r"\b(?:Android|android\.widget|\.android\.)\b", re.IGNORECASE),
}

# ----- Test Case Parser -----

class TestCase:
    def __init__(self, case_id, title, priority=None):
        self.id = case_id
        self.title = title
        self.priority = priority
        self.preconditions = []
        self.actions = []
        self.expected = []
        self.api_lines = []
        self.raw_text = ""

    def __repr__(self):
        return f"TestCase({self.id}: {self.title})"


def parse_test_cases(filepath):
    """Parse a test case file and return a list of TestCase objects."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    cases = []
    current_case = None
    current_section = None

    for line in content.split("\n"):
        stripped = line.strip()

        # Skip empty lines and section headers (=== ... ===)
        if not stripped:
            continue
        if stripped.startswith("===") and stripped.endswith("==="):
            continue

        # Detect test case header: ID | Title [Priority]
        # ID can be like "FAVREC-01" or "RecommendedList 01" or "FRA-01"
        header_match = re.match(
            r"^(.+?)\s*\|\s*(.+?)(?:\s+\[(P\d)\])?\s*$", stripped
        )
        if header_match and not line.startswith("    ") and not line.startswith("\t"):
            # Validate that the ID part looks like a test case ID (not a table row)
            candidate_id = header_match.group(1).strip()
            if re.match(r"^[\w\s-]+$", candidate_id) and len(candidate_id) <= 40:
                if current_case:
                    cases.append(current_case)
                case_id = candidate_id
                title = header_match.group(2).strip()
                priority = header_match.group(3)
                current_case = TestCase(case_id, title, priority)
                current_section = None
                continue

        # Also detect headers without pipe: "Feature Title" at top of file
        if not current_case and not line.startswith(" ") and not line.startswith("\t"):
            # This is a file-level title, skip
            continue

        if not current_case:
            continue

        # Detect section headers
        section_lower = stripped.lower()
        if section_lower == "preconditions":
            current_section = "preconditions"
            continue
        elif section_lower == "actions":
            current_section = "actions"
            continue
        elif section_lower == "expected":
            current_section = "expected"
            continue
        elif section_lower in ("api", "api:"):
            current_section = "api"
            continue

        # Collect content into current section
        if current_section and stripped:
            content_text = stripped
            if current_section == "preconditions":
                current_case.preconditions.append(content_text)
            elif current_section == "actions":
                current_case.actions.append(content_text)
            elif current_section == "expected":
                current_case.expected.append(content_text)
            elif current_section == "api":
                current_case.api_lines.append(content_text)

        current_case.raw_text += line + "\n"

    if current_case:
        cases.append(current_case)

    return cases


def parse_regression_test_cases(filepath):
    """Parse a regression test case file with indentation-based hierarchy.

    Handles two patterns:
    1. Group (level 0) -> Test Case (level 1) -> Section (level 2) -> Content (level 3)
    2. Test Case (level 0) -> Section (level 1) -> Content (level 2)

    Detection: if a level-0 item has section headers (Actions/Expected/Preconditions)
    as direct children, it's a test case. Otherwise it's a group.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    SECTION_NAMES = {"preconditions", "preconditons", "actions", "expected"}

    # Parse lines into (indent_chars, text), skip blanks
    raw_entries = []
    for line in raw_lines:
        if not line.strip():
            continue
        stripped = line.rstrip()
        indent = len(stripped) - len(stripped.lstrip())
        raw_entries.append((indent, stripped.strip()))

    if not raw_entries:
        return []

    # Determine indent unit from first indented line
    non_zero = [ind for ind, _ in raw_entries if ind > 0]
    indent_unit = min(non_zero) if non_zero else 4

    # Normalize to levels
    entries = [(ind // indent_unit, text) for ind, text in raw_entries]

    # Module prefix from filename (e.g., "01_app_install.txt" -> "REG01")
    module_match = re.match(r"(\d+)_", os.path.basename(filepath))
    module_num = module_match.group(1) if module_match else "00"

    def get_children_end(start_idx):
        """Get the index after the last child of entries[start_idx]."""
        parent_level = entries[start_idx][0]
        end = start_idx + 1
        while end < len(entries) and entries[end][0] > parent_level:
            end += 1
        return end

    def has_section_children(idx):
        """Check if the item at idx has section headers as direct children."""
        parent_level = entries[idx][0]
        end = get_children_end(idx)
        for j in range(idx + 1, end):
            if entries[j][0] == parent_level + 1 and entries[j][1].lower().rstrip(":") in SECTION_NAMES:
                return True
        return False

    def extract_case_from(idx, group_name=None):
        """Extract a TestCase from entries[idx] which is a test case title."""
        nonlocal case_counter
        case_counter += 1
        case_id = f"REG{module_num}-{case_counter:02d}"

        level, text = entries[idx]
        title = f"{group_name} > {text}" if group_name else text
        case = TestCase(case_id, title)

        section_level = level + 1
        current_section = None
        end = get_children_end(idx)

        for j in range(idx + 1, end):
            j_level, j_text = entries[j]
            j_lower = j_text.lower().rstrip(":")

            if j_level == section_level and j_lower in SECTION_NAMES:
                current_section = "preconditions" if j_lower in ("preconditions", "preconditons") else j_lower
            elif j_level > section_level and current_section:
                if current_section == "preconditions":
                    case.preconditions.append(j_text)
                elif current_section == "actions":
                    case.actions.append(j_text)
                elif current_section == "expected":
                    case.expected.append(j_text)
                case.raw_text += j_text + "\n"

        return case

    cases = []
    case_counter = 0
    i = 0

    while i < len(entries):
        level, text = entries[i]

        if level != 0:
            i += 1
            continue

        if has_section_children(i):
            # Level 0 is a test case (sections at level 1)
            case = extract_case_from(i)
            cases.append(case)
        else:
            # Level 0 is a group — children at level 1 are test cases or bare titles
            group_name = text
            group_end = get_children_end(i)
            j = i + 1
            while j < group_end:
                if entries[j][0] == 1:
                    if has_section_children(j):
                        case = extract_case_from(j, group_name=group_name)
                        cases.append(case)
                    else:
                        # Bare title (no sections) — create a minimal case
                        case_counter += 1
                        case_id = f"REG{module_num}-{case_counter:02d}"
                        bare_case = TestCase(case_id, f"{group_name} > {entries[j][1]}")
                        # Collect any sub-lines as expected behavior hints
                        k = j + 1
                        while k < group_end and entries[k][0] > 1:
                            bare_case.expected.append(entries[k][1])
                            bare_case.raw_text += entries[k][1] + "\n"
                            k += 1
                        cases.append(bare_case)
                    # Skip past this child's descendants
                    j = get_children_end(j)
                else:
                    j += 1

        i = get_children_end(i)

    return cases


# ----- Knowledge Extractors -----

def extract_screens(cases):
    """Extract screen names mentioned across test cases."""
    screens = defaultdict(lambda: {"mentions": 0, "contexts": set()})

    for case in cases:
        all_text = " ".join(case.preconditions + case.actions + case.expected)
        for pattern in SCREEN_PATTERNS:
            for match in re.finditer(pattern, all_text, re.IGNORECASE):
                screen_name = match.group(1).strip().rstrip(".,;:")
                screen_name = re.sub(r"\s+", " ", screen_name)
                if len(screen_name) > 3 and len(screen_name) < 60:
                    key = screen_name.lower()
                    screens[key]["mentions"] += 1
                    screens[key]["name"] = screen_name
                    screens[key]["contexts"].add(case.id)

    return dict(screens)


def extract_navigation_paths(cases):
    """Extract navigation sequences from preconditions and actions."""
    paths = []

    for case in cases:
        steps = []
        for line in case.preconditions:
            if re.search(r"(?:navigate|go to|is on|open|launch)", line, re.IGNORECASE):
                steps.append(("precondition", line))
        for line in case.actions:
            if re.search(r"(?:navigate|go to|tap|open|launch|switch)", line, re.IGNORECASE):
                steps.append(("action", line))
        if steps:
            paths.append({
                "case_id": case.id,
                "steps": steps,
            })

    return paths


def extract_elements(cases):
    """Extract UI elements mentioned in actions and expected results."""
    elements = defaultdict(lambda: {"mentions": 0, "types": set(), "contexts": set()})

    for case in cases:
        for line in case.actions + case.expected:
            # Extract quoted strings (button labels, element names)
            for match in re.finditer(r'"([^"]+)"', line):
                name = match.group(1)
                if len(name) > 1 and len(name) < 80:
                    elements[name]["mentions"] += 1
                    elements[name]["contexts"].add(case.id)

            # Extract element types
            for match in re.finditer(
                r"(?:the |a )?([\w\s/-]+?)\s+(button|icon|toggle|tab|link|field|selector|bar|menu|item|sheet|dialog|prompt|screen|view|carousel|shelf)",
                line,
                re.IGNORECASE,
            ):
                elem_name = match.group(1).strip()
                elem_type = match.group(2).lower()
                if len(elem_name) > 1 and len(elem_name) < 60:
                    key = f"{elem_name} ({elem_type})"
                    elements[key]["mentions"] += 1
                    elements[key]["types"].add(elem_type)
                    elements[key]["contexts"].add(case.id)

    return dict(elements)


def extract_apis(cases):
    """Extract API endpoints from test cases."""
    apis = []
    seen = set()

    for case in cases:
        for line in case.api_lines:
            if line.strip().upper() == "N/A":
                continue
            match = API_PATTERN.search(line)
            if match:
                method = match.group(1)
                path = match.group(2)
                key = f"{method} {path}"
                if key not in seen:
                    seen.add(key)
                    # Extract description (text after " - " separator following the URL)
                    rest_after_url = line[match.end():]
                    desc_match = re.search(r"\s+[-–—]\s+(.+)$", rest_after_url)
                    desc = desc_match.group(1).strip() if desc_match else ""
                    apis.append({
                        "method": method,
                        "path": path,
                        "description": desc,
                        "case_ids": [case.id],
                    })
                else:
                    # Add case_id to existing
                    for api in apis:
                        if f"{api['method']} {api['path']}" == key:
                            api["case_ids"].append(case.id)
                            break

    return apis


def extract_feature_flags(cases):
    """Extract feature flags mentioned in test cases."""
    flags = defaultdict(lambda: {"contexts": set(), "values": set()})

    for case in cases:
        all_text = " ".join(case.preconditions + case.actions + case.expected + case.api_lines)
        for match in FEATURE_FLAG_PATTERN.finditer(all_text):
            flag = match.group(1).strip().rstrip(".,;:")
            if "." in flag and len(flag) > 5:
                flags[flag]["contexts"].add(case.id)

        # Also find flag patterns like app.android.payments.mobilePay
        for match in re.finditer(r"(app\.\w+\.\w+(?:\.\w+)*)", all_text):
            flag = match.group(1)
            flags[flag]["contexts"].add(case.id)

    return dict(flags)


def extract_platform_notes(cases):
    """Extract platform-specific behaviors."""
    notes = {"ios": [], "android": [], "both": []}

    for case in cases:
        all_text = case.raw_text
        is_ios = bool(PLATFORM_PATTERNS["ios"].search(all_text))
        is_android = bool(PLATFORM_PATTERNS["android"].search(all_text))

        if is_ios and not is_android:
            notes["ios"].append({
                "case_id": case.id,
                "title": case.title,
                "text": all_text.strip(),
            })
        elif is_android and not is_ios:
            notes["android"].append({
                "case_id": case.id,
                "title": case.title,
                "text": all_text.strip(),
            })
        elif is_ios and is_android:
            notes["both"].append({
                "case_id": case.id,
                "title": case.title,
                "text": all_text.strip(),
            })

    return notes


def extract_behaviors(cases):
    """Extract key behaviors: normal flows, error states, edge cases."""
    behaviors = {"normal": [], "error": [], "edge_case": []}

    for case in cases:
        expected_text = " ".join(case.expected).lower()
        precond_text = " ".join(case.preconditions).lower()

        # Classify by content
        if any(kw in expected_text for kw in ["error", "fail", "crash", "not available", "cannot"]):
            category = "error"
        elif any(kw in precond_text for kw in ["no network", "timeout", "empty", "not logged", "disabled", "denied", "not yet"]):
            category = "edge_case"
        elif case.priority in ("P0", "P1"):
            category = "normal"
        else:
            category = "edge_case"

        behaviors[category].append({
            "case_id": case.id,
            "title": case.title,
            "priority": case.priority,
            "preconditions_summary": "; ".join(case.preconditions[:3]),
            "expected_summary": "; ".join(case.expected[:3]),
        })

    return behaviors


# ----- Markdown Generators -----

def generate_feature_markdown(feature_name, config, all_cases, all_extracted):
    """Generate a feature knowledge file."""
    screens = all_extracted["screens"]
    nav_paths = all_extracted["nav_paths"]
    elements = all_extracted["elements"]
    apis = all_extracted["apis"]
    flags = all_extracted["feature_flags"]
    platform = all_extracted["platform_notes"]
    behaviors = all_extracted["behaviors"]
    total_cases = len(all_cases)

    lines = []
    lines.append(f"# {feature_name}")
    lines.append("")
    lines.append("<!-- AUTO-EXTRACTED — Do not edit above this line manually -->")
    lines.append(f"<!-- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Source: {total_cases} test cases -->")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    case_titles = [c.title for c in all_cases[:5]]
    lines.append(f"Feature area covering {total_cases} test cases. Key areas:")
    for t in case_titles:
        lines.append(f"- {t}")
    if total_cases > 5:
        lines.append(f"- ... and {total_cases - 5} more")
    lines.append("")

    # Navigation
    lines.append("## Navigation")
    lines.append("")
    if nav_paths:
        seen_paths = set()
        for path in nav_paths[:10]:
            path_str = " → ".join(s[1] for s in path["steps"])
            if path_str not in seen_paths:
                seen_paths.add(path_str)
                lines.append(f"- **{path['case_id']}**: {path_str}")
        lines.append("")
    else:
        lines.append("No explicit navigation paths found in test cases.")
        lines.append("")

    # UI Elements
    lines.append("## UI Elements")
    lines.append("")
    if elements:
        lines.append("| Element | Mentions | Referenced In |")
        lines.append("|---------|----------|---------------|")
        sorted_elements = sorted(elements.items(), key=lambda x: x[1]["mentions"], reverse=True)
        for name, info in sorted_elements[:25]:
            refs = ", ".join(sorted(info["contexts"])[:5])
            if len(info["contexts"]) > 5:
                refs += f" +{len(info['contexts'])-5}"
            lines.append(f"| {name} | {info['mentions']} | {refs} |")
        lines.append("")
    else:
        lines.append("No UI elements extracted.")
        lines.append("")

    # Behaviors
    lines.append("## Behaviors")
    lines.append("")
    if behaviors["normal"]:
        lines.append("### Normal Flow (P0/P1)")
        for b in behaviors["normal"][:10]:
            prio = f" [{b['priority']}]" if b["priority"] else ""
            lines.append(f"- **{b['case_id']}**{prio}: {b['title']}")
            if b["expected_summary"]:
                lines.append(f"  - Expected: {b['expected_summary'][:150]}")
        lines.append("")

    if behaviors["edge_case"]:
        lines.append("### Edge Cases")
        for b in behaviors["edge_case"][:10]:
            prio = f" [{b['priority']}]" if b["priority"] else ""
            lines.append(f"- **{b['case_id']}**{prio}: {b['title']}")
            if b["preconditions_summary"]:
                lines.append(f"  - When: {b['preconditions_summary'][:150]}")
        lines.append("")

    if behaviors["error"]:
        lines.append("### Error States")
        for b in behaviors["error"][:10]:
            lines.append(f"- **{b['case_id']}**: {b['title']}")
            if b["expected_summary"]:
                lines.append(f"  - Expected: {b['expected_summary'][:150]}")
        lines.append("")

    # API Dependencies
    lines.append("## API Dependencies")
    lines.append("")
    if apis:
        lines.append("| Method | Endpoint | Description | Used In |")
        lines.append("|--------|----------|-------------|---------|")
        for api in apis:
            refs = ", ".join(api["case_ids"][:5])
            if len(api["case_ids"]) > 5:
                refs += f" +{len(api['case_ids'])-5}"
            lines.append(f"| {api['method']} | `{api['path']}` | {api['description'][:80]} | {refs} |")
        lines.append("")
    else:
        lines.append("No API endpoints documented in test cases.")
        lines.append("")

    # Feature Flags
    if flags:
        lines.append("## Feature Flags")
        lines.append("")
        for flag, info in flags.items():
            refs = ", ".join(sorted(info["contexts"])[:5])
            lines.append(f"- `{flag}` — referenced in {refs}")
        lines.append("")

    # Platform Notes
    if platform["ios"] or platform["android"]:
        lines.append("## Platform Notes")
        lines.append("")
        if platform["ios"]:
            lines.append("### iOS-Specific")
            for note in platform["ios"][:5]:
                lines.append(f"- **{note['case_id']}**: {note['title']}")
            lines.append("")
        if platform["android"]:
            lines.append("### Android-Specific")
            for note in platform["android"][:5]:
                lines.append(f"- **{note['case_id']}**: {note['title']}")
            lines.append("")

    # Source
    lines.append("## Source Test Cases")
    lines.append("")
    source_files = config.get("files", [])
    for f in source_files:
        lines.append(f"- `{config['source_dir']}/{f}`")
    lines.append(f"- Total: {total_cases} test cases")
    lines.append("")

    # Manual section
    lines.append("<!-- MANUAL — Add your own notes below this line -->")
    lines.append("")
    lines.append("## Manual Notes")
    lines.append("")
    lines.append("<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->")
    lines.append("")

    return "\n".join(lines)


def generate_screen_markdown(screen_key, screen_config, feature_contributions):
    """Generate a screen knowledge file."""
    lines = []
    lines.append(f"# {screen_config['name']} Screen")
    lines.append("")
    lines.append("<!-- AUTO-EXTRACTED -->")
    lines.append(f"<!-- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    lines.append("")

    lines.append("## Overview")
    lines.append("")
    lines.append(screen_config["description"])
    if screen_config.get("tab"):
        lines.append(f"- **Tab name**: {screen_config['tab']}")
    lines.append("")

    # Navigation to this screen
    lines.append("## How to Reach")
    lines.append("")
    if screen_config.get("tab"):
        lines.append(f"1. From any screen, tap the **{screen_config['tab']}** tab in the bottom navigation bar")
    else:
        lines.append("This screen is not directly accessible from the tab bar.")
    lines.append("")

    # Aggregate elements and features for this screen
    lines.append("## Features on This Screen")
    lines.append("")
    for feature_name, data in feature_contributions.items():
        total = data.get("case_count", 0)
        lines.append(f"- **[{feature_name}](../features/{data['output_file']})** — {total} test cases")
    lines.append("")

    # Elements aggregated from all features
    all_elements = {}
    for feature_name, data in feature_contributions.items():
        for elem_name, elem_info in data.get("elements", {}).items():
            if elem_name not in all_elements:
                all_elements[elem_name] = {"mentions": 0, "features": set()}
            all_elements[elem_name]["mentions"] += elem_info["mentions"]
            all_elements[elem_name]["features"].add(feature_name)

    if all_elements:
        lines.append("## UI Elements")
        lines.append("")
        lines.append("| Element | Mentions | Feature |")
        lines.append("|---------|----------|---------|")
        sorted_elems = sorted(all_elements.items(), key=lambda x: x[1]["mentions"], reverse=True)
        for name, info in sorted_elems[:20]:
            features = ", ".join(info["features"])
            lines.append(f"| {name} | {info['mentions']} | {features} |")
        lines.append("")

    # APIs aggregated
    all_apis = {}
    for feature_name, data in feature_contributions.items():
        for api in data.get("apis", []):
            key = f"{api['method']} {api['path']}"
            if key not in all_apis:
                all_apis[key] = api.copy()
                all_apis[key]["feature"] = feature_name
            else:
                all_apis[key]["case_ids"].extend(api["case_ids"])

    if all_apis:
        lines.append("## APIs Used")
        lines.append("")
        for key, api in all_apis.items():
            lines.append(f"- `{api['method']} {api['path']}` — {api.get('description', '')}")
        lines.append("")

    lines.append("<!-- MANUAL — Add your own notes below this line -->")
    lines.append("")
    lines.append("## Manual Notes")
    lines.append("")
    lines.append("<!-- Add accessibility IDs, element XPaths from real Appium sessions, etc. -->")
    lines.append("")

    return "\n".join(lines)


def generate_index_markdown(features_data, screens_config):
    """Generate the master index.md."""
    lines = []
    lines.append("# Rema App Knowledge Base — Index")
    lines.append("")
    lines.append("<!-- AUTO-EXTRACTED -->")
    lines.append(f"<!-- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    lines.append("")

    lines.append("## Quick Lookup")
    lines.append("")
    lines.append("### By Feature")
    lines.append("")
    lines.append("| Feature | File | Test Cases | Key Screens |")
    lines.append("|---------|------|------------|-------------|")
    for name, data in sorted(features_data.items()):
        filepath = data["output"]
        count = data["case_count"]
        screen_list = ", ".join(data.get("screens", []))
        lines.append(f"| {name} | [{filepath}]({filepath}) | {count} | {screen_list} |")
    lines.append("")

    lines.append("### By Screen")
    lines.append("")
    lines.append("| Screen | Tab | File | Related Features |")
    lines.append("|--------|-----|------|------------------|")
    for key, scr in screens_config.items():
        tab = scr.get("tab", "—")
        filepath = f"screens/{key}.md"
        features = [name for name, data in features_data.items() if key in data.get("screens", [])]
        features_str = ", ".join(features) if features else "—"
        lines.append(f"| {scr['name']} | {tab} | [{filepath}]({filepath}) | {features_str} |")
    lines.append("")

    lines.append("### Keyword → Feature Mapping")
    lines.append("")
    keywords = {
        "share": "Share Shopping List",
        "del liste": "Share Shopping List",
        "avatar": "Share Shopping List",
        "invitation": "Share Shopping List",
        "QR": "Share Shopping List",
        "recipe": "Favorite Recipes",
        "favorite": "Favorite Recipes",
        "heart": "Favorite Recipes",
        "opskrift": "Favorite Recipes",
        "recommended": "Recommended Products",
        "personalization": "Recommended Products",
        "payment": "Payment Methods",
        "MobilePay": "Payment Methods",
        "Worldline": "Payment Methods",
        "checkout": "Payment Methods",
        "vigo": "Vigo",
        "picker": "Faster Picker Flow",
        "store": "GPS Store Suggestions",
        "GPS": "GPS Store Suggestions",
        "butik": "GPS Store Suggestions",
        "cookie": "Cookie Consent",
        "consent": "Cookie Consent",
        "zendesk": "Zendesk Help",
        "help button": "Zendesk Help",
        "FAQ": "FAQ Help Page",
        "help page": "FAQ Help Page",
        "meget mere": "Meget Mere",
        "settings": "Meget Mere",
        "product shelf": "Pre-Defined Products",
    }
    lines.append("| Keyword | Feature |")
    lines.append("|---------|---------|")
    for kw, feature in sorted(keywords.items()):
        lines.append(f"| {kw} | [{feature}](features/{features_data.get(feature, {}).get('output', '').split('/')[-1] if feature in features_data else ''}) |")
    lines.append("")

    return "\n".join(lines)


def generate_app_map_markdown(screens_config, features_data):
    """Generate the app navigation map."""
    lines = []
    lines.append("# Rema 1000 App — Navigation Map")
    lines.append("")
    lines.append("<!-- AUTO-EXTRACTED -->")
    lines.append(f"<!-- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    lines.append("")

    lines.append("## Tab Bar (Bottom Navigation)")
    lines.append("")
    lines.append("The Rema 1000 app has a bottom tab bar with the following tabs:")
    lines.append("")
    lines.append("| Position | Tab Name | Screen | Danish Label |")
    lines.append("|----------|----------|--------|-------------|")
    tab_screens = [(k, v) for k, v in screens_config.items() if v.get("tab")]
    for i, (key, scr) in enumerate(tab_screens, 1):
        lines.append(f"| {i} | {scr['name']} | [screens/{key}.md](screens/{key}.md) | {scr['tab']} |")
    lines.append("")

    lines.append("## Screen Flow Overview")
    lines.append("")
    lines.append("```")
    lines.append("App Launch")
    lines.append("├── Cookie Consent (first launch only)")
    lines.append("│   └── Accept → Home Screen")
    lines.append("├── Home (Hjem tab)")
    lines.append("│   ├── Offers / Promotions")
    lines.append("│   └── Store info")
    lines.append("├── Shopping List (Indkøbsliste tab)")
    lines.append("│   ├── Product search → Add to list")
    lines.append("│   ├── Recommended Products shelf")
    lines.append("│   ├── Pre-Defined Products shelf")
    lines.append("│   ├── Share Shopping List → Bottom sheet")
    lines.append("│   │   ├── Share Link")
    lines.append("│   │   ├── QR Code")
    lines.append("│   │   └── Who Has Access")
    lines.append("│   └── Checkout (Køb & Hent)")
    lines.append("│       ├── Store Selection (GPS suggestions)")
    lines.append("│       ├── Payment Method (MobilePay / Worldline)")
    lines.append("│       └── Picker Flow")
    lines.append("├── Recipes (Opskrifter tab)")
    lines.append("│   ├── Search recipes")
    lines.append("│   ├── Favorite recipes (heart icon)")
    lines.append("│   └── Recipe details → Add to list")
    lines.append("└── Meget mere (More tab)")
    lines.append("    ├── Profile / Account")
    lines.append("    ├── Settings (Indstillinger)")
    lines.append("    ├── Help (Zendesk)")
    lines.append("    ├── FAQ")
    lines.append("    └── Customer Service")
    lines.append("```")
    lines.append("")

    lines.append("## Key Entry Points by Feature")
    lines.append("")
    for name, data in sorted(features_data.items()):
        screen_list = data.get("screens", [])
        screen_names = [screens_config[s]["name"] for s in screen_list if s in screens_config]
        lines.append(f"- **{name}**: {', '.join(screen_names) if screen_names else 'Various'}")
    lines.append("")

    lines.append("<!-- MANUAL -->")
    lines.append("")
    lines.append("## Manual Notes")
    lines.append("")
    lines.append("<!-- Add notes about tricky navigation, login requirements, etc. -->")
    lines.append("")

    return "\n".join(lines)


def generate_api_catalog_markdown(all_apis_by_feature):
    """Generate the API endpoint catalog."""
    lines = []
    lines.append("# Rema App — API Catalog")
    lines.append("")
    lines.append("<!-- AUTO-EXTRACTED -->")
    lines.append(f"<!-- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    lines.append("")

    lines.append("All API endpoints discovered from test case documentation.")
    lines.append("")

    for feature_name, apis in sorted(all_apis_by_feature.items()):
        if not apis:
            continue
        lines.append(f"## {feature_name}")
        lines.append("")
        lines.append("| Method | Endpoint | Description |")
        lines.append("|--------|----------|-------------|")
        for api in apis:
            lines.append(f"| {api['method']} | `{api['path']}` | {api['description'][:100]} |")
        lines.append("")

    # Aggregate all unique endpoints
    all_unique = {}
    for feature_name, apis in all_apis_by_feature.items():
        for api in apis:
            key = f"{api['method']} {api['path']}"
            if key not in all_unique:
                all_unique[key] = {"features": set(), **api}
            all_unique[key]["features"].add(feature_name)

    lines.append("## All Endpoints (Deduplicated)")
    lines.append("")
    lines.append("| Method | Endpoint | Features |")
    lines.append("|--------|----------|----------|")
    for key in sorted(all_unique.keys()):
        api = all_unique[key]
        features = ", ".join(sorted(api["features"]))
        lines.append(f"| {api['method']} | `{api['path']}` | {features} |")
    lines.append("")

    # Feature flags section
    lines.append("## Known Feature Flags")
    lines.append("")
    lines.append("| Flag | Feature |")
    lines.append("|------|---------|")
    # Will be populated per-run
    lines.append("")

    lines.append("<!-- MANUAL -->")
    lines.append("")
    lines.append("## Manual Notes")
    lines.append("")
    lines.append("<!-- Add base URL, auth requirements, environment-specific endpoints, etc. -->")
    lines.append("")

    return "\n".join(lines)


def generate_platform_differences_markdown(all_platform_notes):
    """Generate platform differences file."""
    lines = []
    lines.append("# Rema App — Platform Differences (iOS vs Android)")
    lines.append("")
    lines.append("<!-- AUTO-EXTRACTED -->")
    lines.append(f"<!-- Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->")
    lines.append("")

    lines.append("## General Notes")
    lines.append("")
    lines.append("- iOS uses `XCUIElementType*` classes in Appium page source")
    lines.append("- Android uses `android.widget.*` and `android.view.*` classes")
    lines.append("- Element finding strategies differ:")
    lines.append("  - iOS: `accessibility id`, `//XCUIElementTypeStaticText[@name='X']`, `//*[contains(@label, 'X')]`")
    lines.append("  - Android: `accessibility id`, `//*[contains(@text, 'X')]`, `//*[contains(@content-desc, 'X')]`")
    lines.append("")

    lines.append("## iOS-Specific Test Cases")
    lines.append("")
    if all_platform_notes["ios"]:
        for feature, notes in all_platform_notes["ios"].items():
            lines.append(f"### {feature}")
            for note in notes:
                lines.append(f"- **{note['case_id']}**: {note['title']}")
            lines.append("")
    else:
        lines.append("No iOS-specific test cases found.")
        lines.append("")

    lines.append("## Android-Specific Test Cases")
    lines.append("")
    if all_platform_notes["android"]:
        for feature, notes in all_platform_notes["android"].items():
            lines.append(f"### {feature}")
            for note in notes:
                lines.append(f"- **{note['case_id']}**: {note['title']}")
            lines.append("")
    else:
        lines.append("No Android-specific test cases found.")
        lines.append("")

    lines.append("<!-- MANUAL -->")
    lines.append("")
    lines.append("## Manual Notes")
    lines.append("")
    lines.append("<!-- Add real Appium selector differences, platform-specific bugs, etc. -->")
    lines.append("")

    return "\n".join(lines)


# ----- Main Orchestration -----

def preserve_manual_sections(filepath, new_content):
    """Preserve <!-- MANUAL --> sections from existing files."""
    if not os.path.exists(filepath):
        return new_content

    with open(filepath, "r") as f:
        old_content = f.read()

    # Extract manual section from old file
    manual_match = re.search(r"(<!-- MANUAL.*?-->.*)", old_content, re.DOTALL)
    if not manual_match:
        return new_content

    old_manual = manual_match.group(1)

    # Check if manual section has been customized (not just the template)
    template_lines = ["<!-- MANUAL", "## Manual Notes", "<!-- Add"]
    old_manual_stripped = old_manual.strip()
    is_template_only = all(
        any(tl in line for tl in template_lines) or not line.strip()
        for line in old_manual_stripped.split("\n")
    )

    if is_template_only:
        return new_content

    # Replace new manual section with old customized one
    new_manual_match = re.search(r"<!-- MANUAL.*?-->.*", new_content, re.DOTALL)
    if new_manual_match:
        new_content = new_content[:new_manual_match.start()] + old_manual
    return new_content


def run_extraction(config, feature_filter=None):
    """Run the full extraction pipeline."""
    testcases_root = PROJECT_ROOT / config["testcases_root"]
    output_root = PROJECT_ROOT / config["output_root"]

    features_config = config["features"]
    screens_config = config["screens"]

    # Ensure output directories exist
    (output_root / "screens").mkdir(parents=True, exist_ok=True)
    (output_root / "features").mkdir(parents=True, exist_ok=True)

    all_apis_by_feature = {}
    all_platform_notes = {"ios": {}, "android": {}}
    all_feature_flags = {}
    features_data = {}
    screen_contributions = defaultdict(dict)

    features_to_process = features_config.items()
    if feature_filter:
        features_to_process = [(k, v) for k, v in features_config.items() if k == feature_filter]
        if not features_to_process:
            print(f"Feature '{feature_filter}' not found in config. Available: {', '.join(features_config.keys())}")
            sys.exit(1)

    total_cases = 0

    for feature_name, fconfig in features_to_process:
        print(f"  Extracting: {feature_name}...")

        # Parse all test case files for this feature
        all_cases = []
        parser_type = fconfig.get("parser", "standard")
        for fname in fconfig["files"]:
            fpath = testcases_root / fconfig["source_dir"] / fname
            if fpath.exists():
                if parser_type == "regression":
                    cases = parse_regression_test_cases(fpath)
                else:
                    cases = parse_test_cases(fpath)
                all_cases.extend(cases)
                print(f"    Parsed {len(cases)} cases from {fname} ({parser_type})")
            else:
                print(f"    WARNING: File not found: {fpath}")

        if not all_cases:
            print(f"    No test cases found for {feature_name}, skipping.")
            continue

        total_cases += len(all_cases)

        # Extract knowledge
        extracted = {
            "screens": extract_screens(all_cases),
            "nav_paths": extract_navigation_paths(all_cases),
            "elements": extract_elements(all_cases),
            "apis": extract_apis(all_cases),
            "feature_flags": extract_feature_flags(all_cases),
            "platform_notes": extract_platform_notes(all_cases),
            "behaviors": extract_behaviors(all_cases),
        }

        # Generate feature markdown
        md = generate_feature_markdown(feature_name, fconfig, all_cases, extracted)
        out_path = output_root / fconfig["output"]
        md = preserve_manual_sections(out_path, md)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"    Written: {out_path.relative_to(PROJECT_ROOT)}")

        # Collect data for index/catalog
        all_apis_by_feature[feature_name] = extracted["apis"]
        if extracted["platform_notes"]["ios"]:
            all_platform_notes["ios"][feature_name] = extracted["platform_notes"]["ios"]
        if extracted["platform_notes"]["android"]:
            all_platform_notes["android"][feature_name] = extracted["platform_notes"]["android"]
        all_feature_flags[feature_name] = extracted["feature_flags"]

        features_data[feature_name] = {
            "output": fconfig["output"],
            "case_count": len(all_cases),
            "screens": fconfig.get("screens", []),
        }

        # Contribute to screen files
        for screen_key in fconfig.get("screens", []):
            screen_contributions[screen_key][feature_name] = {
                "case_count": len(all_cases),
                "elements": extracted["elements"],
                "apis": extracted["apis"],
                "output_file": fconfig["output"].split("/")[-1],
            }

    # Generate screen files
    for screen_key, scr_config in screens_config.items():
        contributions = screen_contributions.get(screen_key, {})
        md = generate_screen_markdown(screen_key, scr_config, contributions)
        out_path = output_root / "screens" / f"{screen_key}.md"
        md = preserve_manual_sections(out_path, md)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"  Written: {out_path.relative_to(PROJECT_ROOT)}")

    # Generate aggregate files (only on full extraction)
    if not feature_filter:
        # Index
        md = generate_index_markdown(features_data, screens_config)
        out_path = output_root / "index.md"
        md = preserve_manual_sections(out_path, md)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"  Written: {out_path.relative_to(PROJECT_ROOT)}")

        # App map
        md = generate_app_map_markdown(screens_config, features_data)
        out_path = output_root / "app-map.md"
        md = preserve_manual_sections(out_path, md)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"  Written: {out_path.relative_to(PROJECT_ROOT)}")

        # API catalog
        md = generate_api_catalog_markdown(all_apis_by_feature)
        # Add feature flags
        flag_lines = []
        for feature_name, flags in all_feature_flags.items():
            for flag in flags:
                flag_lines.append(f"| `{flag}` | {feature_name} |")
        if flag_lines:
            md = md.replace(
                "| Flag | Feature |\n|------|---------|",
                "| Flag | Feature |\n|------|---------|\n" + "\n".join(flag_lines),
            )
        out_path = output_root / "api-catalog.md"
        md = preserve_manual_sections(out_path, md)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"  Written: {out_path.relative_to(PROJECT_ROOT)}")

        # Platform differences
        md = generate_platform_differences_markdown(all_platform_notes)
        out_path = output_root / "platform-differences.md"
        md = preserve_manual_sections(out_path, md)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"  Written: {out_path.relative_to(PROJECT_ROOT)}")

    print(f"\nExtraction complete. {total_cases} test cases processed across {len(features_data)} features.")


def validate_freshness(config):
    """Check if knowledge files are up to date with test case files."""
    testcases_root = PROJECT_ROOT / config["testcases_root"]
    output_root = PROJECT_ROOT / config["output_root"]

    stale = []
    missing = []

    for feature_name, fconfig in config["features"].items():
        out_path = output_root / fconfig["output"]
        if not out_path.exists():
            missing.append(feature_name)
            continue

        out_mtime = out_path.stat().st_mtime

        for fname in fconfig["files"]:
            src_path = testcases_root / fconfig["source_dir"] / fname
            if src_path.exists() and src_path.stat().st_mtime > out_mtime:
                stale.append((feature_name, fname))

    if missing:
        print("Missing knowledge files:")
        for name in missing:
            print(f"  - {name}")

    if stale:
        print("\nStale knowledge files (source newer than output):")
        for name, fname in stale:
            print(f"  - {name}: {fname}")

    if not missing and not stale:
        print("All knowledge files are up to date.")

    return not missing and not stale


def main():
    parser = argparse.ArgumentParser(description="Extract knowledge from Rema test cases")
    parser.add_argument("--feature", type=str, help="Extract only a specific feature")
    parser.add_argument("--validate", action="store_true", help="Check if knowledge files are fresh")
    args = parser.parse_args()

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    if args.validate:
        ok = validate_freshness(config)
        sys.exit(0 if ok else 1)

    print("Rema App Knowledge Extraction")
    print("=" * 40)
    run_extraction(config, feature_filter=args.feature)


if __name__ == "__main__":
    main()
