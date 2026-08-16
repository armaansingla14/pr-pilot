import math
import re
from collections import Counter

KEYWORDS = re.compile(r"\b(if|for|while|catch|try|case|when|switch|await|async|yield|throw)\b")
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS access key id-ish
    re.compile(r"-----BEGIN (?:RSA|DSA|EC) PRIVATE KEY-----"),
    re.compile(r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9\-_]{16,}['\"]"),
]

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = Counter(s)
    total = len(s)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def extract_features(diff_text: str) -> dict[str, float]:
    lines = diff_text.splitlines()
    added = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
    removed = sum(1 for line in lines if line.startswith('-') and not line.startswith('---'))
    files_changed = sum(1 for line in lines if line.startswith(('+++ b/', '--- a/')))
    code_lines = [line[1:] for line in lines if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]
    code_blob = "\n".join(code_lines)

    keyword_hits = len(KEYWORDS.findall(code_blob))
    keyword_density = keyword_hits / (len(code_lines) + 1e-6)

    # crude test ratio: lines touching `test/` paths vs total
    test_path_touches = sum(1 for line in lines if re.search(r"/test[s]?/", line))
    test_ratio = test_path_touches / (files_changed + 1e-6)

    # secrets
    secret_hits = 0
    for pat in SECRET_PATTERNS:
        secret_hits += len(pat.findall(diff_text))

    # path entropy: diverse touched paths often correlates with wider blast radius
    path_lines = [line for line in lines if line.startswith(('+++ b/', '--- a/'))]
    path_str = "|".join(path_lines)
    path_entropy = shannon_entropy(path_str)

    # magnitude proxies
    churn = added + removed
    net = added - removed

    feats = {
        "files_changed": float(files_changed),
        "lines_added": float(added),
        "lines_removed": float(removed),
        "churn": float(churn),
        "net": float(net),
        "keyword_density": float(keyword_density),
        "test_ratio": float(test_ratio),
        "secret_hits": float(secret_hits),
        "path_entropy": float(path_entropy),
    }
    return feats

def summarize_features(feats: dict[str, float]) -> list[str]:
    items = sorted(feats.items(), key=lambda kv: abs(kv[1]), reverse=True)
    return [f"{k}={v:.2f}" for k,v in items[:5]]
