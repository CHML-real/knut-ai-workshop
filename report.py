from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from common import RESULTS


def label(slide, x, y, w, h, value, size, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    run = box.text_frame.paragraphs[0].add_run()
    run.text = value
    run.font.name = "맑은 고딕"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string("164D57")


def make_report(year, quarter, total, departments):
    deck = Presentation()
    deck.slide_width, deck.slide_height = Inches(13.33), Inches(7.5)

    def slide(title):
        page = deck.slides.add_slide(deck.slide_layouts[6])
        label(page, .65, .4, 12, .8, title, 28, True)
        label(page, .65, 6.98, 12, .4, f"{year}년 {quarter}분기  |  대학 행정 실습용 가상자료", 12)
        return page

    page = slide(f"{year}년 {quarter}분기 예산 집행 보고")
    for i, (title, field) in enumerate([("이번 분기 순집행", "분기 순집행액"), ("직전 분기 대비 증감", "전분기 대비 증감액"), ("분기 말 잔여 예산", "기말 예산잔액")]):
        y = 1.55 + i * 1.45
        label(page, .8, y, 4.5, .6, title, 20)
        label(page, 5, y-.1, 7.5, .9, f"{total[field]:,.0f} 원", 30, True)
    page = slide("부서별 순집행액 비교")
    data = CategoryChartData()
    ordered = departments.sort_values("분기 순집행액")
    data.categories = ordered["부서"].tolist()
    for field in ["직전분기 순집행액", "분기 순집행액"]:
        data.add_series(field, (ordered[field] / 10000).tolist())
    chart = page.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(.8), Inches(1.4), Inches(11.6), Inches(5.2), data).chart
    chart.has_legend = True
    chart.value_axis.has_title = True
    chart.value_axis.axis_title.text_frame.text = "단위 · 만 원"
    page = slide("기말 잔액 산출 근거")
    for i, field in enumerate(["연간예산현액", "누적집행액", "기말 예산잔액"]):
        label(page, .9, 1.65+i, 11.5, .7, f"{field}     {total[field]:,.0f} 원", 24)
    label(page, .9, 5.3, 11.7, .9, f"1~{quarter * 3}월 확정 지출과 음수 환입을 합산했습니다. 승인대기·반려 전표는 제외했습니다.", 18)
    deck.save(RESULTS / "03_분기보고.pptx")
