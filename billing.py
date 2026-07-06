import os
import datetime
import logging
from dataclasses import dataclass
from typing import List
from inventory import LowStockAlert

# ReportLab imports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
except ImportError:
    # We will raise a clear error or handle it during runtime imports
    pass

@dataclass
class DraftPurchaseOrder:
    po_id: str
    vendor: str
    sku: str
    name: str
    qty: int
    unit_cost: float
    total_cost: float


def generate_po_pdf(po: DraftPurchaseOrder, output_dir: str = "output_pos") -> str:
    """Generates a professional PDF Purchase Order and saves it to output_dir."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"{po.po_id}.pdf")
    
    # Check if reportlab is available
    try:
        import reportlab
    except ImportError:
        logging.warning("reportlab is not installed. PDF generation will write a text file stub for testing.")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"PURCHASE ORDER: {po.po_id}\n")
            f.write(f"Vendor: {po.vendor}\n")
            f.write(f"SKU: {po.sku} ({po.name})\n")
            f.write(f"Quantity: {po.qty}\n")
            f.write(f"Unit Cost: ${po.unit_cost:.2f}\n")
            f.write(f"Total Cost: ${po.total_cost:.2f}\n")
        return file_path

    doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'POTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1F2733'),
        spaceAfter=15
    )
    
    body_style = ParagraphStyle(
        'POBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#161B22')
    )
    
    bold_style = ParagraphStyle(
        'POBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    # Title and Metadata
    story.append(Paragraph("PURCHASE ORDER", title_style))
    story.append(Spacer(1, 10))
    
    date_str = datetime.date.today().strftime("%B %d, %Y")
    
    meta_data = [
        [Paragraph(f"<b>PO Number:</b> {po.po_id}", body_style), Paragraph(f"<b>Date:</b> {date_str}", body_style)],
        [Paragraph(f"<b>Vendor:</b> {po.vendor}", body_style), Paragraph("<b>Ship To:</b> FinlyAI SME Store", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # Line Items Table
    headers = [
        Paragraph("<b>SKU</b>", bold_style),
        Paragraph("<b>Description</b>", bold_style),
        Paragraph("<b>Quantity</b>", bold_style),
        Paragraph("<b>Unit Price</b>", bold_style),
        Paragraph("<b>Total</b>", bold_style)
    ]
    
    row = [
        Paragraph(po.sku, body_style),
        Paragraph(po.name, body_style),
        Paragraph(str(po.qty), body_style),
        Paragraph(f"${po.unit_cost:.2f}", body_style),
        Paragraph(f"${po.total_cost:.2f}", body_style)
    ]
    
    table_data = [headers, row]
    
    # Add a subtotal/total row
    table_data.append([
        Paragraph("", body_style),
        Paragraph("", body_style),
        Paragraph("", body_style),
        Paragraph("<b>Total Amount:</b>", bold_style),
        Paragraph(f"<b>${po.total_cost:.2f}</b>", bold_style)
    ])
    
    po_table = Table(table_data, colWidths=[80, 200, 70, 90, 100])
    po_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ECE8DE')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,1), 0.5, colors.HexColor('#C9C3B4')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (3,2), (4,2), 1.5, colors.HexColor('#161B22')),
    ]))
    
    story.append(po_table)
    story.append(Spacer(1, 40))
    
    # Footer disclaimer
    story.append(Paragraph("<i>Note: This is an automatically generated purchase order drafted by FinlyAI. Pending final CFO approval.</i>", body_style))
    
    doc.build(story)
    return file_path


def draft_reorder_email_dry_run(po: DraftPurchaseOrder) -> str:
    """Drafts a reorder email using smtplib structures in dry-run mode, printing to stdout."""
    # Build MIME-like text for stdout display
    subject = f"Reorder Purchase Order - {po.po_id} - FinlyAI"
    to_email = f"sales@{po.vendor.lower().replace(' ', '').replace('.', '')}.com"
    from_email = "cfo@finlyai-sme.com"
    
    email_body = f"""From: {from_email}
To: {to_email}
Subject: {subject}
Date: {datetime.date.today().strftime("%a, %d %b %Y")}

Dear {po.vendor} Sales Team,

Please find attached Purchase Order {po.po_id} for the replenishment of our stock.

Order Details:
- SKU: {po.sku}
- Item: {po.name}
- Quantity: {po.qty}
- Unit Cost: ${po.unit_cost:.2f}
- Total Order Value: ${po.total_cost:.2f}

Please confirm receipt of this order and estimate delivery dates.

Best regards,
FinlyAI Virtual CFO Agent
(On behalf of FinlyAI SME Store)
"""
    
    print("\n--- [EMAIL DRY-RUN] Draft Email Compiled ---")
    print(email_body)
    print("-------------------------------------------\n")
    return email_body


def run_automated_billing(alerts: List[LowStockAlert]) -> List[DraftPurchaseOrder]:
    """Fragment 2 entrance point: generates purchase orders and email drafts for low stock alerts."""
    print("\n=== FRAGMENT 2: Automated Billing ===")
    if not alerts:
        print("No low-stock triggers received from Fragment 1. Nothing to draft.")
        return []

    print("Drafting vendor reorder purchase orders for triggered items...\n")
    drafts = []
    
    # Use current year/month/day as basis to avoid overlaps in PO sequences
    base_po_num = int(datetime.datetime.now().strftime("%y%m%d00"))
    
    for i, alert in enumerate(alerts, start=1):
        po = DraftPurchaseOrder(
            po_id=f"PO-{base_po_num + i}",
            vendor=alert.vendor,
            sku=alert.sku,
            name=alert.name,
            qty=alert.reorder_qty,
            unit_cost=alert.unit_cost,
            total_cost=alert.est_reorder_cost
        )
        drafts.append(po)
        
        # Generate the PDF
        file_path = generate_po_pdf(po)
        print(f"  Drafted {po.po_id}: {po.qty} x {po.name} from {po.vendor} -> ${po.total_cost:,.2f}")
        print(f"    Saved PDF to: {file_path}")
        
        # Draft email
        draft_reorder_email_dry_run(po)
        
    total = sum(p.total_cost for p in drafts)
    print(f"\n>> Fragment 2 complete: {len(drafts)} draft PO(s) created, total outflow ${total:,.2f} (pending CFO approval).")
    return drafts
