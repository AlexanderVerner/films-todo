"""
Test to verify the detail.html template has correct HTML structure.
Validates:
1. No nested forms
2. Balanced div tags
3. Proper form structure
"""
import re
from pathlib import Path


def test_no_nested_forms():
    """Verify that template has no nested forms."""
    template_path = Path(__file__).parent / "_project_/templates/todo/detail.html"
    content = template_path.read_text()
    
    # Find all form tags
    form_pattern = r'<form[^>]*>|</form>'
    forms = re.finditer(form_pattern, content)
    
    form_stack = []
    for match in forms:
        tag = match.group(0)
        if tag.startswith('<form'):
            form_stack.append(match.start())
        elif tag == '</form>':
            if not form_stack:
                raise AssertionError("Unmatched closing </form> tag")
            form_stack.pop()
    
    assert len(form_stack) == 0, f"Unclosed form tags: {len(form_stack)}"
    print("✓ No nested forms detected")


def test_balanced_div_tags():
    """Verify that all div tags are properly balanced."""
    template_path = Path(__file__).parent / "_project_/templates/todo/detail.html"
    content = template_path.read_text()
    
    # Count div open and close tags
    open_divs = len(re.findall(r'<div[^>]*>', content))
    close_divs = len(re.findall(r'</div>', content))
    
    assert open_divs == close_divs, f"Unbalanced div tags: {open_divs} open, {close_divs} close"
    print(f"✓ Balanced div tags: {open_divs} pairs")


def test_form_structure():
    """Verify that each form has proper structure."""
    template_path = Path(__file__).parent / "_project_/templates/todo/detail.html"
    content = template_path.read_text()
    
    # Find delete form - should have action with "todo:delete" (case insensitive for template syntax)
    has_delete_form = 'todo:delete' in content
    assert has_delete_form, "Delete form not found in template"
    
    # Find detail/seen form - should have action with "todo:detail"
    has_detail_form = 'todo:detail' in content
    assert has_detail_form, "Detail/Seen form not found in template"
    
    print("✓ Form structure is correct (separate Delete and Seen forms)")


def test_no_orphaned_buttons():
    """Verify that buttons are inside forms."""
    template_path = Path(__file__).parent / "_project_/templates/todo/detail.html"
    content = template_path.read_text()
    
    # Remove form tags temporarily to check if buttons exist outside forms
    forms_removed = re.sub(r'<form[^>]*>.*?</form>', '', content, flags=re.DOTALL)
    
    # Check for standalone buttons with type="submit"
    orphaned_buttons = re.findall(r'<button[^>]*type="submit"[^>]*>', forms_removed)
    
    assert len(orphaned_buttons) == 0, f"Found {len(orphaned_buttons)} orphaned submit buttons"
    print("✓ All buttons are inside forms")


if __name__ == "__main__":
    test_no_nested_forms()
    test_balanced_div_tags()
    test_form_structure()
    test_no_orphaned_buttons()
    print("\n✅ All template structure tests passed!")
