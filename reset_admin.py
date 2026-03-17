#!/usr/bin/env python3
"""
admin 비밀번호 초기화 유틸리티
실행:
  python reset_admin.py                    # data/esg.db  에 admin/admin 재설정
  python reset_admin.py --password 1234   # 비밀번호 변경
  python reset_admin.py --db /path/to/esg.db  # 특정 DB 지정
"""
import sys
import os
import sqlite3
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def reset_admin(db_path: str, new_password: str = "admin") -> None:
    import bcrypt

    print(f"[DB] {db_path}")

    if not os.path.exists(db_path):
        print("DB 파일이 없습니다. 먼저 앱을 한 번 실행하거나 db/init_db.py 를 실행하세요.")
        sys.exit(1)

    pw_bytes = new_password.encode("utf-8")
    hashed   = bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode()

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM APP_USER WHERE user_id='admin'")
        exists = cur.fetchone()

        if exists:
            cur.execute(
                "UPDATE APP_USER SET password=?, use_at='Y' WHERE user_id='admin'",
                (hashed,)
            )
            print(f"[UPDATE] admin 비밀번호를 '{new_password}' 로 재설정했습니다.")
        else:
            cur.execute(
                "INSERT INTO APP_USER (user_id, user_nm, password, email, author_code, use_at) "
                "VALUES ('admin','관리자',?,'admin@esg.co.kr','ROLE_ADMIN','Y')",
                (hashed,)
            )
            print(f"[INSERT] admin 계정을 '{new_password}' 로 새로 생성했습니다.")

        conn.commit()

        # 검증
        cur.execute("SELECT password, use_at FROM APP_USER WHERE user_id='admin'")
        row = cur.fetchone()
        ok = bcrypt.checkpw(pw_bytes, row[0].encode())
        print(f"[검증] use_at={row[1]}, bcrypt.checkpw={ok}")
        print("완료!")
    except Exception as exc:
        conn.rollback()
        print(f"오류: {exc}")
        raise
    finally:
        conn.close()


def _resolve_db_path(db_arg: str | None) -> str:
    """db_arg 가 없으면 기본 data/esg.db 경로 반환"""
    if db_arg:
        return os.path.abspath(db_arg)
    # 환경변수 → settings.py 와 동일한 로직
    data_dir = os.environ.get(
        "ESG_DATA_DIR",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    )
    return os.path.join(data_dir, "esg.db")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="admin 비밀번호 재설정")
    parser.add_argument("--password", default="admin", help="새 비밀번호 (기본값: admin)")
    parser.add_argument("--db", default=None,
                        help="DB 파일 경로 (기본값: data/esg.db)")
    args = parser.parse_args()

    db_path = _resolve_db_path(args.db)
    reset_admin(db_path, args.password)
