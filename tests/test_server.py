from reascript_mcp.server import _tool_registry


def test_tool_registry_exposes_initial_reascript_tools() -> None:
    assert set(_tool_registry) == {"parse_rpp_project", "generate_reascript", "write_reascript_file"}
    assert _tool_registry["parse_rpp_project"]["description"]
    assert _tool_registry["generate_reascript"]["description"]
    assert _tool_registry["write_reascript_file"]["description"]
