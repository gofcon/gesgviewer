#!/usr/bin/env python3
"""
Oracle migration SQL → SQLite 데이터 이관 스크립트

Usage:
    python db/migrate_oracle.py [SQL_FILE]

기본 SQL 파일은 MIGRATION_SQL 환경변수 또는 스크립트 상수로 지정.
"""
import re
import sqlite3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine
from sqlmodel import SQLModel
import db.models  # noqa: F401 — 모든 테이블 등록
from config.settings import DB_PATH

# ── 기본 SQL 파일 경로 ────────────────────────────────────────
DEFAULT_SQL = "/home/javanance/github/obsidian/githubvault/90.Temp/oracle_migration.sql"
MIGRATION_SQL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MIGRATION_SQL", DEFAULT_SQL)

BATCH_SIZE = 2000

# ── Oracle 테이블 → SQLite 컬럼 매핑 (Oracle DDL 컬럼 순서) ──
TABLE_MAP: dict[str, list[str]] = {
    "E_CO_ESG_META": [
        "group_id", "param_key", "param_value", "param_name", "param_desc",
        "use_yn", "last_modified_by", "last_update_date",
    ],
    "E_CO_JOB_LIST": [
        "job_id", "job_nm", "use_yn", "last_modified_by", "last_update_date",
    ],
    "E_CO_JOB_INFO": [
        "job_id", "job_nm", "base_yymm", "calc_date", "calc_start",
        "calc_end", "calc_elps", "calc_scd", "last_modified_by", "last_update_date",
    ],
    "E_IR_CURVE": [
        "ir_curve_id", "ir_curve_nm", "cur_cd", "appl_meth_dv", "crd_grd_cd",
        "intp_meth_cd", "use_yn", "last_modified_by", "last_update_date",
    ],
    "E_IR_CURVE_SPOT": [
        "base_date", "ir_curve_id", "mat_cd", "spot_rate",
        "last_modified_by", "last_update_date",
    ],
    "E_IR_CURVE_YTM_USR": [
        "base_date", "ir_curve_id", "mat_cd", "ytm",
        "last_modified_by", "last_update_date",
    ],
    "E_IR_DCNT_RATE": [
        "base_yymm", "appl_biz_dv", "ir_curve_id", "ir_curve_sce_no", "mat_cd",
        "spot_rate", "fwd_rate", "adj_spot_rate", "adj_fwd_rate",
        "last_modified_by", "last_update_date",
    ],
    "E_IR_DCNT_RATE_BIZ": [
        "base_yymm", "appl_biz_dv", "ir_curve_id", "ir_curve_sce_no", "mat_cd",
        "spot_rate", "fwd_rate", "last_modified_by", "last_update_date",
    ],
    "E_IR_DCNT_SCE_STO_BIZ": [
        "base_yymm", "appl_biz_dv", "ir_model_id", "ir_curve_id",
        "ir_curve_sce_no", "sce_no", "mat_cd", "spot_rate", "fwd_rate",
        "last_modified_by", "last_update_date",
    ],
    "E_IR_PARAM_HW_CALC": [
        "base_yymm", "ir_model_id", "ir_curve_id", "mat_cd", "param_typ_cd",
        "param_val", "last_modified_by", "last_update_date",
    ],
    "E_IR_PARAM_HW_BIZ": [
        "base_yymm", "appl_biz_dv", "ir_model_id", "ir_curve_id", "mat_cd",
        "param_typ_cd", "param_val", "last_modified_by", "last_update_date",
    ],
    "E_IR_PARAM_MODEL": [
        "ir_model_id", "ir_model_nm", "ir_curve_id", "total_sce_no",
        "rnd_seed", "itr_tol", "use_yn", "last_modified_by", "last_update_date",
    ],
    "E_IR_PARAM_AFNS_BIZ": [
        "base_yymm", "ir_model_id", "ir_curve_id", "param_typ_cd",
        "param_val", "last_modified_by", "last_update_date",
    ],
    "E_IR_PARAM_SW": [
        "base_yymm", "appl_biz_dv", "ir_curve_id", "ir_curve_sce_no",
        "ir_curve_sce_nm", "cur_cd", "freq", "llp", "ltfr", "ltfr_cp",
        "liq_prem", "liq_prem_appl_dv", "shk_sprd_sce_no", "sw_alpha_ytm",
        "sto_sce_gen_yn", "fwd_mat_cd", "mult_int_rate", "add_sprd",
        "pvt_rate_mat_cd", "mult_pvt_rate", "last_modified_by", "last_update_date",
        "ytm_add_sprd",
    ],
    "E_IR_PARAM_SW_USR": [
        "appl_st_yymm", "appl_ed_yymm", "appl_biz_dv", "ir_curve_id",
        "ir_curve_sce_no", "ir_curve_sce_nm", "cur_cd", "freq", "llp",
        "ltfr", "ltfr_cp", "liq_prem", "liq_prem_appl_dv", "shk_sprd_sce_no",
        "sw_alpha_ytm", "sto_sce_gen_yn", "fwd_mat_cd", "mult_int_rate",
        "add_sprd", "pvt_rate_mat_cd", "mult_pvt_rate", "last_modified_by",
        "last_update_date", "ytm_add_sprd",
    ],
    "E_IR_VOL_SWPN": [
        "base_yymm", "ir_curve_id", "swpn_mat_num", "swap_ten_num",
        "vol", "last_modified_by", "last_update_date",
    ],
    "E_IR_SPRD_AFNS_BIZ": [
        "base_yymm", "ir_model_id", "ir_curve_id", "ir_curve_sce_no",
        "mat_cd", "shk_sprd_cont", "last_modified_by", "last_update_date",
    ],
    "E_RC_CORP_PD": [
        "base_yymm", "crd_eval_agncy_cd", "crd_grd_cd", "mat_cd",
        "cum_pd", "fwd_pd", "last_modified_by", "last_update_date",
    ],
    "E_RC_CORP_PD_BIZ": [
        "base_yymm", "appl_biz_dv", "crd_grd_cd", "mat_cd",
        "cum_pd", "fwd_pd", "last_modified_by", "last_update_date",
    ],
    "E_IR_VALID_RND": [
        "base_yymm", "ir_model_id", "ir_curve_id", "valid_dv", "valid_seq",
        "valid_val1", "valid_val2", "valid_val3", "valid_val4", "valid_val5",
        "last_modified_by", "last_update_date",
    ],
    "E_IR_VALID_SCE_STO": [
        "base_yymm", "appl_biz_dv", "ir_model_id", "ir_curve_id",
        "ir_curve_sce_no", "valid_dv", "valid_seq",
        "valid_val1", "valid_val2", "valid_val3", "valid_val4", "valid_val5",
        "last_modified_by", "last_update_date",
    ],
}

# ── 정규식 ────────────────────────────────────────────────────
_TO_DATE_RE  = re.compile(r"TO_DATE\('([^']+)','[^']+'\)")
_INSERT_RE   = re.compile(r"^INSERT INTO (\w+) VALUES \((.+)\);$")


def _to_date_sub(m: re.Match) -> str:
    return f"'{m.group(1)}'"


def _parse_values(raw: str) -> list:
    """Oracle VALUES 문자열을 Python 리스트로 파싱."""
    raw = _TO_DATE_RE.sub(_to_date_sub, raw)
    result: list = []
    i, n = 0, len(raw)

    while i < n:
        # 공백·쉼표 스킵
        while i < n and raw[i] in " \t\n":
            i += 1
        if i >= n:
            break
        if raw[i] == ",":
            i += 1
            continue

        if raw[i] == "'":
            # 문자열 리터럴 (' '로 이스케이프된 따옴표 처리)
            i += 1
            chars: list[str] = []
            while i < n:
                if raw[i] == "'" and i + 1 < n and raw[i + 1] == "'":
                    chars.append("'")
                    i += 2
                elif raw[i] == "'":
                    i += 1
                    break
                else:
                    chars.append(raw[i])
                    i += 1
            result.append("".join(chars))

        elif raw[i:i + 4] == "NULL":
            result.append(None)
            i += 4

        else:
            # 숫자 (음수 포함)
            j = i
            if j < n and raw[j] == "-":
                j += 1
            while j < n and raw[j] not in (", ", " ", "\t", "\n", ","):
                j += 1
            token = raw[i:j]
            try:
                result.append(int(token))
            except ValueError:
                try:
                    result.append(float(token))
                except ValueError:
                    result.append(token)
            i = j

    return result


def _flush(con: sqlite3.Connection, tbl: str, sql: str,
           rows: list, counts: dict) -> None:
    try:
        con.executemany(sql, rows)
        con.commit()
        counts[tbl] += len(rows)
        print(f"  {tbl}: 누계 {counts[tbl]:>8,}행", end="\r")
    except Exception as exc:
        con.rollback()
        print(f"\n  [{tbl}] 배치 오류: {exc}")


def main() -> None:
    print("=== Oracle → SQLite 데이터 이관 ===")
    print(f"SQL 파일: {MIGRATION_SQL}")
    print(f"DB 경로:  {DB_PATH}\n")

    # 테이블 생성 (미생성 시)
    SQLModel.metadata.create_all(bind=engine)

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    con.execute("PRAGMA foreign_keys=OFF")

    # INSERT SQL 사전 빌드
    insert_sqls: dict[str, str] = {}
    for tbl, cols in TABLE_MAP.items():
        col_list   = ", ".join(cols)
        ph         = ", ".join("?" * len(cols))
        insert_sqls[tbl] = f"INSERT OR IGNORE INTO {tbl} ({col_list}) VALUES ({ph})"

    batches: dict[str, list] = {t: [] for t in TABLE_MAP}
    counts:  dict[str, int]  = {t: 0  for t in TABLE_MAP}
    errors = 0
    line_no = 0

    with open(MIGRATION_SQL, encoding="utf-8", errors="replace") as f:
        for line in f:
            line_no += 1
            line = line.rstrip()
            m = _INSERT_RE.match(line)
            if not m:
                continue
            tbl = m.group(1)
            if tbl not in TABLE_MAP:
                continue

            try:
                vals = _parse_values(m.group(2))
            except Exception as exc:
                print(f"\n  파싱 오류 {line_no}행 ({tbl}): {exc}")
                errors += 1
                continue

            expected = len(TABLE_MAP[tbl])
            if len(vals) != expected:
                print(f"\n  컬럼 수 불일치 {line_no}행 ({tbl}): "
                      f"expected {expected}, got {len(vals)}")
                errors += 1
                continue

            batches[tbl].append(vals)
            if len(batches[tbl]) >= BATCH_SIZE:
                _flush(con, tbl, insert_sqls[tbl], batches[tbl], counts)
                batches[tbl] = []

    # 나머지 플러시
    for tbl in TABLE_MAP:
        if batches[tbl]:
            _flush(con, tbl, insert_sqls[tbl], batches[tbl], counts)

    con.execute("PRAGMA foreign_keys=ON")
    con.close()

    print("\n\n=== 이관 완료 ===")
    total = 0
    for tbl, cnt in counts.items():
        if cnt:
            print(f"  {tbl:<35} {cnt:>8,}행")
            total += cnt
    print(f"\n  합계: {total:,}행  |  오류: {errors}건")


if __name__ == "__main__":
    main()
