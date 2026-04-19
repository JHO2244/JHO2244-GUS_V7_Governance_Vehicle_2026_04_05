"""
GUS v7 — Phase 63
Historical Governance Analytics Builder (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

REQUIRED_HISTORY_KEYS = (
    "total_decisions",
    "execute_count",
    "block_count",
    "integrity_confirmed_count",
    "integrity_rejected_count",
    "governance_pass_count",
    "governance_fail_count",
)


def _validate_history_window(window: dict) -> None:
    if set(window.keys()) != set(REQUIRED_HISTORY_KEYS):
        raise ValueError("INVALID_HISTORY_WINDOW")

    for key in REQUIRED_HISTORY_KEYS:
        value = window[key]
        if not isinstance(value, int) or value < 0:
            raise ValueError("INVALID_HISTORY_WINDOW")


def _format_rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0000"
    return f"{numerator / denominator:.4f}"


def _governance_trend(first_window: dict, last_window: dict) -> str:
    first_pass = first_window["governance_pass_count"]
    last_pass = last_window["governance_pass_count"]

    if last_pass > first_pass:
        return "IMPROVING"
    if last_pass < first_pass:
        return "DECLINING"
    return "STABLE"


def _governance_pattern_summary(pass_sum: int, fail_sum: int) -> str:
    if pass_sum > fail_sum:
        return "PASS_DOMINANT"
    if fail_sum > pass_sum:
        return "FAIL_DOMINANT"
    return "BALANCED"


def _execution_pattern_summary(execute_sum: int, block_sum: int) -> str:
    if execute_sum > block_sum:
        return "EXECUTE_DOMINANT"
    if block_sum > execute_sum:
        return "BLOCK_DOMINANT"
    return "BALANCED"


def _integrity_pattern_summary(
    integrity_confirmed_sum: int,
    integrity_rejected_sum: int,
) -> str:
    if integrity_confirmed_sum > integrity_rejected_sum:
        return "INTEGRITY_CONFIRMED_DOMINANT"
    if integrity_rejected_sum > integrity_confirmed_sum:
        return "INTEGRITY_REJECTED_DOMINANT"
    return "BALANCED"


def build_historical_governance_analytics_v0_1(history_windows: list) -> dict:
    """
    Input:
        ordered non-empty list of governance metrics history windows

    Output:
        deterministic historical governance analytics dict

    Fail-closed:
        - invalid structure
        - invalid values
        - empty list
    """

    if not isinstance(history_windows, list) or len(history_windows) == 0:
        raise ValueError("INVALID_HISTORY_WINDOWS")

    for window in history_windows:
        if not isinstance(window, dict):
            raise ValueError("INVALID_HISTORY_WINDOW")
        _validate_history_window(window)

    history_window_count = len(history_windows)
    total_decisions_sum = sum(w["total_decisions"] for w in history_windows)
    governance_pass_sum = sum(w["governance_pass_count"] for w in history_windows)
    governance_fail_sum = sum(w["governance_fail_count"] for w in history_windows)
    execute_sum = sum(w["execute_count"] for w in history_windows)
    block_sum = sum(w["block_count"] for w in history_windows)
    integrity_confirmed_sum = sum(
        w["integrity_confirmed_count"] for w in history_windows
    )
    integrity_rejected_sum = sum(
        w["integrity_rejected_count"] for w in history_windows
    )

    return {
        "history_window_count": history_window_count,
        "total_decisions_sum": total_decisions_sum,
        "governance_pass_sum": governance_pass_sum,
        "governance_fail_sum": governance_fail_sum,
        "execute_sum": execute_sum,
        "block_sum": block_sum,
        "integrity_confirmed_sum": integrity_confirmed_sum,
        "integrity_rejected_sum": integrity_rejected_sum,
        "governance_pass_rate": _format_rate(
            governance_pass_sum,
            total_decisions_sum,
        ),
        "governance_fail_rate": _format_rate(
            governance_fail_sum,
            total_decisions_sum,
        ),
        "execute_rate": _format_rate(
            execute_sum,
            total_decisions_sum,
        ),
        "block_rate": _format_rate(
            block_sum,
            total_decisions_sum,
        ),
        "governance_trend": _governance_trend(
            history_windows[0],
            history_windows[-1],
        ),
        "governance_pattern_summary": _governance_pattern_summary(
            governance_pass_sum,
            governance_fail_sum,
        ),
        "execution_pattern_summary": _execution_pattern_summary(
            execute_sum,
            block_sum,
        ),
        "integrity_pattern_summary": _integrity_pattern_summary(
            integrity_confirmed_sum,
            integrity_rejected_sum,
        ),
    }
