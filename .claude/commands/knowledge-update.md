Re-run the Rema app knowledge extraction to update the knowledge base from test case files.

**Arguments:** $ARGUMENTS

## What to do

1. If `$ARGUMENTS` contains a feature name (e.g., "Favorite Recipes"), run single-feature extraction:
   ```bash
   python3 knowledge/extract_knowledge.py --feature "$ARGUMENTS"
   ```

2. If `$ARGUMENTS` is empty, run full extraction:
   ```bash
   python3 knowledge/extract_knowledge.py
   ```

3. After extraction, report:
   - How many test cases were processed
   - How many features were extracted
   - Any warnings (missing files, 0 cases)

4. If `$ARGUMENTS` is "validate" or "check", run validation only:
   ```bash
   python3 knowledge/extract_knowledge.py --validate
   ```

## Notes
- Extraction preserves any `<!-- MANUAL -->` sections you've added to knowledge files
- Re-extraction overwrites `<!-- AUTO-EXTRACTED -->` sections with fresh data
- Run this after adding or modifying test case files in `testcases/Rema/`
