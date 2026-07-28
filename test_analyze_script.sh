#!/bin/bash
# Test script for analyze-project-structure.sh

set -e

SCRIPT="./.cursor/scripts/bash/analyze-project-structure.sh"

echo "🧪 Testing analyze-project-structure.sh"
echo ""

# Make script executable
chmod +x "$SCRIPT"

# Run the script and capture output
OUTPUT=$("$SCRIPT")

echo "Script output:"
echo "$OUTPUT"
echo ""

# Verify key sections exist
if echo "$OUTPUT" | grep -q "=== Файлы ==="; then
    echo "✅ Files section found"
else
    echo "❌ Files section missing"
    exit 1
fi

if echo "$OUTPUT" | grep -q "=== Строки кода ==="; then
    echo "✅ Lines of code section found"
else
    echo "❌ Lines of code section missing"
    exit 1
fi

# Verify Python files are counted
if echo "$OUTPUT" | grep -q "Python"; then
    echo "✅ Python files counted"
else
    echo "❌ Python files not counted"
    exit 1
fi

# Verify line counts are numbers (not empty)
if echo "$OUTPUT" | grep -E "Python.*[0-9]+ строк" > /dev/null; then
    echo "✅ Python line count is numeric"
    PYTHON_LINES=$(echo "$OUTPUT" | grep "Python" | grep -oE "[0-9]+" | head -1)
    echo "   Found $PYTHON_LINES Python lines"
else
    echo "❌ Python line count is empty or invalid"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
