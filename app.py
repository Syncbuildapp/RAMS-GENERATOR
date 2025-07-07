import os, datetime, tempfile
from flask import Flask, request, send_file, abort
from fpdf import FPDF

app = Flask(__name__)

FIELD_MAP = [
    ("Job Name",         "job_name"),
    ("Site Address",     "site_address"),
    ("Contractor",       "contractor_name"),
    ("Work Description", "work_description"),
    ("Start Date",       "start_date"),
    ("End Date",         "end_date"),
    ("Hazards",          "hazards"),
    ("PPE Required",     "ppe_required"),
    ("Emergency Contact","emergency_contact"),
    ("Trade Type",       "trade_type")
]

def build_pdf(data: dict) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, "Risk Assessment & Method Statement", ln=1, align="C")
    pdf.ln(6)

    pdf.set_font("Arial", size=12)
    for label, key in FIELD_MAP:
        value = data.get(key, "")
        pdf.multi_cell(0, 8, f"{label}: {value}")
        pdf.ln(2)

    pdf.ln(4)
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    pdf.cell(0, 8, f"Generated: {ts}", ln=1)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    tmp.close()
    return tmp.name

@app.route("/generate-rams", methods=["POST"])
def generate_rams():
    if not request.is_json:
        abort(400, "Request must be JSON")
    data = request.get_json(force=True)
    pdf_path = build_pdf(data)
    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name="RAMS.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
