from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PYTHON = Path("/home/eston/anaconda3/envs/global_judge/bin/python")
OUT_JSON = Path("data/analysis/release_validation_report.json")
OUT_MD = Path("data/analysis/release_validation_report.md")


@dataclass(frozen=True)
class Check:
    name: str
    command: list[str]
    expect_returncode: int = 0


def tail(text: str, limit: int = 2400) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def run_check(check: Check) -> dict[str, Any]:
    start = time.monotonic()
    result = subprocess.run(check.command, capture_output=True, text=True)
    elapsed = time.monotonic() - start
    passed = result.returncode == check.expect_returncode
    return {
        "name": check.name,
        "command": " ".join(check.command),
        "returncode": result.returncode,
        "expected_returncode": check.expect_returncode,
        "elapsed_seconds": round(elapsed, 3),
        "passed": passed,
        "stdout_tail": tail(result.stdout),
        "stderr_tail": tail(result.stderr),
    }


def pdf_pages(path: str) -> int:
    result = subprocess.run(["pdfinfo", path], check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Could not determine page count for {path}")


def page_check(path: str, expected_pages: int) -> dict[str, Any]:
    start = time.monotonic()
    try:
        pages = pdf_pages(path)
        passed = pages == expected_pages
        detail = f"{path}: {pages} pages"
        return {
            "name": f"page count: {path}",
            "command": f"pdfinfo {path}",
            "returncode": 0,
            "expected_returncode": 0,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "passed": passed,
            "stdout_tail": detail,
            "stderr_tail": "" if passed else f"Expected {expected_pages} pages",
        }
    except Exception as exc:
        return {
            "name": f"page count: {path}",
            "command": f"pdfinfo {path}",
            "returncode": 1,
            "expected_returncode": 0,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "passed": False,
            "stdout_tail": "",
            "stderr_tail": str(exc),
        }


def stale_claim_scan() -> dict[str, Any]:
    pattern = (
        r"(T[O]DO|T[B]D|F[I]XME|p[l]aceholder|0\.3706|0\.3499|0\.3403|"
        r"significant pivot dr[o]p|including a signific[a]nt|single global w[i]nner)"
    )
    check = Check(
        name="stale claim scan",
        command=[
            "rg",
            "-n",
            pattern,
            "README.md",
            "paper",
            "data/analysis/current_research_status.md",
            "src",
            "configs",
        ],
        expect_returncode=1,
    )
    return run_check(check)


def log_scan(path: str) -> dict[str, Any]:
    start = time.monotonic()
    problem_re = re.compile(r"(undefined|Undefined|Citation|Reference|Overfull|Error|Rerun)")
    allowed_substrings = ("Package: rerunfilecheck",)
    findings = []
    try:
        for lineno, line in enumerate(Path(path).read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            if not problem_re.search(line):
                continue
            if any(allowed in line for allowed in allowed_substrings):
                continue
            findings.append(f"{path}:{lineno}:{line}")
        return {
            "name": f"LaTeX hard-problem scan: {path}",
            "command": f"scan {path} for undefined/citation/reference/overfull/error/rerun",
            "returncode": 0 if not findings else 1,
            "expected_returncode": 0,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "passed": not findings,
            "stdout_tail": "\n".join(findings[-20:]),
            "stderr_tail": "",
        }
    except Exception as exc:
        return {
            "name": f"LaTeX hard-problem scan: {path}",
            "command": f"scan {path}",
            "returncode": 1,
            "expected_returncode": 0,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "passed": False,
            "stdout_tail": "",
            "stderr_tail": str(exc),
        }


def all_checks() -> list[Check]:
    py = str(PYTHON)
    return [
        Check("compile source", [py, "-m", "compileall", "src"]),
        Check("summarize protocol instability", [py, "src/summarize_protocol_instability.py"]),
        Check("extract qualitative examples", [py, "src/extract_qualitative_examples.py"]),
        Check("summarize prompt inventory", [py, "src/summarize_prompt_inventory.py"]),
        Check("summarize dataset sampling", [py, "src/summarize_dataset_sampling.py"]),
        Check("summarize calibration learning curve", [py, "src/summarize_calibration_learning_curve.py"]),
        Check("summarize score threshold diagnostic", [py, "src/summarize_score_threshold_diagnostic.py"]),
        Check("summarize run inventory", [py, "src/summarize_run_inventory.py"]),
        Check("summarize repeatability control", [py, "src/summarize_repeatability_control.py"]),
        Check("export paper tables", [py, "src/export_paper_tables.py"]),
        Check("build claim evidence matrix", [py, "src/build_claim_evidence_matrix.py"]),
        Check("build rq contribution matrix", [py, "src/build_rq_contribution_matrix.py"]),
        Check("make results brief", [py, "src/make_results_brief.py"]),
        Check("build benchmark data card", [py, "src/build_benchmark_datacard.py"]),
        Check("build paper PDFs", ["make", "-C", "paper"]),
        Check("build reproducibility manifest", [py, "src/build_reproducibility_manifest.py"]),
        Check("build submission packet", [py, "src/build_submission_packet.py"]),
        Check("build completion audit", [py, "src/build_completion_audit.py"]),
        Check("refresh reproducibility manifest", [py, "src/build_reproducibility_manifest.py"]),
        Check("validate paper claims", [py, "src/validate_paper_claims.py"]),
    ]


def write_reports(results: list[dict[str, Any]]) -> None:
    passed = all(result["passed"] for result in results)
    payload = {
        "status": "passed" if passed else "failed",
        "checks": results,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Release Validation Report",
        "",
        f"Status: **{payload['status']}**",
        "",
        "This report is generated by `src/run_release_checks.py`. It uses only cached artifacts and no API calls.",
        "",
        "| Check | Status | Seconds | Command |",
        "| --- | --- | ---: | --- |",
    ]
    for result in results:
        status = "pass" if result["passed"] else "fail"
        lines.append(
            f"| {result['name']} | {status} | {result['elapsed_seconds']:.3f} | `{result['command']}` |"
        )
    failures = [result for result in results if not result["passed"]]
    if failures:
        lines.extend(["", "## Failures", ""])
        for result in failures:
            lines.extend(
                [
                    f"### {result['name']}",
                    "",
                    "```",
                    result["stdout_tail"],
                    result["stderr_tail"],
                    "```",
                    "",
                ]
            )
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    results = [run_check(check) for check in all_checks()]
    results.extend(
        [
            page_check("paper/main.pdf", 11),
            page_check("paper/extended_abstract.pdf", 2),
            stale_claim_scan(),
            log_scan("paper/main.log"),
            log_scan("paper/extended_abstract.log"),
        ]
    )
    write_reports(results)
    final_manifest = subprocess.run(
        [str(PYTHON), "src/build_reproducibility_manifest.py"],
        capture_output=True,
        text=True,
    )
    status = "passed" if all(result["passed"] for result in results) else "failed"
    if final_manifest.returncode != 0:
        status = "failed"
    print(f"Release validation {status}.")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("Refreshed data/analysis/reproducibility_manifest.json after writing reports.")
    if final_manifest.returncode != 0:
        print(final_manifest.stdout)
        print(final_manifest.stderr)
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
