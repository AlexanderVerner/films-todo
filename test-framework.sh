#!/bin/bash
# Тестирование установки framework

echo "🧪 Тестирование Cursor Optimization Framework"
echo ""

PASS=0; FAIL=0

check_file() {
    local desc=$1 filepath=$2
    if [ -f "$filepath" ]; then
        echo "  ✅ $desc"; ((PASS++))
    else
        echo "  ❌ $desc"; ((FAIL++))
    fi
}

check_dir() {
    local desc=$1 dirpath=$2
    if [ -d "$dirpath" ]; then
        echo "  ✅ $desc"; ((PASS++))
    else
        echo "  ❌ $desc"; ((FAIL++))
    fi
}

check_executable() {
    local desc=$1 filepath=$2
    if [ -x "$filepath" ]; then
        echo "  ✅ $desc"; ((PASS++))
    else
        echo "  ❌ $desc"; ((FAIL++))
    fi
}

check_grep() {
    local desc=$1 pattern=$2 filepath=$3
    if grep -q "$pattern" "$filepath" 2>/dev/null; then
        echo "  ✅ $desc"; ((PASS++))
    else
        echo "  ❌ $desc"; ((FAIL++))
    fi
}

check_command() {
    local desc=$1 cmd=$2
    if bash -c "$cmd" > /dev/null 2>&1; then
        echo "  ✅ $desc"; ((PASS++))
    else
        echo "  ❌ $desc"; ((FAIL++))
    fi
}

echo "=== Структура файлов ==="
check_file ".cursorignore"                        ".cursorignore"
check_file ".cursor/rules/optimization.mdc"       ".cursor/rules/optimization.mdc"
check_file ".cursor/context/base.md"              ".cursor/context/base.md"
check_file ".cursor/snapshots/changes.md"         ".cursor/snapshots/changes.md"
check_file ".cursor/plans/optimization-plan.md"   ".cursor/plans/optimization-plan.md"
check_dir ".cursor/plans/tasks/"                 ".cursor/plans/tasks"
check_dir ".cursor/plans/done/"                  ".cursor/plans/done"
check_dir ".cursor/scripts/bash/"               ".cursor/scripts/bash"
check_dir ".cursor/scripts/prompts/"            ".cursor/scripts/prompts"

echo ""
echo "=== Промпты ==="
for name in \
    01-analyze-project \
    02-create-plan \
    03-fix-simple-bug \
    04-create-architecture \
    05-refactor \
    05b-refactor-complex \
    06-write-unit-tests \
    07-add-godoc \
    09-update-readme \
    run-next-task; do
    check_file "$name.txt" ".cursor/scripts/prompts/${name}.txt"
done

echo ""
echo "=== Bash скрипты ==="
check_file "analyze-project-structure.sh" ".cursor/scripts/bash/analyze-project-structure.sh"
check_file "find-todos.sh"                ".cursor/scripts/bash/find-todos.sh"
check_file "snapshot-state.sh"           ".cursor/scripts/bash/snapshot-state.sh"
check_file "check-coverage.sh"           ".cursor/scripts/bash/check-coverage.sh"
check_executable "Скрипты исполняемы"          ".cursor/scripts/bash/analyze-project-structure.sh"

echo ""
echo "=== .cursorignore ==="
check_grep "node_modules/"   "node_modules" ".cursorignore"
check_grep "vendor/"         "vendor/" ".cursorignore"
check_grep ".git/"           ".git/" ".cursorignore"
check_grep ".cursor/plans/"  ".cursor/plans/" ".cursorignore"

echo ""
echo "=== Функциональный тест ==="
check_command "analyze-project-structure.sh запускается" "bash .cursor/scripts/bash/analyze-project-structure.sh"
check_command "find-todos.sh запускается"               "bash .cursor/scripts/bash/find-todos.sh"

echo ""
echo "==============================="
echo "Результат: ✅ $PASS | ❌ $FAIL"
echo ""
if [ "$FAIL" -gt 0 ]; then
    echo "⚠️  Запусти setup.sh заново или проверь ошибки выше."
    exit 1
else
    echo "🎉 Framework готов!"
    echo ""
    echo "Следующий шаг:"
    echo "  1. Отредактируй .cursor/context/base.md"
    echo "  2. В Cursor: промпт 01-analyze-project.txt (Opus)"
fi
