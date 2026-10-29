from collections import Counter
from pathlib import Path
import re
from typing import Any

import pandas as pd

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<request>[^"]*)"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)'
)

BASE_COLUMNS = ["IP", "Timestamp", "Method", "Page", "Status", "Bytes"]


def parse_line(line: str) -> dict[str, Any] | None:
    """Parse one Apache/Nginx common or combined access-log record."""
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    request_parts = match.group("request").split()
    method = request_parts[0] if request_parts else "UNKNOWN"
    page = request_parts[1] if len(request_parts) > 1 else "/"
    size_text = match.group("size")
    size = int(size_text) if size_text.isdigit() else 0

    return {
        "IP": match.group("ip"),
        "Timestamp": match.group("time"),
        "Method": method,
        "Page": page,
        "Status": int(match.group("status")),
        "Bytes": size,
    }


def parse_log_text(raw_text: str) -> tuple[pd.DataFrame, dict[str, int]]:
    """Return parsed log rows and simple data-quality counts."""
    lines = [line for line in raw_text.splitlines() if line.strip()]
    records: list[dict[str, Any]] = []
    for line in lines:
        record = parse_line(line)
        if record is not None:
            records.append(record)

    df = pd.DataFrame(records, columns=BASE_COLUMNS)
    stats = {
        "nonempty_lines": len(lines),
        "parsed_lines": len(records),
        "rejected_lines": len(lines) - len(records),
    }
    if not df.empty:
        df["Status"] = pd.to_numeric(df["Status"], errors="coerce").fillna(0).astype(int)
        df["Bytes"] = pd.to_numeric(df["Bytes"], errors="coerce").fillna(0).astype(int)
    return df, stats


def dataframe_for_app(df: pd.DataFrame) -> pd.DataFrame:
    """Add consistent columns used across pages without altering raw fields."""
    result = df.copy()
    if result.empty:
        result["Status Group"] = pd.Series(dtype="object")
        result["TimestampParsed"] = pd.Series(dtype="datetime64[ns, UTC]")
        return result
    result["Status Group"] = result["Status"].apply(lambda status: f"{int(status) // 100}xx")
    # Apache timestamp example: 28/Oct/2026:10:20:30 +0530
    parsed = pd.to_datetime(
        result["Timestamp"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce", utc=True
    )
    # Fall back for logs whose timestamps differ slightly from the common format.
    missing = parsed.isna()
    if missing.any():
        parsed.loc[missing] = pd.to_datetime(result.loc[missing, "Timestamp"], errors="coerce", utc=True)
    result["TimestampParsed"] = parsed
    return result


def load_default_text(path: Path) -> str:
    """Read the repository's included sample log file."""
    if not path.exists():
        raise OSError(f"Sample log file not found at {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def map_reduce(records: list[dict[str, Any]], key: str) -> pd.DataFrame:
    """Count occurrences by key using local mapper/reducer-style logic."""
    counts: Counter[str] = Counter()
    for row in records:
        value = row.get(key, "Unknown")
        if pd.isna(value):
            value = "Unknown"
        counts[str(value)] += 1
    return pd.DataFrame(
        [{key: value, "Requests": count} for value, count in counts.most_common()],
        columns=[key, "Requests"],
    )


def clean_display_df(df: pd.DataFrame) -> pd.DataFrame:
    """Hide internal timestamp helper column from tables and CSV downloads."""
    return df.drop(columns=["TimestampParsed"], errors="ignore").copy()


def format_bytes(value: int | float) -> str:
    amount = float(value or 0)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if amount < 1024 or unit == "TB":
            return f"{amount:,.0f} {unit}" if unit == "B" else f"{amount:,.2f} {unit}"
        amount /= 1024
    return f"{amount:,.2f} TB"
