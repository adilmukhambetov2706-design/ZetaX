from datetime import datetime
import os
from tkinter import filedialog, messagebox
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape

import customtkinter as ctk

from Weather_info import Mid_frame_info
from i18n import t, set_language, get_language_name

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SettingsPage(ctk.CTkToplevel):

    def __init__(self, master=None, city="Bishkek"):
        super().__init__(master)
        self.city = city

        self.geometry("390x780")
        self.title("Settings")
        self.configure(fg_color="#050B45")

        self.selected_language = get_language_name()
        self.last_export_path = None

        self.build_ui()

    def build_ui(self):

        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#2D3AA8",
            scrollbar_button_hover_color="#3C4BCE"
        )
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        # =========================
        # HEADER
        # =========================

        top = ctk.CTkFrame(scroll, fg_color="transparent")
        top.pack(fill="x", pady=(5, 0))

        back_btn = ctk.CTkButton(
            top,
            text="←",
            width=34,
            height=34,
            corner_radius=17,
            fg_color="transparent",
            hover_color="#141D73",
            font=("Arial", 22),
            command=self.destroy
        )
        back_btn.pack(anchor="w", padx=5)

        title = ctk.CTkLabel(
            scroll,
            text=t("setting"),
            font=("Arial", 38, "bold"),
            text_color="white"
        )
        title.pack(pady=(10, 0))

        subtitle = ctk.CTkLabel(
            scroll,
            text=t("customizeWeather"),
            font=("Arial", 15),
            text_color="#8E95D9"
        )
        subtitle.pack(pady=(0, 30))

        # =========================
        # LANGUAGE
        # =========================

        self.section_title(scroll, t("language"))

        lang_card = self.card(scroll, 165)

        self.language_buttons = {}

        self.language_option(lang_card, "Kyrgyz", t("kyrgyz"))
        self.separator(lang_card)

        self.language_option(lang_card, "Russian", t("russian"))
        self.separator(lang_card)

        self.language_option(lang_card, "English", t("english"))
        self.update_language_buttons()

        # =========================
        # EXPORT DATA
        # =========================

        self.section_title(scroll, t("exportData"))

        export_card = self.card(scroll, 190)

        top_row = ctk.CTkFrame(export_card, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(15, 8))

        export_label = ctk.CTkLabel(
            top_row,
            text=t("exportExcel"),
            font=("Arial", 16),
            text_color="white"
        )
        export_label.pack(side="left")

        export_btn = ctk.CTkButton(
            top_row,
            text="Export",
            width=85,
            height=32,
            corner_radius=16,
            fg_color="#7D5CFF",
            hover_color="#6947F5",
            font=("Arial", 13, "bold"),
            command=self.export_excel
        )
        export_btn.pack(side="right")

        export_weather = ctk.CTkLabel(
            export_card,
            text=t("exportWeatherData") + " 📄",
            font=("Arial", 16),
            text_color="white"
        )
        export_weather.pack(anchor="w", padx=16, pady=(8, 0))

        desc = ctk.CTkLabel(
            export_card,
            text=f"{t('exportWeeklyForecast')}\n{t('exportAirQuality')}\n{t('exportHistory')}",
            justify="left",
            font=("Arial", 12),
            text_color="#8E95D9"
        )
        desc.pack(anchor="w", padx=16, pady=(4, 0))

        open_btn = ctk.CTkButton(
            export_card,
            text=t("open") + " >",
            width=70,
            height=28,
            fg_color="transparent",
            hover_color="#1A247D",
            text_color="#8D6BFF",
            corner_radius=14,
            font=("Arial", 13, "bold"),
            command=self.open_exported_excel
        )
        open_btn.pack(anchor="e", padx=16, pady=(0, 12))

    def open_calendar(self):
        from Calendar import CalendarPage

        root = self.master
        self.destroy()

        calendar_page = CalendarPage(root, self.city)
        calendar_page.focus()

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Export Excel",
            defaultextension=".xlsx",
            initialfile=f"zeta_x_{self.city}_{datetime.now():%Y%m%d}.xlsx",
            filetypes=[("Excel workbook", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            rows = self.get_export_rows()
            self.write_xlsx(file_path, rows)
            self.last_export_path = file_path
            messagebox.showinfo("Export Excel", "Excel file exported successfully.", parent=self)
        except Exception as exc:
            messagebox.showerror("Export Excel", f"Could not export Excel file:\n{exc}", parent=self)

    def open_exported_excel(self):
        file_path = self.last_export_path
        if not file_path or not os.path.exists(file_path):
            file_path = filedialog.askopenfilename(
                parent=self,
                title="Open Excel",
                filetypes=[("Excel workbook", "*.xlsx")]
            )
        if not file_path:
            return

        try:
            os.startfile(file_path)
            self.last_export_path = file_path
        except Exception as exc:
            messagebox.showerror("Open Excel", f"Could not open Excel file:\n{exc}", parent=self)

    def get_export_rows(self):
        rows = [
            ["Zeta-X Weather Export"],
            ["City", self.city],
            ["Generated", datetime.now().strftime("%Y-%m-%d %H:%M")],
            [],
            ["Metric", "Value"],
        ]

        try:
            info = Mid_frame_info(self.city)
            rows.extend([
                ["Current temperature", f"{info.temp_today(0):.1f} C"],
                ["Wind speed", f"{info.wind_speed():.1f} KM/H"],
                ["Wind direction", f"{info.wind_direction_degrees()} degrees"],
                ["Sunrise", info.sunrise_time()],
                ["Sunset", info.sunset_time()],
                ["Air quality", str(info.air_quality())],
            ])
        except Exception:
            rows.extend([
                ["Current temperature", "N/A"],
                ["Wind speed", "N/A"],
                ["Wind direction", "N/A"],
                ["Sunrise", "N/A"],
                ["Sunset", "N/A"],
                ["Air quality", "N/A"],
            ])

        return rows

    def write_xlsx(self, file_path, rows):
        sheet_xml = self.build_sheet_xml(rows)
        workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Weather Export" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>"""
        workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""
        root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""
        styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="14"/><name val="Calibri"/></font></fonts>
  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" applyFont="1"/></cellXfs>
</styleSheet>"""

        with ZipFile(file_path, "w", ZIP_DEFLATED) as workbook:
            workbook.writestr("[Content_Types].xml", content_types)
            workbook.writestr("_rels/.rels", root_rels)
            workbook.writestr("xl/workbook.xml", workbook_xml)
            workbook.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
            workbook.writestr("xl/worksheets/sheet1.xml", sheet_xml)
            workbook.writestr("xl/styles.xml", styles_xml)

    def build_sheet_xml(self, rows):
        body = []
        for row_index, row in enumerate(rows, start=1):
            cells = []
            for col_index, value in enumerate(row, start=1):
                ref = f"{self.excel_column(col_index)}{row_index}"
                style = ' s="1"' if row_index in (1, 5) else ""
                cells.append(
                    f'<c r="{ref}" t="inlineStr"{style}><is><t>{escape(str(value))}</t></is></c>'
                )
            body.append(f'<row r="{row_index}">{"".join(cells)}</row>')

        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <cols><col min="1" max="1" width="26" customWidth="1"/><col min="2" max="2" width="34" customWidth="1"/></cols>
  <sheetData>{"".join(body)}</sheetData>
</worksheet>"""

    def excel_column(self, number):
        result = ""
        while number:
            number, remainder = divmod(number - 1, 26)
            result = chr(65 + remainder) + result
        return result

    # =====================================
    # COMPONENTS
    # =====================================

    def section_title(self, parent, text):

        label = ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", 12),
            text_color="#8E95D9"
        )
        label.pack(anchor="w", padx=10, pady=(12, 8))

    def card(self, parent, height):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#18236D",
            corner_radius=24,
            height=height
        )
        frame.pack(fill="x", padx=6, pady=4)

        frame.pack_propagate(False)

        return frame

    def separator(self, parent):

        line = ctk.CTkFrame(
            parent,
            height=1,
            fg_color="#28358D"
        )
        line.pack(fill="x", padx=16)

    def option(self, parent, text, switch=False):

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=14)

        label = ctk.CTkLabel(
            row,
            text=text,
            font=("Arial", 16),
            text_color="white"
        )
        label.pack(side="left")

        if switch:
            sw = ctk.CTkSwitch(
                row,
                text="",
                progress_color="#7D5CFF",
                button_color="white",
                button_hover_color="#F2F2F2"
            )
            sw.select()
            sw.pack(side="right")

    # =====================================
    # LANGUAGE SWITCHING
    # =====================================

    def language_option(self, parent, name, display_text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(row, text=display_text, font=("Arial", 16), text_color="white").pack(side="left")

        switch = ctk.CTkSwitch(
            row,
            text="",
            progress_color="#7D5CFF",
            button_color="white",
            button_hover_color="#F2F2F2",
            command=lambda n=name: self.select_language(n)
        )
        switch.pack(side="right")

        self.language_buttons[name] = switch

    def select_language(self, language):
        self.selected_language = language
        self.update_language_buttons()
        set_language(language)
        root = self.master
        self.destroy()
        if hasattr(root, "show_main_page"):
            root.show_main_page()
        elif hasattr(root, "build_page"):
            root.build_page()

    def update_language_buttons(self):

        for lang, switch in self.language_buttons.items():

            if lang == self.selected_language:
                switch.select()
            else:
                switch.deselect()


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    settings_page = SettingsPage(app)
    settings_page.protocol("WM_DELETE_WINDOW", app.destroy)
    app.mainloop()
