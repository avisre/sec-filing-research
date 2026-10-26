#!/usr/bin/env python3
"""Render the editable paper.md into a standalone, selectable-text research PDF."""
from pathlib import Path
from functools import partial
import html,re
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT_DIR/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
styles={
 'body':ParagraphStyle('Body',fontName='Body',fontSize=10,leading=14.3,spaceAfter=8,textColor=colors.HexColor('#202a32')),
 'h1':ParagraphStyle('Title',fontName='SansBold',fontSize=22,leading=28,spaceAfter=16,textColor=colors.HexColor('#142c3c')),
 'h2':ParagraphStyle('Section',fontName='SansBold',fontSize=13.5,leading=18,spaceBefore=15,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#142c3c')),
 'h3':ParagraphStyle('Subsection',fontName='SansBold',fontSize=10.6,leading=14.5,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.HexColor('#203c4d')),
 'cell':ParagraphStyle('Cell',fontName='Sans',fontSize=8,leading=11,spaceAfter=0),
 'head':ParagraphStyle('Head',fontName='SansBold',fontSize=8,leading=11,textColor=colors.white),
 'bullet':ParagraphStyle('Bullet',fontName='Body',fontSize=9,leading=13,spaceAfter=6,leftIndent=10,firstLineIndent=-8),
}
styles['appendix']=ParagraphStyle('AppendixBody',parent=styles['body'],fontSize=9.5,leading=13,spaceAfter=6)
styles['snapshot']=ParagraphStyle('Snapshot',parent=styles['appendix'],keepWithNext=True)
styles['table_intro']=ParagraphStyle('TableIntro',parent=styles['body'],keepWithNext=True)
def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',lambda m:'<link href="'+m[2]+'" color="#235e7a">'+m[1]+'</link>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Sans">\1</font>',s)
    return s
def footer(c,doc):
    c.saveState();c.setFillColor(colors.HexColor('#64717c'));c.setFont('Sans',7.3)
    c.drawString(52,27,'StockPortfolio.pro | Research report v1.0')
    c.drawRightString(A4[0]-52,27,str(doc.page))
    if doc.page>1:
        c.setStrokeColor(colors.HexColor('#d6dce0'));c.line(52,A4[1]-38,A4[0]-52,A4[1]-38)
        c.drawString(52,A4[1]-30,'Why financial statement data goes missing')
    c.restoreState()
def main():
    text=(ROOT/'paper.md').read_text();lines=text.splitlines();story=[];i=0;appendix=False
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',v) for v in cells):rows.append(cells)
                i+=1
            width=A4[0]-104
            widths=([100,78,104,104,width-386] if len(rows[0])==5 else [137,63,width-200])
            data=[[Paragraph(inline(x),styles['head' if n==0 else 'cell']) for x in row] for n,row in enumerate(rows)]
            table=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#183749')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f4f6'),colors.white]),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#bac7d0'))]))
            story.extend([KeepTogether([table]),Spacer(1,10)]);continue
        if line.startswith('# '):kind='h1';body=line[2:]
        elif line.startswith('## '):
            kind='h2';body=line[3:]
            if body.startswith('Appendix'):
                appendix=True;story.append(PageBreak())
        elif line.startswith('### '):kind='h3';body=line[4:]
        elif line.startswith('- '):kind='bullet';body='• '+line[2:]
        else:
            kind='appendix' if appendix else 'body';body=line
            while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith(('#','|','- ')):
                i+=1;body+=' '+lines[i].strip()
        if body.startswith('Snapshot:'):kind='snapshot'
        if body.startswith('The 174,134'):kind='table_intro'
        story.append(Paragraph(inline(body),styles[kind]));i+=1
    pdf=ROOT/'financial-statement-coverage-audit.pdf'
    doc=SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=52,rightMargin=52,topMargin=52,bottomMargin=49,title='Why Financial Statement Data Goes Missing: A Reproducible SEC Filing Coverage Audit',author='Avinash Sreekumar',subject='Frozen product coverage audit and original SEC filing case studies')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=partial(canvas.Canvas,invariant=1))
    print(pdf)

if __name__=='__main__':main()
