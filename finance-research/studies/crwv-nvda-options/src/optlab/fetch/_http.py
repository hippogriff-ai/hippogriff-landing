from __future__ import annotations

import requests

UA = "finance-research/0.1 (research; contact via repository)"


class NetworkBlocked(RuntimeError):
    """Raised when the host is unreachable (typically a sandbox network policy)."""


def get(url: str, **kw) -> requests.Response:
    kw.setdefault("timeout", 30)
    headers = {"User-Agent": UA, **kw.pop("headers", {})}
    try:
        r = requests.get(url, headers=headers, **kw)
    except requests.exceptions.RequestException as e:  # DNS failure, proxy 403, etc.
        raise NetworkBlocked(f"could not reach {url}: {e}. If you are in a sandbox, allow the host "
                             "in the environment's network settings and rerun.") from e
    r.raise_for_status()
    return r
