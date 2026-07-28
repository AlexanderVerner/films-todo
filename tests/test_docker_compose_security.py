"""Test to verify Django port is not exposed to the host."""
import re
import os


def test_django_port_not_exposed_on_host():
    """Verify that port 8000 is not published to the host in docker-compose.yml"""
    compose_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "docker-compose.yml"
    )
    
    with open(compose_path, "r") as f:
        content = f.read()
    
    # Verify that 8000:8000 port mapping does NOT exist in the file
    assert not re.search(r'8000\s*:\s*8000', content), (
        "Django port 8000 should not be exposed to the host with 8000:8000 mapping. "
        "This bypasses nginx and TLS protection."
    )
    
    # Verify that 'expose:' section is used for web service
    web_section = re.search(
        r'web:\s*\n(.*?)\n\s{2}\w+:',
        content,
        re.DOTALL
    )
    
    assert web_section is not None, "Could not find web service in docker-compose.yml"
    
    web_config = web_section.group(1)
    
    # Check that expose is configured
    assert re.search(r'expose\s*:\s*\n\s*-\s*8000', web_config), (
        "Django service should use 'expose' to make port 8000 accessible "
        "only within the Docker network, not to the host"
    )


if __name__ == "__main__":
    test_django_port_not_exposed_on_host()
    print("✅ Test passed: Django port is not exposed to host")
