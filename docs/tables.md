# GesgViewer — DB 테이블 목록

> 출처: `data/esg.db` (SQLite) 실제 테이블 기준
> 최종 업데이트: 2026-03-21
>
> **범례**
> - ✅ SQLModel 클래스 + View 구현됨
> - ❌ DB만 존재 (미구현)
> - ⚠️ 구버전 테이블 (DDL 정렬 전 이름, 현재 미사용)

---

## 1. 환경설정

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_CO_JOB_INFO` | ESG 작업 이력 | ✅ |
| `E_CO_JOB_LIST` | ESG 작업 목록 | ✅ |
| `E_CO_ESG_META` | ESG 메타 정보 | ✅ |
| `E_CO_CD_MST` | 공통코드 마스터 | ❌ |
| `E_CO_JOB_HIST` | 작업 이력 (구) | ⚠️ |
| `COMTNBATCHOPERT` | 배치 작업 | ✅ |
| `COMTNBATCHRESULT` | 배치 결과 | ✅ |
| `COMTNBATCHSCHDUL` | 배치 스케줄 | ✅ |

---

## 2. 사용자 입력

### 2.1 금리정보

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_CURVE_YTM_USR` | 금리커브 YTM (사용자 입력) | ✅ |
| `E_IR_CURVE_YTM_USR_HIS` | 금리커브 YTM 사용자 이력 | ❌ |
| `E_IR_DCNT_RATE_USR` | 할인율 (사용자 입력) | ✅ |


### 2.2 금리스프레드

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_SPRD_AFNS_USR` | AFNS 스프레드 (사용자 입력) | ✅ |
| `E_IR_SPRD_LP_USR` | LP 스프레드 (사용자 입력) | ✅ |

### 2.3 Swap 변동성

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_VOL_SWPN_USR` | 변동성/스왑션 (사용자 입력) | ✅ |

### 2.4 기업 부도율

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_RC_CORP_TM_USR` | 기업 전환행렬 (사용자 입력) | ✅ |

### 2.5 매개변수

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_PARAM_SW_USR` | SW 파라미터 (사용자 입력) | ✅ |
| `E_IR_PARAM_AFNS_USR` | AFNS 파라미터 (사용자 입력) | ✅ |
| `E_IR_PARAM_HW_USR` | HW 파라미터 (사용자 입력) | ✅ |
| `E_IR_PARAM_MODEL_USR` | 파라미터 모델 (사용자 입력) | ✅ |

---

## 3. 기초데이터

### 3.1 금리정보

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_CURVE` | 금리 커브 (마스터) | ✅ |
| `E_IR_CURVE_YTM` | 금리커브 YTM | ✅ |
| `E_IR_CURVE_SPOT` | 금리커브 현물 | ✅ |
| `E_IR_CURVE_SPOT_WEEK` | 금리커브 현물 (주간) | ✅ |
| `E_IR_CURVE_FWD` | 금리커브 선도 | ✅ |
| `E_IR_PARAM_SW` | SW 파라미터 (산출) | ✅ |

### 3.2 금리스프레드

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_SPRD_CURVE` | 위험스프레드 커브 | ✅ |
| `E_IR_SPRD_AFNS_BIZ` | AFNS 충격 스프레드 | ✅ |
| `E_IR_SPRD_AFNS_CALC` | AFNS 스프레드 (계산) | ✅ |
| `E_IR_SPRD_CRD` | 신용 스프레드 | ❌ |
| `E_IR_SPRD_LP` | LP 스프레드 | ✅ |
| `E_IR_SPRD_LP_BIZ` | LP 스프레드 (비즈) | ✅ |

### 3.3 Swap 변동성

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_VOL_SWPN` | 변동성/스왑션 | ✅ |

### 3.4 매개변수

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_PARAM_AFNS_BIZ` | AFNS 모수생성결과 | ✅ |
| `E_IR_PARAM_AFNS_CALC` | AFNS 모수 계산 | ✅ |
| `E_IR_PARAM_HW_CALC` | HW 파라미터 계산 | ✅ |
| `E_IR_PARAM_HW_BIZ` | HW 파라미터 (비즈 적용) | ✅ |
| `E_IR_PARAM_HW_RND` | HW 난수 | ✅ |
| `E_IR_PARAM_MODEL` | 파라미터 모델 | ✅ |
| `E_IR_PARAM_MODEL_CALC` | 파라미터 모델 계산 | ✅ |
| `E_IR_PARAM_MODEL_BIZ` | 파라미터 모델 (비즈) | ✅ |
| `E_IR_PARAM_MODEL_RND` | 파라미터 모델 난수 | ✅ |

---

## 4. 산출결과

### 4.1 할인율

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_DCNT_RATE` | 할인율 (선도 검증용) | ✅ |
| `E_IR_DCNT_RATE_BIZ` | 할인율 (비즈) | ✅ |
| `E_IR_DCNT_RATE_BU` | 할인율 (BU) | ✅ |
| `E_IR_DCNT_RATE_BU_IM` | 할인율 BU 내부모형 | ✅ |

### 4.2 금리시나리오

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_CURVE_SCE_BIZ` | 금리커브 시나리오 (비즈) | ✅ |
| `E_IR_DCNT_SCE_DET_BIZ` | 확률시나리오 상세 (비즈) | ✅ |
| `E_IR_DCNT_SCE_IM` | 확률시나리오 내부모형 | ✅ |
| `E_IR_DCNT_SCE_STO_BIZ` | 확률시나리오 저장 (비즈) | ✅ |
| `E_IR_DCNT_SCE_STO_GNR` | 확률시나리오 저장 (일반) | ✅ |
| `E_IR_DCNT_STO_BIZ` | 시나리오 저장 비즈 (구) | ⚠️ |

### 4.3 기업 부도율

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_RC_CORP_TM` | 기업 전환행렬 | ✅ |
| `E_RC_CORP_PD` | 기업 부도율 (신용등급별) | ✅ |
| `E_RC_CORP_PD_BIZ` | 기업 부도율 (비즈) | ✅ |

---

## 5. 결과검증

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_IR_VALID_PARAM_HW` | HW 파라미터 검증 | ✅ |
| `E_IR_VALID_RND` | 랜덤 검증 | ✅ |
| `E_IR_VALID_SCE_STO` | 시나리오 저장 검증 | ✅ |
| `E_IR_QVAL_SCE` | Q값 시나리오 검증 | ✅ |

---

## 6. 시스템 관리

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `APP_USER` | 사용자 | ✅ |
| `LETTNAUTHORINFO` | 권한 정보 | ✅ |
| `LETTNAUTHORGROUPINFO` | 그룹 정보 | ✅ |
| `LETTNBASEDATE` | 개인 기준년월 | ✅ |
| `LETTNLGNPOLICY` | 로그인 정책 | ✅ |
| `LETTNBBS` | 공지사항 | ✅ |
| `LETTNMENUINFO` | 메뉴 목록 | ✅ |
| `LETTNPROGRMLIST` | 프로그램 관리 | ✅ |
| `COMTCCMMNCLCODE` | 공통분류코드 | ✅ |

---

## 기타 (메뉴 미분류)

| 테이블명 | 한글명 | 구현 |
|---|---|:---:|
| `E_BZ_INV_COST` | 투자비용 | ❌ |
| `E_FX_RATE` | 환율 | ❌ |
| `E_MV_CORR` | 상관계수 | ❌ |
| `E_MV_VOL` | 변동성 (주식) | ❌ |
| `E_STD_ASST` | 표준자산 | ❌ |
| `E_STD_ASST_IR_SCE_STO` | 표준자산 금리시나리오 저장 | ❌ |
| `E_STD_ASST_PRC` | 표준자산 가격 | ❌ |

---

## 구버전 테이블 (DDL 정렬 전 이름, ⚠️)

> 현재 DB에 잔존하나 SQLModel 모델에서 제거된 구버전 테이블

| 구버전 테이블명 | 현재 테이블명 | 한글명 |
|---|---|---|
| `E_CO_JOB_HIST` | `E_CO_JOB_INFO` | 작업 이력 |
| `E_CORP_PD` | `E_RC_CORP_PD` | 기업 부도율 |
| `E_CRD_CORP_PD` | `E_RC_CORP_PD` | 기업 부도율 (신용등급별) |
| `E_DCNT_STO_BIZ` → | `E_IR_DCNT_SCE_STO_BIZ` | 확률시나리오 저장 (비즈) |
| `E_SPRD_AFNS_BIZ` | `E_IR_SPRD_AFNS_BIZ` | AFNS 충격 스프레드 |
| `E_SPRD_CURVE` | `E_IR_SPRD_CURVE` | 위험스프레드 커브 |
| `E_VALID_RND` | `E_IR_VALID_RND` | 랜덤 검증 |
| `E_VALID_SCE_FWD` | `E_IR_DCNT_RATE` | 할인율 (선도 검증용) |
| `E_VALID_SCE_STO` | `E_IR_VALID_SCE_STO` | 시나리오 저장 검증 |
| `E_VOL_SWPN` | `E_IR_VOL_SWPN` | 변동성/스왑션 |

---

## 전체 목록 (알파벳순)

| # | 테이블명 | 한글명 | 구현 |
|---|---|---|:---:|
| 1 | `APP_USER` | 사용자 | ✅ |
| 2 | `COMTCCMMNCLCODE` | 공통분류코드 | ✅ |
| 3 | `COMTNBATCHOPERT` | 배치 작업 | ✅ |
| 4 | `COMTNBATCHRESULT` | 배치 결과 | ✅ |
| 5 | `COMTNBATCHSCHDUL` | 배치 스케줄 | ✅ |
| 8 | `E_CO_CD_MST` | 공통코드 마스터 | ❌ |
| 9 | `E_CO_ESG_META` | ESG 메타 정보 | ✅ |
| 10 | `E_CO_JOB_HIST` | 작업 이력 (구) | ⚠️ |
| 11 | `E_CO_JOB_INFO` | 작업 이력 | ✅ |
| 12 | `E_CO_JOB_LIST` | 작업 목록 | ✅ |
| 16 | `E_IR_CURVE` | 금리 커브 (마스터) | ✅ |
| 17 | `E_IR_CURVE_FWD` | 금리커브 선도 | ✅ |
| 18 | `E_IR_CURVE_SCE_BIZ` | 금리커브 시나리오 (비즈) | ✅ |
| 19 | `E_IR_CURVE_SPOT` | 금리커브 현물 | ✅ |
| 20 | `E_IR_CURVE_SPOT_WEEK` | 금리커브 현물 (주간) | ✅ |
| 21 | `E_IR_CURVE_YTM` | 금리커브 YTM | ✅ |
| 22 | `E_IR_CURVE_YTM_USR` | 금리커브 YTM (사용자 입력) | ✅ |
| 23 | `E_IR_CURVE_YTM_USR_HIS` | 금리커브 YTM 사용자 이력 | ❌ |
| 24 | `E_IR_DCNT_RATE` | 할인율 (선도 검증용) | ✅ |
| 25 | `E_IR_DCNT_RATE_BIZ` | 할인율 (비즈) | ✅ |
| 26 | `E_IR_DCNT_RATE_BU` | 할인율 (BU) | ✅ |
| 27 | `E_IR_DCNT_RATE_BU_IM` | 할인율 BU 내부모형 | ✅ |
| 28 | `E_IR_DCNT_RATE_USR` | 할인율 (사용자 입력) | ✅ |
| 29 | `E_IR_DCNT_SCE_DET_BIZ` | 확률시나리오 상세 (비즈) | ✅ |
| 30 | `E_IR_DCNT_SCE_IM` | 확률시나리오 내부모형 | ✅ |
| 31 | `E_IR_DCNT_SCE_STO_BIZ` | 확률시나리오 저장 (비즈) | ✅ |
| 32 | `E_IR_DCNT_SCE_STO_GNR` | 확률시나리오 저장 (일반) | ✅ |
| 33 | `E_IR_DCNT_STO_BIZ` | 시나리오 저장 비즈 (구) | ⚠️ |
| 34 | `E_IR_PARAM_AFNS_BIZ` | AFNS 모수생성결과 | ✅ |
| 35 | `E_IR_PARAM_AFNS_CALC` | AFNS 모수 계산 | ✅ |
| 36 | `E_IR_PARAM_AFNS_USR` | AFNS 파라미터 (사용자 입력) | ✅ |
| 37 | `E_IR_PARAM_HW_BIZ` | HW 파라미터 (비즈 적용) | ✅ |
| 38 | `E_IR_PARAM_HW_CALC` | HW 파라미터 계산 | ✅ |
| 39 | `E_IR_PARAM_HW_RND` | HW 난수 | ✅ |
| 40 | `E_IR_PARAM_HW_USR` | HW 파라미터 (사용자 입력) | ✅ |
| 41 | `E_IR_PARAM_MODEL` | 파라미터 모델 | ✅ |
| 42 | `E_IR_PARAM_MODEL_BIZ` | 파라미터 모델 (비즈) | ✅ |
| 43 | `E_IR_PARAM_MODEL_CALC` | 파라미터 모델 계산 | ✅ |
| 44 | `E_IR_PARAM_MODEL_RND` | 파라미터 모델 난수 | ✅ |
| 45 | `E_IR_PARAM_MODEL_USR` | 파라미터 모델 (사용자 입력) | ✅ |
| 46 | `E_IR_PARAM_SW` | SW 파라미터 (산출) | ✅ |
| 47 | `E_IR_PARAM_SW_USR` | SW 파라미터 (사용자 입력) | ✅ |
| 48 | `E_IR_QVAL_SCE` | Q값 시나리오 검증 | ✅ |
| 49 | `E_IR_SPRD_AFNS_BIZ` | AFNS 충격 스프레드 | ✅ |
| 50 | `E_IR_SPRD_AFNS_CALC` | AFNS 스프레드 계산 | ✅ |
| 51 | `E_IR_SPRD_AFNS_USR` | AFNS 스프레드 (사용자 입력) | ✅ |
| 52 | `E_IR_SPRD_CRD` | 신용 스프레드 | ❌ |
| 53 | `E_IR_SPRD_CURVE` | 위험스프레드 커브 | ✅ |
| 54 | `E_IR_SPRD_LP` | LP 스프레드 | ✅ |
| 55 | `E_IR_SPRD_LP_BIZ` | LP 스프레드 (비즈) | ✅ |
| 56 | `E_IR_SPRD_LP_USR` | LP 스프레드 (사용자 입력) | ✅ |
| 57 | `E_IR_VALID_PARAM_HW` | HW 파라미터 검증 | ✅ |
| 58 | `E_IR_VALID_RND` | 랜덤 검증 | ✅ |
| 59 | `E_IR_VALID_SCE_STO` | 시나리오 저장 검증 | ✅ |
| 60 | `E_IR_VOL_SWPN` | 변동성/스왑션 | ✅ |
| 61 | `E_IR_VOL_SWPN_USR` | 변동성/스왑션 (사용자 입력) | ✅ |
| 64 | `E_RC_CORP_PD` | 기업 부도율 (신용등급별) | ✅ |
| 65 | `E_RC_CORP_PD_BIZ` | 기업 부도율 (비즈) | ✅ |
| 66 | `E_RC_CORP_TM` | 기업 전환행렬 | ✅ |
| 67 | `E_RC_CORP_TM_USR` | 기업 전환행렬 (사용자 입력) | ✅ |
| 77 | `LETTNAUTHORGROUPINFO` | 그룹 정보 | ✅ |
| 78 | `LETTNAUTHORINFO` | 권한 정보 | ✅ |
| 79 | `LETTNBASEDATE` | 개인 기준년월 | ✅ |
| 80 | `LETTNBBS` | 공지사항 | ✅ |
| 81 | `LETTNLGNPOLICY` | 로그인 정책 | ✅ |
| 82 | `LETTNMENUINFO` | 메뉴 목록 | ✅ |
| 83 | `LETTNPROGRMLIST` | 프로그램 관리 | ✅ |

---

_총 83개 테이블 | ✅ 구현 62개 · ❌ 미구현 11개 · ⚠️ 구버전 10개_
