"""사업·부서별 분기 집행과 누적 잔액을 계산하고 발표용 보고서를 만든다."""
from datetime import date

import pandas as pd
from common import DATA, write_excel
from report import make_report

YEAR = 2026
QUARTER = 3


def main():
    path = DATA / "02_예산집행.xlsx"
    projects = pd.read_excel(path, sheet_name="사업예산")
    ledger = pd.read_excel(path, sheet_name="지출원장")
    if not projects["사업코드"].is_unique or not ledger["전표ID"].is_unique:
        raise ValueError("중복된 사업코드 또는 전표ID를 확인하세요.")
    if not ledger["사업코드"].isin(projects["사업코드"]).all():
        raise ValueError("예산표에서 찾을 수 없는 사업코드가 있습니다.")
    period = pd.Period(date(YEAR, QUARTER * 3, 1), freq="Q")
    periods = pd.to_datetime(ledger["처리일"]).dt.to_period("Q")
    accepted = ledger["상태"].isin(["확정", "환입"])
    current = periods.eq(period)
    ledger["분기판정"] = "기간 외"
    ledger.loc[current, "분기판정"] = "미확정"
    for state, label in [("환입", "음수 환입 반영"), ("확정", "확정 지출 반영")]:
        ledger.loc[current & ledger["상태"].eq(state), "분기판정"] = label
    ledger["분기반영액"] = ledger["금액_원"].where(current & accepted, 0)
    projects["연간예산현액"] = projects["본예산_원"] + projects["조정액_원"]
    for name, mask in {
        "분기 순집행액": current,
        "직전분기 순집행액": periods.eq(period - 1),
        "누적집행액": periods.le(period) & periods.dt.year.eq(YEAR),
    }.items():
        amounts = ledger.loc[accepted & mask].groupby("사업코드")["금액_원"].sum()
        projects[name] = projects["사업코드"].map(amounts).fillna(0).astype(int)
    money = ["연간예산현액", "분기 순집행액", "직전분기 순집행액", "누적집행액"]
    depts = projects.groupby("부서", as_index=False)[money].sum()
    total = pd.DataFrame([projects[money].sum()])
    for frame in [projects, depts, total]:
        frame["분기 집행률"] = frame["분기 순집행액"].div(frame["연간예산현액"].replace(0, float("nan")))
        frame["전분기 대비 증감액"] = frame["분기 순집행액"] - frame["직전분기 순집행액"]
        frame["기말 예산잔액"] = frame["연간예산현액"] - frame["누적집행액"]
    write_excel("02_예산분석.xlsx", {"전체": total, "부서별": depts, "사업별": projects, "전표판정": ledger})
    make_report(YEAR, QUARTER, total.iloc[0], depts)
    print(f"{period} 예산 분석 및 PPT 생성 완료")


if __name__ == "__main__":
    main()
