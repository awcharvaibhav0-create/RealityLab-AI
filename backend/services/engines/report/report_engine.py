import json
import csv
import io


class ReportEngine:
    def __init__(self):
        pass

    def _strip_md(self, text):
        if not isinstance(text, str):
            return str(text)
        return text.replace("**", "").replace("__", "")

    def generate(self, data):
        return "report"

    def _strip_md_recursive(self, data):
        if isinstance(data, str):
            return self._strip_md(data)
        elif isinstance(data, dict):
            return {k: self._strip_md_recursive(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._strip_md_recursive(item) for item in data]
        return data

    def generate_json(self, data):
        cleaned = self._strip_md_recursive(data)
        return json.dumps(cleaned, indent=2).encode("utf-8")

    def generate_csv(self, data):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Section", "Metric", "Value"])
        
        metrics = data.get("metrics", {}) if isinstance(data, dict) else {}
        
        # Finance
        writer.writerow(["Finance", "Revenue", f"${metrics.get('revenue', 0):,.2f}"])
        writer.writerow(["Finance", "Profit", f"${metrics.get('profit', 0):,.2f}"])
        writer.writerow(["Finance", "ROI", f"{metrics.get('roi', 0)}%"])
        
        # Market
        m_data = metrics.get("market_analysis", {})
        writer.writerow(["Market", "Growth", self._strip_md(m_data.get('growth', ''))])
        writer.writerow(["Market", "Competition", self._strip_md(m_data.get('competition', ''))])
        writer.writerow(["Market", "Demand", self._strip_md(m_data.get('demand', ''))])
        writer.writerow(["Market", "Opportunity", self._strip_md(m_data.get('opportunity', ''))])
        writer.writerow(["Market", "Confidence", f"{m_data.get('confidence', 0)}%"])
        
        # Risk
        writer.writerow(["Risk", "Risk Score", metrics.get('risk_score', 0)])
        r_data = metrics.get("risk_analysis", {}).get("factors", [])
        for i, factor in enumerate(r_data):
            writer.writerow(["Risk", f"Factor {i+1}", self._strip_md(factor)])
            
        # Prediction (Handling dict of arrays)
        preds = metrics.get("predictions", {})
        if isinstance(preds, dict):
            for sc_name, curve in preds.items():
                curve_str = ", ".join([f"${c:,.2f}" if isinstance(c, (int, float)) else str(c) for c in curve])
                writer.writerow(["Prediction", sc_name, curve_str])
        elif isinstance(preds, list):
            for i, p in enumerate(preds):
                writer.writerow(["Prediction", f"Month {i+1}", p])
            
        # Timeline
        timeline = metrics.get("timeline", [])
        for phase in timeline:
            writer.writerow(["Timeline", self._strip_md(phase.get("name", "")), self._strip_md(phase.get("duration", ""))])
            
        # Evidence
        evidence = metrics.get("evidence", [])
        for ev in evidence:
            writer.writerow(["Evidence", self._strip_md(ev.get("title", "")), self._strip_md(ev.get("description", ""))])
            
        # Decision
        score = metrics.get("confidence", 0)
        writer.writerow(["Decision", "Score", score])
        rec = data.get("rationale", "")
        writer.writerow(["Decision", "Recommendation", self._strip_md(rec)])

        return output.getvalue().encode("utf-8")

    def generate_html(self, data):
        metrics = data.get("metrics", {}) if isinstance(data, dict) else {}
        
        html = """
        <html>
        <head>
            <title>RealityLab AI - Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; color: #333; line-height: 1.6; }
                h1 { color: #003366; border-bottom: 2px solid #003366; padding-bottom: 10px; margin-bottom: 30px; }
                h2 { color: #00509e; margin-top: 40px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
                h3 { color: #444; margin-top: 20px; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; margin-top: 15px; }
                th, td { text-align: left; padding: 10px; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; color: #333; }
                .metric-box { background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 15px; border-left: 4px solid #00509e; }
                .page-break { page-break-before: always; }
                ul { margin-top: 10px; }
                li { margin-bottom: 8px; }
            </style>
        </head>
        <body>
            <h1>RealityLab AI - Analysis Report</h1>
        """
        
        # 1. Finance
        html += f"""
            <h2>1. Financial Breakdown</h2>
            <div class='metric-box'>
                <strong>Revenue:</strong> ${float(metrics.get('revenue', 0)):,.2f}<br>
                <strong>Profit:</strong> ${float(metrics.get('profit', 0)):,.2f}<br>
                <strong>ROI:</strong> {float(metrics.get('roi', 0)):.2f}%
            </div>
        """
        
        # 2. Market
        m_data = metrics.get("market_analysis", {})
        html += f"""
            <h2>2. Market Analysis</h2>
            <div class='metric-box'>
                <strong>Growth:</strong> {self._strip_md(m_data.get('growth', ''))}<br>
                <strong>Competition:</strong> {self._strip_md(m_data.get('competition', ''))}<br>
                <strong>Demand:</strong> {self._strip_md(m_data.get('demand', ''))}<br>
                <strong>Opportunity:</strong> {self._strip_md(m_data.get('opportunity', ''))}<br>
                <strong>Confidence:</strong> {float(m_data.get('confidence', 0)):.1f}%
            </div>
        """
        
        # 3. Risk
        r_score = float(metrics.get("risk_score", 0))
        html += f"<h2>3. Risk Factors (Score: {r_score:.1f}/100)</h2><ul>"
        for factor in metrics.get("risk_analysis", {}).get("factors", []):
            html += f"<li>{self._strip_md(factor)}</li>"
        html += "</ul>"
        
        # Page Break for layout
        html += "<div class='page-break'></div>"
        
        # 4. Predictions
        html += "<h2>4. Predictive Models (6 Months)</h2>"
        preds = metrics.get("predictions", {})
        if isinstance(preds, dict):
            html += "<table><tr><th>Scenario</th><th>6-Month Forecast</th></tr>"
            for sc_name, curve in preds.items():
                curve_str = " | ".join([f"${float(c):,.2f}" for c in curve])
                html += f"<tr><td><strong>{sc_name}</strong></td><td>{curve_str}</td></tr>"
            html += "</table>"
            
        # 5. Timeline
        html += "<h2>5. Implementation Timeline</h2><table><tr><th>Phase</th><th>Duration</th></tr>"
        for phase in metrics.get("timeline", []):
            html += f"<tr><td><strong>{self._strip_md(phase.get('name', ''))}</strong></td><td>{self._strip_md(phase.get('duration', ''))}</td></tr>"
        html += "</table>"
        
        # 6. Evidence
        html += "<h2>6. Evidence & Citations</h2>"
        for ev in metrics.get("evidence", []):
            html += f"<h3>{self._strip_md(ev.get('title', ''))}</h3><p>{self._strip_md(ev.get('description', ''))}</p>"
            
        # 7. Decision
        score = float(metrics.get("confidence", 0))
        rec = data.get("rationale", "")
        html += f"""
            <h2>7. Final Decision</h2>
            <div style='background: #e6f2ff; padding: 20px; border-left: 6px solid #00509e; border-radius: 5px; font-size: 1.1em;'>
                <strong>Score:</strong> {score:.1f}/100<br><br>
                <strong>Recommendation:</strong> {self._strip_md(rec)}
            </div>
        </body>
        </html>
        """
        return html.encode("utf-8")

    def generate_pdf(self, data):
        try:
            from fpdf import FPDF
            from fpdf.enums import XPos, YPos
            
            metrics = data.get("metrics", {}) if isinstance(data, dict) else {}
            
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Helvetica", "B", 18)
            pdf.cell(0, 12, "RealityLab AI - Analysis Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            pdf.ln(8)
            
            def safe_str(s):
                return str(s).encode('latin-1', 'replace').decode('latin-1')

            # Decision
            score = float(metrics.get("confidence", 0))
            rec = data.get("rationale", "")
                
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_fill_color(230, 242, 255)
            pdf.multi_cell(0, 10, safe_str(f"Final Decision: {self._strip_md(rec)} (Score: {score:.1f}/100)"), fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(8)
            
            # Helper function for sections
            def add_section_header(title):
                pdf.set_font("Helvetica", "B", 14)
                pdf.set_text_color(0, 51, 102)
                pdf.cell(0, 10, safe_str(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.line(pdf.get_x(), pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
                pdf.ln(4)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Helvetica", "", 11)
                
            # Finance
            add_section_header("1. Financial Breakdown")
            pdf.cell(0, 6, safe_str(f"Revenue: ${float(metrics.get('revenue', 0)):,.2f}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 6, safe_str(f"Profit: ${float(metrics.get('profit', 0)):,.2f}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 6, safe_str(f"ROI: {float(metrics.get('roi', 0)):.2f}%"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(8)
            
            # Market
            add_section_header("2. Market Analysis")
            m_data = metrics.get("market_analysis", {})
            pdf.multi_cell(0, 6, safe_str(f"Projected Growth: {self._strip_md(m_data.get('growth', ''))}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(0, 6, safe_str(f"Competition Level: {self._strip_md(m_data.get('competition', ''))}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(0, 6, safe_str(f"Demand: {self._strip_md(m_data.get('demand', ''))}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(0, 6, safe_str(f"Market Opportunity: {self._strip_md(m_data.get('opportunity', ''))}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(0, 6, safe_str(f"Confidence: {float(m_data.get('confidence', 0)):.1f}%"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(8)
            
            # Risk
            add_section_header("3. Risk Factors")
            pdf.cell(0, 6, safe_str(f"Risk Score: {float(metrics.get('risk_score', 0)):.1f}/100"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
            r_data = metrics.get("risk_analysis", {}).get("factors", [])
            for factor in r_data:
                factor_text = self._strip_md(factor)
                pdf.multi_cell(0, 6, safe_str(f"- {factor_text}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(8)
            
            # Prediction
            pdf.add_page() # Page break
            add_section_header("4. Predictive Models (6 Months)")
            preds = metrics.get("predictions", {})
            if isinstance(preds, dict) and preds:
                with pdf.table(text_align="LEFT") as table:
                    row = table.row()
                    row.cell("Scenario")
                    row.cell("6-Month Forecast")
                    for sc_name, curve in preds.items():
                        row = table.row()
                        row.cell(safe_str(sc_name))
                        pred_str = " | ".join([f"${float(p):,.2f}" for p in curve])
                        row.cell(safe_str(pred_str))
            elif isinstance(preds, list):
                pred_str = " | ".join([f"${float(p):,.2f}" if isinstance(p, (int, float)) else str(p) for p in preds])
                pdf.multi_cell(0, 6, safe_str(f"Forecasts: {pred_str}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(8)
            
            # Timeline
            add_section_header("5. Implementation Timeline")
            timeline = metrics.get("timeline", [])
            if timeline:
                with pdf.table(text_align="LEFT") as table:
                    row = table.row()
                    row.cell("Phase")
                    row.cell("Duration")
                    for phase in timeline:
                        phase_name = self._strip_md(phase.get('name', ''))
                        phase_dur = self._strip_md(phase.get('duration', ''))
                        row = table.row()
                        row.cell(safe_str(phase_name))
                        row.cell(safe_str(phase_dur))
            pdf.ln(8)
            
            # Evidence
            add_section_header("6. Evidence & Citations")
            evidence = metrics.get("evidence", [])
            for ev in evidence:
                ev_title = self._strip_md(ev.get('title', ''))
                ev_desc = self._strip_md(ev.get('description', ''))
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 6, safe_str(ev_title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("Helvetica", "", 11)
                pdf.multi_cell(0, 6, safe_str(ev_desc), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(4)
                
            import io
            buffer = io.BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            return buffer.read()
            
        except Exception as e:
            # Fallback if fpdf fails
            import traceback
            err = traceback.format_exc()
            return f"Error generating PDF: {err}".encode("utf-8")
