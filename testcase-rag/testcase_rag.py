#!/usr/bin/env python3
"""
Test Case RAG System
Indexes existing test cases and retrieves relevant ones as few-shot examples.

Usage:
    python testcase_rag.py index                          # Index all test cases
    python testcase_rag.py query "share shopping list"    # Find similar test cases
    python testcase_rag.py query "login flow" --top 5     # Return top 5 matches
    python testcase_rag.py query "electricity" --project Norlys  # Filter by project
    python testcase_rag.py query "payment" --prompt       # Output for agent injection
    python testcase_rag.py stats                          # Show index statistics
"""

import argparse
import json
import logging
import os
import re
import warnings
from pathlib import Path

# Suppress noisy model loading warnings
warnings.filterwarnings("ignore", message=".*UNEXPECTED.*")
warnings.filterwarnings("ignore", message=".*BertModel LOAD REPORT.*")
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import chromadb
from chromadb.utils import embedding_functions

# Paths
SCRIPT_DIR = Path(__file__).parent
CHROMA_DIR = SCRIPT_DIR / ".chroma_db"
CONFIG_PATH = SCRIPT_DIR / "sources.json"

# Embedding model - runs locally, no API key needed
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Default sources if no config file exists
DEFAULT_SOURCES = [
    {
        "name": "Rema",
        "path": str(SCRIPT_DIR.parent / "testcases"),
        "format": "standard",
        "extensions": [".txt"],
    },
    {
        "name": "Norlys",
        "path": str(Path.home() / "Downloads" / "Norlys Testpad"),
        "format": "testpad",
        "extensions": [""],  # no extension
    },
]


def load_sources() -> list[dict]:
    """Load source directories from config file, or use defaults."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return DEFAULT_SOURCES


def save_default_config():
    """Write default config to sources.json for easy editing."""
    CONFIG_PATH.write_text(json.dumps(DEFAULT_SOURCES, indent=2))
    print(f"Config written to: {CONFIG_PATH}")


def get_collection():
    """Get or create the ChromaDB collection."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
    return client.get_or_create_collection(
        name="test_cases",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_standard_format(file_path: Path, project: str) -> list[dict]:
    """Parse standard format: ID | Title [Priority] or ID - Title.

    Handles: SHARE_LIST-01 | Title [P0], cookie_prompt-01 | Title,
    TC01 - Title, INSTALL-01 | Title, RecommendedList 01 | Title
    """
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    tc_header_pattern = re.compile(
        r"^\s*([A-Za-z_][\w-]*[\s-]?\d+)\s*[|\u2013\u2014-]\s*(.+?)(?:\s*\[(P\d)\])?\s*$"
    )

    test_cases = []
    current_tc = None
    current_lines = []
    current_id = None
    current_title = None
    current_priority = None

    for line in lines:
        match = tc_header_pattern.match(line)
        if match:
            if current_tc is not None:
                body = "\n".join(current_lines).strip()
                test_cases.append(_make_tc_dict(
                    current_id, current_title, current_priority,
                    body, file_path, project,
                ))
            current_id = match.group(1).strip()
            current_title = match.group(2).strip()
            current_priority = match.group(3)
            current_lines = []
            current_tc = True
        elif current_tc is not None:
            current_lines.append(line)

    if current_tc is not None:
        body = "\n".join(current_lines).strip()
        test_cases.append(_make_tc_dict(
            current_id, current_title, current_priority,
            body, file_path, project,
        ))

    return test_cases


def parse_testpad_format(file_path: Path, project: str) -> list[dict]:
    """Parse TestPad export format: *{blue}TEST CASE XX-YY* Title.

    Sections: PRECONDITION, STEPS, EXPECTED, NOTE ON TESTING
    Steps prefixed with --1., --2. etc.
    """
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    # Pattern: *{blue}TEST CASE 01-01* Title
    tc_header_pattern = re.compile(
        r"^\s*\*\{blue\}TEST CASE\s+(\d+-\d+)\*\s*(.+?)\s*$"
    )

    test_cases = []
    current_tc = None
    current_lines = []
    current_id = None
    current_title = None

    for line in lines:
        match = tc_header_pattern.match(line)
        if match:
            if current_tc is not None:
                body = _normalize_testpad_body("\n".join(current_lines).strip())
                test_cases.append(_make_tc_dict(
                    f"TC-{current_id}", current_title, None,
                    body, file_path, project,
                ))
            current_id = match.group(1).strip()
            current_title = match.group(2).strip()
            current_lines = []
            current_tc = True
        elif current_tc is not None:
            current_lines.append(line)

    if current_tc is not None:
        body = _normalize_testpad_body("\n".join(current_lines).strip())
        test_cases.append(_make_tc_dict(
            f"TC-{current_id}", current_title, None,
            body, file_path, project,
        ))

    return test_cases


def _normalize_testpad_body(body: str) -> str:
    """Clean up TestPad body: remove -- prefixes, normalize section headers."""
    # Remove -- prefixes from steps/preconditions
    body = re.sub(r"^(\s*)--(\d+\.)", r"\1\2", body, flags=re.MULTILINE)
    body = re.sub(r"^(\s*)--", r"\1", body, flags=re.MULTILINE)
    # Normalize section headers
    body = re.sub(r"PRECONDITION\b", "Preconditions", body)
    body = re.sub(r"STEPS\b", "Actions", body)
    body = re.sub(r"EXPECTED\b", "Expected", body)
    return body


def _make_tc_dict(tc_id, title, priority, body, file_path, project):
    """Build a standardized test case dict."""
    # Derive feature from file path
    feature = file_path.stem

    full_text = (
        f"{tc_id} | {title}"
        + (f" [{priority}]" if priority else "")
        + "\n"
        + body
    )

    return {
        "id": tc_id,
        "title": title,
        "priority": priority,
        "body": body,
        "full_text": full_text,
        "file_path": str(file_path),
        "project": project,
        "feature": feature,
    }


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def find_files(base_dir: Path, extensions: list[str]) -> list[Path]:
    """Find test case files matching given extensions."""
    files = []
    if not base_dir.exists():
        return files

    for f in sorted(base_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.name.startswith("."):
            continue
        if extensions == [""]:
            # No extension — match all non-hidden files (TestPad exports)
            files.append(f)
        else:
            if f.suffix in extensions:
                files.append(f)
    return files


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

def index_test_cases():
    """Parse all test case files from all sources and index them into ChromaDB."""
    collection = get_collection()
    sources = load_sources()

    # Clear existing data
    existing = collection.count()
    if existing > 0:
        print(f"Clearing {existing} existing entries...")
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)

    total_cases = 0
    total_files = 0

    for source in sources:
        name = source["name"]
        base_dir = Path(source["path"])
        fmt = source.get("format", "standard")
        extensions = source.get("extensions", [".txt"])

        if not base_dir.exists():
            print(f"\n[{name}] Directory not found: {base_dir}")
            continue

        files = find_files(base_dir, extensions)
        if not files:
            print(f"\n[{name}] No files found in {base_dir}")
            continue

        print(f"\n[{name}] Indexing from {base_dir}")

        parser = parse_testpad_format if fmt == "testpad" else parse_standard_format
        source_cases = 0

        for file_path in files:
            test_cases = parser(file_path, name)
            if not test_cases:
                print(f"  Skipped (no test cases parsed): {file_path.name}")
                continue

            ids = []
            documents = []
            metadatas = []

            seen_ids = {}
            for tc in test_cases:
                doc = f"{tc['title']}\n{tc['body']}"

                base_id = f"{name}__{file_path.stem}__{tc['id']}"
                seen_ids[base_id] = seen_ids.get(base_id, 0) + 1
                unique_id = (
                    base_id
                    if seen_ids[base_id] == 1
                    else f"{base_id}_{seen_ids[base_id]}"
                )

                ids.append(unique_id)
                documents.append(doc)
                metadatas.append({
                    "tc_id": tc["id"],
                    "title": tc["title"],
                    "priority": tc["priority"] or "unset",
                    "file_path": tc["file_path"],
                    "project": tc["project"],
                    "feature": tc["feature"],
                    "full_text": tc["full_text"],
                })

            collection.add(ids=ids, documents=documents, metadatas=metadatas)
            source_cases += len(test_cases)
            total_files += 1
            rel = file_path.relative_to(base_dir) if file_path.is_relative_to(base_dir) else file_path.name
            print(f"  Indexed {len(test_cases):>3} cases from {rel}")

        total_cases += source_cases
        print(f"  Subtotal: {source_cases} cases from {len(files)} files")

    print(f"\nDone! Indexed {total_cases} test cases from {total_files} files across {len(sources)} sources.")
    print(f"Database stored at: {CHROMA_DIR}")


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------

def query_test_cases(query: str, top_k: int = 3, project: str = None):
    """Query the index for similar test cases."""
    collection = get_collection()

    if collection.count() == 0:
        print("Index is empty. Run 'python testcase_rag.py index' first.")
        return

    where_filter = {"project": project} if project else None

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter,
        include=["metadatas", "distances"],
    )

    if not results["ids"][0]:
        print("No matching test cases found.")
        return

    print(f"Top {len(results['ids'][0])} test cases matching: \"{query}\"\n")
    print("=" * 80)

    for i, (doc_id, metadata, distance) in enumerate(
        zip(results["ids"][0], results["metadatas"][0], results["distances"][0])
    ):
        similarity = 1 - distance
        print(
            f"\n--- Match {i + 1} | Similarity: {similarity:.2f} | "
            f"[{metadata['project']}] {metadata['feature']} ---\n"
        )
        print(metadata["full_text"])
        print()

    print("=" * 80)


def query_for_prompt(query: str, top_k: int = 3, project: str = None) -> str:
    """Query and return formatted text ready for injection into an agent prompt."""
    collection = get_collection()

    if collection.count() == 0:
        return "ERROR: Index is empty. Run 'python testcase_rag.py index' first."

    where_filter = {"project": project} if project else None

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter,
        include=["metadatas", "distances"],
    )

    if not results["ids"][0]:
        return "No matching test cases found."

    output_lines = [
        "## Reference Test Cases (from existing test suite)\n",
        "Use these as style and format examples when generating new test cases:\n",
    ]

    for i, (doc_id, metadata, distance) in enumerate(
        zip(results["ids"][0], results["metadatas"][0], results["distances"][0])
    ):
        similarity = 1 - distance
        source = f"[{metadata['project']}] {metadata['feature']}"
        output_lines.append(
            f"### Example {i + 1} (from {source}, similarity: {similarity:.2f})"
        )
        output_lines.append("")
        output_lines.append(metadata["full_text"])
        output_lines.append("")

    return "\n".join(output_lines)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def show_stats():
    """Show statistics about the indexed test cases."""
    collection = get_collection()
    total = collection.count()

    if total == 0:
        print("Index is empty. Run 'python testcase_rag.py index' first.")
        return

    all_data = collection.get(include=["metadatas"])
    metadatas = all_data["metadatas"]

    projects = {}
    features = {}
    priorities = {}

    for m in metadatas:
        proj = m.get("project", "unknown")
        feat = m.get("feature", "unknown")
        prio = m.get("priority", "unset")

        projects[proj] = projects.get(proj, 0) + 1
        key = f"{proj}/{feat}"
        features[key] = features.get(key, 0) + 1
        priorities[prio] = priorities.get(prio, 0) + 1

    print(f"Total indexed test cases: {total}\n")

    print("By project:")
    for proj, count in sorted(projects.items()):
        print(f"  {proj}: {count}")

    print(f"\nBy feature ({len(features)} features):")
    for feat, count in sorted(features.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {feat}: {count}")

    print("\nBy priority:")
    for prio, count in sorted(priorities.items()):
        print(f"  {prio}: {count}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Test Case RAG - Index and retrieve similar test cases"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # index
    subparsers.add_parser("index", help="Index all test cases from configured sources")

    # query
    query_parser = subparsers.add_parser("query", help="Find similar test cases")
    query_parser.add_argument(
        "text", help="Feature description or keywords to search for"
    )
    query_parser.add_argument(
        "--top", type=int, default=3, help="Number of results (default: 3)"
    )
    query_parser.add_argument(
        "--project", help="Filter by project (e.g., Rema, Norlys, imCore)"
    )
    query_parser.add_argument(
        "--prompt",
        action="store_true",
        help="Output in prompt-injection format (for use with agents)",
    )

    # stats
    subparsers.add_parser("stats", help="Show index statistics")

    # config
    subparsers.add_parser(
        "config", help="Write default sources.json config for editing"
    )

    args = parser.parse_args()

    if args.command == "index":
        index_test_cases()
    elif args.command == "query":
        if args.prompt:
            print(query_for_prompt(args.text, top_k=args.top, project=args.project))
        else:
            query_test_cases(args.text, top_k=args.top, project=args.project)
    elif args.command == "stats":
        show_stats()
    elif args.command == "config":
        save_default_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
