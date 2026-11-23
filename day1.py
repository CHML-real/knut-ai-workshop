"""행정 문의를 분류하고 담당자가 먼저 확인할 미회신 목록을 만든다."""
import pandas as pd
from common import DATA, write_excel

RULES = {
    "학사": ["수강", "휴학", "복학", "성적", "졸업"],
    "재무": ["등록금", "환불", "납부"],
    "시설": ["냉난방", "누수", "조명", "콘센트"],
    "전산": ["로그인", "와이파이", "비밀번호", "포털"],
    "학생지원": ["학생증"],
}


def classify(message):
    if pd.isna(message) or not str(message).strip():
        return "검토", "본문 누락"
    matches = [name for name, words in RULES.items() if any(word in message for word in words)]
    if len(matches) > 1:
        return "검토", " / ".join(matches)
    return (matches[0], matches[0]) if matches else ("기타", "키워드 없음")


def main():
    path = DATA / "01_행정문의.xlsx"
    cases = pd.read_excel(path, sheet_name="문의접수")
    log = pd.read_excel(path, sheet_name="처리이력")
    latest = log.sort_values("순번").drop_duplicates("문의ID", keep="last")
    cases = cases.merge(latest[["문의ID", "상태"]], on="문의ID", how="left", validate="one_to_one")
    cases[["담당분야", "판단근거"]] = pd.DataFrame(cases["문의내용"].map(classify).tolist(), index=cases.index)
    review = cases[cases["담당분야"].isin(["검토", "기타"]) & cases["상태"].ne("회신 완료")]
    counts = cases.groupby(["담당분야", "접수경로"]).size().reset_index(name="문의건수")
    write_excel("01_문의분류결과.xlsx", {"전체분류": cases, "미회신_검토후보": review, "분야별_접수경로": counts})
    print(f"문의 {len(cases)}건 처리, 미회신 검토 후보 {len(review)}건")


if __name__ == "__main__":
    main()
