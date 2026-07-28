#!/bin/bash
# Анализ структуры проекта - 0 токенов

echo "🔍 Анализ структуры проекта"
echo "Дата: $(date '+%Y-%m-%d %H:%M')"
echo ""

count_lines() {
    local pattern=$1 name=$2
    local count=0
    
    # Use find with awk to count lines avoiding ARG_MAX issues
    # Each file is counted separately to avoid xargs sysconf errors
    count=$(find . -name "$pattern" \
        -not -path "*/node_modules/*" -not -path "*/vendor/*" \
        -not -path "*/dist/*" -not -path "*/build/*" \
        -not -path "*/.git/*" -not -path "*/target/*" \
        -type f 2>/dev/null | awk '{
            while ((getline line < $0) > 0) { c++ }
            close($0)
        } END { print c }')
    
    # Fallback: if awk method fails, use wc with find directly (ignore errors)
    if [ -z "$count" ] || [ "$count" = "0" ] || ! [[ "$count" =~ ^[0-9]+$ ]]; then
        count=$(find . -name "$pattern" \
            -not -path "*/node_modules/*" -not -path "*/vendor/*" \
            -not -path "*/dist/*" -not -path "*/build/*" \
            -not -path "*/.git/*" -not -path "*/target/*" \
            -type f 2>/dev/null -exec sh -c 'wc -l < "$1" 2>/dev/null || echo 0' _ {} \; | \
            awk '{s+=$1} END {print s}')
    fi
    
    [ -n "$count" ] && [ "$count" != "0" ] && echo "  $name: $count строк"
}

count_files() {
    local pattern=$1 name=$2
    local count=$(find . -name "$pattern" \
        -not -path "*/node_modules/*" -not -path "*/vendor/*" \
        -not -path "*/dist/*" -not -path "*/build/*" \
        -not -path "*/.git/*" -not -path "*/target/*" \
        2>/dev/null | wc -l)
    [ "$count" != "0" ] && echo "  $name: $count файлов"
}

echo "=== Файлы ==="
count_files "*.go" "Go"
count_files "*.ts" "TypeScript"
count_files "*.js" "JavaScript"
count_files "*.py" "Python"
count_files "*.java" "Java"
count_files "*.rs" "Rust"

echo ""
echo "=== Строки кода ==="
count_lines "*.go" "Go"
count_lines "*.ts" "TypeScript"
count_lines "*.js" "JavaScript"
count_lines "*.py" "Python"

echo ""
echo "=== Тесты ==="
test_count=$(find . \( -name "*_test.go" -o -name "*.test.ts" -o -name "*.test.js" \
    -o -name "*.spec.ts" -o -name "*.spec.js" -o -name "test_*.py" \) \
    -not -path "*/node_modules/*" -not -path "*/vendor/*" 2>/dev/null | wc -l)
if [ "$test_count" != "0" ]; then
    echo "  ✅ Тестовых файлов: $test_count"
    find . \( -name "*_test.go" -o -name "*.test.ts" \) \
        -not -path "*/node_modules/*" -not -path "*/vendor/*" 2>/dev/null
else
    echo "  ❌ Тестов не найдено"
fi

echo ""
echo "=== Крупные файлы Go (>150 строк) ==="
find . -name "*.go" -not -path "*/vendor/*" -type f 2>/dev/null -exec sh -c '
    lines=$(wc -l < "$1" 2>/dev/null || echo 0)
    if [ "$lines" -gt 150 ]; then
        echo "  ⚠️  $lines строк: $1"
    fi
' _ {} \; | sort -rn

echo ""
echo "=== TODO / Tech debt ==="
todo_count=$(grep -r "TODO\|FIXME\|HACK\|XXX" . \
    --include="*.go" --include="*.ts" --include="*.js" \
    --exclude-dir=vendor --exclude-dir=.git 2>/dev/null | wc -l)
echo "  Найдено: $todo_count"
grep -rn "TODO\|FIXME\|HACK" . \
    --include="*.go" --exclude-dir=vendor --exclude-dir=.git 2>/dev/null | head -10

echo ""
echo "✅ Готово"
