import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit


def collect_files_by_extension(root_folder):
    """Collects files by extension type and returns sorted lists."""
    xml_files, java_files, jsp_files = [], [], []

    for folder, _, files in os.walk(root_folder):
        for file in files:
            path = os.path.join(folder, file)
            if file.endswith(".xml"):
                xml_files.append(path)
            elif file.endswith(".java"):
                java_files.append(path)
            elif file.endswith(".jsp"):
                jsp_files.append(path)

    return xml_files, java_files, jsp_files


def write_files_to_pdf(file_paths, pdf_canvas, start_y, label):
    """Writes the given list of files into the PDF."""
    width, height = A4
    x_margin, y_margin = inch * 0.5, inch * 0.5
    y_position = start_y

    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(x_margin, y_position, f"=== {label} FILES ===")
    y_position -= 20

    for file_path in file_paths:
        # Print file path
        pdf_canvas.setFont("Helvetica-Bold", 11)
        pdf_canvas.drawString(x_margin, y_position, file_path)
        y_position -= 15

        # Read content safely
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            content = f"[Error reading file: {e}]"

        # Write content line by line
        pdf_canvas.setFont("Courier", 9)
        wrapped_text = simpleSplit(content, "Courier", 9, width - 2 * x_margin)
        for line in wrapped_text:
            if y_position <= y_margin:
                pdf_canvas.showPage()
                pdf_canvas.setFont("Courier", 9)
                y_position = height - y_margin
            pdf_canvas.drawString(x_margin, y_position, line)
            y_position -= 11

        # Separator line
        y_position -= 10
        pdf_canvas.setFont("Helvetica-Oblique", 10)
        pdf_canvas.drawString(x_margin, y_position, "-" * 90)
        y_position -= 20

        # Create new page if needed
        if y_position <= y_margin:
            pdf_canvas.showPage()
            y_position = height - y_margin

    return y_position


def write_code_files_to_pdf(root_folder, output_pdf):
    """Main function to create the PDF with .xml, .java, and .jsp files."""
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    y_start = height - inch * 0.5

    xml_files, java_files, jsp_files = collect_files_by_extension(root_folder)

    print(f" Found {len(xml_files)} XML, {len(java_files)} Java, {len(jsp_files)} JSP files.")

    # Write in given order
    y_pos = write_files_to_pdf(xml_files, c, y_start, "XML")
    y_pos = write_files_to_pdf(java_files, c, y_pos, "JAVA")
    write_files_to_pdf(jsp_files, c, y_pos, "JSP")

    c.save()
    print(f" PDF created successfully: {output_pdf}")


if __name__ == "__main__":
    root_folder = input("Enter the root folder path: ").strip()
    output_pdf = input("Enter output PDF filename (e.g., combined_files.pdf): ").strip()
    if not output_pdf.endswith(".pdf"):
        output_pdf += ".pdf"
    write_code_files_to_pdf(root_folder, output_pdf)
