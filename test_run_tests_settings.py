"""Test that run_tests_settings loads settings safely using importlib."""
from pathlib import Path


def test_no_exec_in_source():
    """Test that the source code does not use exec() for settings loading."""
    source_file = Path(__file__).parent / "_project_" / "run_tests_settings.py"
    with open(source_file) as f:
        content = f.read()
    
    # Check that exec is not used for loading settings
    assert 'exec("from' not in content, "Source code still uses exec() for settings loading"
    assert "importlib.import_module" in content, "Source code should use importlib.import_module"
    assert "for name in dir(settings_module):" in content, "Source should copy settings to globals"
    
    print("✓ Source code uses importlib instead of exec()")
    print("✓ Settings are copied to globals safely")
    return True


def test_importlib_usage_pattern():
    """Test that the correct importlib pattern is used."""
    source_file = Path(__file__).parent / "_project_" / "run_tests_settings.py"
    with open(source_file) as f:
        content = f.read()
    
    # Verify the safe pattern
    assert "import importlib" in content, "importlib module should be imported"
    assert "importlib.import_module" in content, "Should use importlib.import_module"
    assert "globals()[name]" in content, "Should copy to globals safely"
    
    # Make sure old pattern is gone
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        assert not line.strip().startswith('exec('), f"Found exec() call at line {i}"
    
    print("✓ Importlib pattern implemented correctly")
    return True


if __name__ == "__main__":
    test_no_exec_in_source()
    test_importlib_usage_pattern()
    print("\n✅ All tests passed! Settings loading is now safe.")
