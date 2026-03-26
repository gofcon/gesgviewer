"""
앱 내비게이션 트리 정의 — DB 시드(seed) 및 폴백(fallback) 용도

형식: [(카테고리명, [(그룹명, [(메뉴명, view_key)])])]

규칙
  • view_key 는 main_window._lazy_views() 의 딕셔너리 키와 일치해야 함
  • "__" 로 시작하는 key 는 뷰 클래스가 아닌 특수 동작 (ex: __help__, __about__)
"""

NAV_TREE: list = [
    ("환경설정", [
        ("ESG 작업정보", [
            ("ESG 작업 정보", "co_job"),
        ]),
        ("배치관리", [
            ("배치 작업 관리",   "batch_opert"),
            ("배치 결과 관리",   "batch_result"),
            ("배치 스케줄 관리", "batch_schd"),
        ]),
    ]),
    ("사용자 입력", [
        ("금리정보", [
            ("YTM 사용자 입력",    "ytm_usr"),
            ("할인율 사용자 입력", "dcnt_rate_usr"),
        ]),
        ("금리스프레드", [
            ("AFNS 스프레드 사용자 입력", "sprd_afns_usr"),
            ("LP 스프레드 사용자 입력",   "sprd_lp_usr"),
        ]),
        ("Swap 변동성", [
            ("변동성/스왑션 사용자 입력", "vol_swpn_usr"),
        ]),
        ("기업 부도율", [
            ("기업 전환행렬 사용자 입력", "corp_tm_usr"),
        ]),
        ("매개변수", [
            ("Smith-Wilson 사용자 파라미터", "param_sw"),
            ("AFNS 파라미터 사용자 입력",    "param_afns_usr"),
            ("HW 파라미터 사용자 입력",       "param_hw_usr"),
            ("파라미터 모델 사용자 입력",     "param_model_usr"),
        ]),
    ]),
    ("기초데이터", [
        ("금리정보", [
            ("금리 커브",           "ir_curve"),
            ("금리커브 YTM",        "ir_curve_ytm"),
            ("금리커브 현물(주간)", "ir_curve_spot_week"),
            ("금리커브 선도",       "ir_curve_fwd"),
        ]),
        ("금리스프레드", [
            ("AFNS 스프레드",         "sprd_afns"),
            ("AFNS 스프레드 계산",    "sprd_afns_calc"),
            ("위험스프레드 커브",     "sprd_curve"),
            ("LP 스프레드",           "sprd_lp"),
            ("LP 스프레드 비즈",      "sprd_lp_biz"),
        ]),
        ("Swap 변동성", [
            ("변동성/스왑션",        "vol_swpn"),
        ]),
        ("매개변수", [
            ("HW Calc 파라미터",       "param_hw_calc"),
            ("HW Biz 적용 파라미터",   "param_hw_biz"),
            ("AFNS 모수생성결과",      "param_afns"),
            ("AFNS 모수 계산",         "param_afns_calc"),
            ("파라미터 모델",          "param_model"),
            ("파라미터 모델 계산",     "param_model_calc"),
            ("파라미터 모델 비즈",     "param_model_biz"),
            ("HW 난수",               "param_hw_rnd"),
            ("파라미터 모델 난수",     "param_model_rnd"),
        ]),
    ]),
    ("산출결과", [
        ("할인율", [
            ("할인율 비즈",           "dcnt_rate"),
            ("할인율 BU",             "dcnt_rate_bu"),
            ("할인율 BU 내부모형",    "dcnt_rate_bu_im"),
        ]),
        ("금리시나리오", [
            ("확률시나리오 저장(비즈)",   "dcnt_sto"),
            ("확률시나리오 저장(일반)",   "dcnt_sce_sto_gnr"),
            ("확률시나리오 상세(비즈)",   "dcnt_sce_det"),
            ("확률시나리오 내부모형",     "dcnt_sce_im"),
            ("금리커브 시나리오(비즈)",   "ir_curve_sce_biz"),
        ]),
        ("기업 부도율", [
            ("기업 전환행렬",          "corp_tm"),
            ("기업 부도율",            "corp_pd"),
            ("신용등급 기업 부도율",   "crd_corp_pd"),
        ]),
    ]),
    ("결과 검증", [
        ("검증", [
            ("시나리오 선도 검증",    "valid_fwd"),
            ("시나리오 랜덤 검증",   "valid_rnd"),
            ("시나리오 저장 검증",   "valid_sce_sto"),
            ("HW 파라미터 검증",     "valid_param_hw"),
            ("Q값 시나리오 검증",    "qval_sce"),
        ]),
    ]),
    ("시스템 관리", [
        ("시스템 관리", [
            ("사용자 목록",         "usr_mng"),
            ("사용자별 권한 관리",  "auth_group"),
            ("사용자 권한 목록",    "auth_info"),
            ("로그인 정책",         "lgn_policy"),
            ("메뉴 목록 관리",      "mnu_mng"),
            ("프로그램 관리",       "pgm_mng"),
            ("개인 기준일자",       "indiv_base_dt"),
        ]),
    ]),
    ("데이터", [
        ("데이터 탐색", [
            ("데이터 브라우저",  "data_browser"),
        ]),
    ]),
    ("도움말", [
        ("도움말", [
            ("도움말", "help"),
            ("정보",   "__about__"),
        ]),
    ]),
]
