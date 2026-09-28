from pathlib import Path
import json, re, sys
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'source_documents'
OUT = Path(__file__).resolve().parent

FILES = {
 'approved': '00 PLANS/Approved Set/APPROVED-COS-001319.pdf',
 'approved_revision': '00 PLANS/APPROVED-COS-RV-001319-001.pdf',
 'permit_general': '00 PLANS/Permit_Pricing CDs 09.30.25/01 GENERAL_CSMC MOB 2_2025.09.29 - PERMIT SET.pdf',
 'permit_arch': '00 PLANS/Permit_Pricing CDs 09.30.25/03 ARCHITECTURAL_CSMC MOB 2_2025.09.29 - PERMIT SET.pdf',
 'rev5_arch': '00 PLANS/Revision 5/03 Architectural_CSMC MOB 2_REV 5 2026.02.27.pdf',
 'rev5_log': '00 PLANS/Revision 5/_00 REVISION LOG 2026.02.27_CSMC MOB 2_REV 05.pdf',
 'rev5_struct': '00 PLANS/Revision 5/04 Structural_CSMC MOB 2_REV 5 2026.02.27.pdf',
 'civil_approved': '00 PLANS/Approved Civil/APPROVED-LDCP-2025-00715.pdf',
 'civil_march': '00 PLANS/Revision 5/Rea Farms 2 - Civil Drawings 03.17.26.pdf',
 'civil_rev5': '00 PLANS/Revision 5/02 Civil & Landscape_CSMC MOB 2_REV 5 2026.02.12.pdf',
 'infrastructure_may': '00 PLANS/APPROVED Bulletin_REA FARMS INFRASTRUCTURE EXTENSION_2026-5-14.pdf',
 'civil_rtap1': '00 PLANS/APPROVED.CW-2024-00149_RTAP1.pdf',
 'civil_rtap3': '00 PLANS/APPROVED.CW-2024-00149_RTAP3.pdf',
 'testfit_level2': '00 PLANS/Test Fits/A122 - Level 2 Dimension Plan_r1.pdf',
 'testfit_june': '00 PLANS/Test Fits/ARCH_Dormie Equity Partners Carolina Sports MOB_Plan 20260625.pdf',
}

def extract():
    data = {}
    for key, relative in FILES.items():
        try:
            doc = pdfium.PdfDocument(str(SOURCE / relative))
            pages = []
            for i in range(len(doc)):
                page = doc[i]
                textpage = page.get_textpage()
                text = textpage.get_text_range()
                pages.append({'page': i+1, 'size': page.get_size(), 'text': text})
                textpage.close(); page.close()
            data[key] = {'path': relative, 'pages': pages}
            print(key, len(pages), 'pages', 'first page:', pages[0]['text'][:1600].replace('\r',''))
            doc.close()
        except Exception as e:
            data[key] = {'path': relative, 'error': str(e)}
            print(key, 'ERROR', str(e))
    with (OUT / 'extracted_text.json').open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def render(key, number, name=None, crop=None, width=2000):
    doc = pdfium.PdfDocument(str(SOURCE / FILES[key]))
    page = doc[number-1]
    w,h=page.get_size()
    # Crop fractions use visual image coordinates (left, top, right, bottom).
    scale=width / (w * ((crop[2]-crop[0]) if crop else 1))
    if crop:
        left,top,right,bottom=crop
        bitmap=page.render(scale=scale, crop=(w*left,h*(1-bottom),w*(1-right),h*top))
    else:
        bitmap=page.render(scale=scale)
    destination=OUT / ((name or f'{key}_p{number:03d}')+'.png')
    if destination.exists(): raise FileExistsError(destination)
    bitmap.to_pil().save(destination)
    print(destination)
    bitmap.close(); page.close(); doc.close()

if __name__=='__main__':
    if sys.argv[1]=='extract': extract()
    elif sys.argv[1]=='render':
        render(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv)>4 else None,
               tuple(map(float,sys.argv[5].split(','))) if len(sys.argv)>5 else None)
