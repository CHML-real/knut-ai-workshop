from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def write_excel(filename, sheets):
    with pd.ExcelWriter(RESULTS / filename, engine="openpyxl") as writer:
        for title, frame in sheets.items():
            frame.to_excel(writer, sheet_name=title, index=False)
            sheet = writer.sheets[title]
            sheet.freeze_panes = "B2"
            sheet.auto_filter.ref = sheet.dimensions
            for i, name in enumerate(frame.columns, 1):
                width = max(len(str(v)) for v in [name, *frame[name].dropna()])
                sheet.column_dimensions[get_column_letter(i)].width = min(88, max(15, 2 * width + 2))
                header = sheet.cell(1, i)
                header.fill = PatternFill("solid", fgColor="175463")
                header.font = Font(color="FFFFFF", bold=True)
                for (cell,) in sheet.iter_rows(min_row=2, min_col=i, max_col=i):
                    if name == "문의내용":
                        cell.alignment = Alignment(wrap_text=True, vertical="center")
                        sheet.row_dimensions[cell.row].height = 72
                    if "집행률" in name:
                        cell.number_format = "0.00%"
                    elif isinstance(cell.value, (int, float)):
                        cell.number_format = "#,##0;[Red](#,##0);0"
