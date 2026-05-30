#!/usr/bin/env bash
# Invoke Gemini for read-only analysis and create collaboration artifact

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLAB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ARTIFACTS_DIR="$COLLAB_DIR/artifacts"

# Usage
usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Invoke Gemini CLI for read-only analysis and create collaboration artifact.

OPTIONS:
    -t, --task-id TASK_ID       Task ID (required)
    -p, --prompt PROMPT         Analysis prompt (required)
    -f, --files FILES           Comma-separated file paths to analyze
    -d, --dry-run               Dry-run mode (skip actual Gemini call)
    -h, --help                  Show this help

EXAMPLES:
    $0 -t TASK-20260530-05 -p "Analyze error patterns" -f "logs/app.log"
    $0 -t TASK-20260530-05 -p "Review architecture" --dry-run

NOTES:
    - Gemini operates in read-only mode (--approval-mode plan)
    - Output artifact: $ARTIFACTS_DIR/YYYYMMDD-HHMM-gemini-*.md
    - Event logged to events.jsonl
    - API failures are handled gracefully
EOF
    exit 1
}

# Parse arguments
TASK_ID=""
PROMPT=""
FILES=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--task-id)
            TASK_ID="$2"
            shift 2
            ;;
        -p|--prompt)
            PROMPT="$2"
            shift 2
            ;;
        -f|--files)
            FILES="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate required arguments
if [[ -z "$TASK_ID" ]]; then
    echo "Error: --task-id is required"
    usage
fi

if [[ -z "$PROMPT" ]]; then
    echo "Error: --prompt is required"
    usage
fi

# Check Gemini CLI availability
if ! command -v gemini &> /dev/null; then
    echo "❌ Gemini CLI not found. Install: npm install -g @google/gemini-cli"
    exit 1
fi

# Generate artifact filename
TIMESTAMP=$(date +"%Y%m%d-%H%M")
SLUG=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | cut -c1-30)
ARTIFACT_FILE="$ARTIFACTS_DIR/${TIMESTAMP}-gemini-${SLUG}.md"

# Build Gemini command
GEMINI_CMD="gemini -p"

# Construct full prompt
FULL_PROMPT="$PROMPT"
if [[ -n "$FILES" ]]; then
    FULL_PROMPT="$FULL_PROMPT

Files to analyze: $FILES

Please provide your analysis in markdown format."
fi

# Dry-run mode
if [[ "$DRY_RUN" == true ]]; then
    echo "🔍 Dry-run mode - skipping actual Gemini call"
    echo ""
    echo "Would execute:"
    echo "  gemini -p \"$FULL_PROMPT\" --approval-mode plan --output-format text"
    echo ""
    echo "Would create artifact: $ARTIFACT_FILE"
    echo ""

    # Create mock artifact
    cat > "$ARTIFACT_FILE" <<EOF
# Gemini Analysis (Dry-Run)

**Task:** $TASK_ID
**Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Mode:** Dry-run (no actual Gemini call)

## Prompt

$PROMPT

## Files

$FILES

## Analysis

[Dry-run mode - no actual analysis performed]

This artifact was created in dry-run mode to test the workflow without calling the Gemini API.
EOF

    echo "✓ Created dry-run artifact: $ARTIFACT_FILE"

    # Log event (dry-run)
    python3 "$SCRIPT_DIR/../../../.claude/skills/claude-codex-collab/scripts/collab_event.py" \
        analysis_requested gemini "$TASK_ID" \
        "Gemini analysis requested (dry-run): $PROMPT" \
        "[\"$ARTIFACT_FILE\"]"

    exit 0
fi

# Execute Gemini CLI
echo "🤖 Invoking Gemini CLI..."
echo "Task: $TASK_ID"
echo "Prompt: $PROMPT"
if [[ -n "$FILES" ]]; then
    echo "Files: $FILES"
fi
echo ""

# Run Gemini with error handling
GEMINI_OUTPUT=""
GEMINI_EXIT_CODE=0

set +e
GEMINI_OUTPUT=$(echo "$FULL_PROMPT" | gemini -p "$(cat)" --approval-mode plan --output-format text 2>&1)
GEMINI_EXIT_CODE=$?
set -e

# Handle API failure
if [[ $GEMINI_EXIT_CODE -ne 0 ]]; then
    echo "❌ Gemini API call failed (exit code: $GEMINI_EXIT_CODE)"
    echo ""
    echo "Error output:"
    echo "$GEMINI_OUTPUT"
    echo ""

    # Create failure artifact
    cat > "$ARTIFACT_FILE" <<EOF
# Gemini Analysis (Failed)

**Task:** $TASK_ID
**Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Status:** API call failed

## Prompt

$PROMPT

## Files

$FILES

## Error

\`\`\`
$GEMINI_OUTPUT
\`\`\`

## Mitigation

The Gemini API returned an error. Possible causes:
- API service unavailable (500 error)
- Authentication issues
- Rate limiting
- Network connectivity

**Recommendation:** Retry later or use dry-run mode to test workflow without API calls.
EOF

    echo "✓ Created failure artifact: $ARTIFACT_FILE"

    # Log failure event
    python3 "$SCRIPT_DIR/../../../.claude/skills/claude-codex-collab/scripts/collab_event.py" \
        analysis_failed gemini "$TASK_ID" \
        "Gemini analysis failed: API error (exit code $GEMINI_EXIT_CODE)" \
        "[\"$ARTIFACT_FILE\"]"

    exit 1
fi

# Success - create artifact
cat > "$ARTIFACT_FILE" <<EOF
# Gemini Analysis

**Task:** $TASK_ID
**Timestamp:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Agent:** Gemini
**Mode:** Read-only (--approval-mode plan)

## Prompt

$PROMPT

## Files

$FILES

## Analysis

$GEMINI_OUTPUT
EOF

echo "✓ Created artifact: $ARTIFACT_FILE"

# Log success event
python3 "$SCRIPT_DIR/../../../.claude/skills/claude-codex-collab/scripts/collab_event.py" \
    artifact_created gemini "$TASK_ID" \
    "Gemini analysis completed: $PROMPT" \
    "[\"$ARTIFACT_FILE\"]"

echo "✓ Event logged to events.jsonl"
echo ""
echo "Done. Artifact: $ARTIFACT_FILE"
