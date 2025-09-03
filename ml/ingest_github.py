"""
Ingest GitHub PR metadata and diffs.

Usage:
  export GITHUB_TOKEN=...
  python ml/ingest_github.py owner repo > ml/data/raw_prs.jsonl

Then transform JSONL → features CSV you can train on.
(You can extend this to label "risky" PRs using heuristics like:
  - PR reverted within N days
  - Issues referencing this PR number in titles
  - Files touched in src/ without corresponding tests touched in test/
)
"""
import os, sys, json, time, requests

GITHUB = "https://api.github.com"

def gh_get(url):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def list_prs(owner, repo, state="closed", per_page=50, pages=2):
    out = []
    for page in range(1, pages+1):
        url = f"{GITHUB}/repos/{owner}/{repo}/pulls?state={state}&per_page={per_page}&page={page}"
        data = gh_get(url)
        out.extend(data)
        time.sleep(0.5)
    return out

def get_diff(owner, repo, number):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3.diff"}
    url = f"{GITHUB}/repos/{owner}/{repo}/pulls/{number}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ml/ingest_github.py <owner> <repo>", file=sys.stderr)
        sys.exit(1)
    owner, repo = sys.argv[1], sys.argv[2]
    prs = list_prs(owner, repo, state="closed", per_page=50, pages=2)
    for pr in prs:
        number = pr["number"]
        try:
            diff = get_diff(owner, repo, number)
        except Exception as e:
            diff = ""
        print(json.dumps({
            "number": number,
            "title": pr.get("title"),
            "merged": pr.get("merged_at") is not None,
            "additions": pr.get("additions"),
            "deletions": pr.get("deletions"),
            "changed_files": pr.get("changed_files"),
            "diff": diff
        }))
