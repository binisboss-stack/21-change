"""
Generate SL/TP Cheat Sheet PDF for XAUUSD
Output: sl_tp_cheatsheet.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

# ── Colors ────────────────────────────────────────────────────────────────────
BG        = colors.HexColor('#0f0f0f')
CARD      = colors.HexColor('#1a1a1a')
CARD2     = colors.HexColor('#252525')
YELLOW    = colors.HexColor('#facc15')
YELLOW_DIM= colors.HexColor('#3a3000')
GREEN     = colors.HexColor('#22c55e')
RED       = colors.HexColor('#ef4444')
ORANGE    = colors.HexColor('#f97316')
GRAY      = colors.HexColor('#888888')
WHITE     = colors.HexColor('#e5e5e5')
BORDER    = colors.HexColor('#333333')

W, H = A4  # 595 x 842 pt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sl_tp_cheatsheet.pdf')

def draw_rect(c, x, y, w, h, fill, radius=4, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.5)
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    else:
        c.setStrokeColor(fill)
        c.roundRect(x, y, w, h, radius, stroke=0, fill=1)

def text(c, txt, x, y, font='Helvetica-Bold', size=10, color=WHITE, align='left'):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == 'center':
        c.drawCentredString(x, y, txt)
    elif align == 'right':
        c.drawRightString(x, y, txt)
    else:
        c.drawString(x, y, txt)

def wrapped_text(c, txt, x, y, max_w, font='Helvetica', size=9, color=WHITE, leading=13):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = simpleSplit(txt, font, size, max_w)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y

def make_pdf():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle('Cheat Sheet: SL/TP XAUUSD — NEXUS VIP')

    PAD = 14 * mm
    CW  = W - 2 * PAD   # content width

    # ── Background ────────────────────────────────────────────────────────────
    draw_rect(c, 0, 0, W, H, BG, radius=0)

    # ── Top accent line ───────────────────────────────────────────────────────
    c.setFillColor(YELLOW)
    c.rect(0, H - 4, W, 4, stroke=0, fill=1)

    # ── Header ───────────────────────────────────────────────────────────────
    y = H - 20*mm
    text(c, 'NEXUS VIP', PAD, y, size=8, color=YELLOW)
    text(c, '— XAUUSD Signal Room', PAD + 42, y, font='Helvetica', size=8, color=GRAY)

    y -= 8*mm
    text(c, 'Cách đặt SL/TP cho XAUUSD', PAD, y, size=18, color=WHITE)
    y -= 7*mm
    text(c, 'Không cần phân tích phức tạp', PAD, y, font='Helvetica', size=11, color=YELLOW)
    y -= 5*mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(PAD, y, W - PAD, y)

    # ── Rule strip ────────────────────────────────────────────────────────────
    y -= 6*mm
    draw_rect(c, PAD, y - 8*mm, CW, 10*mm, YELLOW_DIM, radius=5, stroke=YELLOW)
    text(c, '3 QUY TẮC KHÔNG THƯƠNG LƯỢNG:', PAD + 4*mm, y - 3*mm, size=8, color=YELLOW)
    rules = '① SL theo thị trường, tính lot size sau    ② R:R tối thiểu 1:2    ③ Tính lot size TRƯỚC khi vào lệnh'
    text(c, rules, PAD + 4*mm, y - 6.5*mm, font='Helvetica', size=8, color=WHITE)

    # ── 3 Methods ─────────────────────────────────────────────────────────────
    y -= 18*mm
    COL = (CW - 2*4) / 3   # 3 equal columns, 4pt gap
    cols_x = [PAD, PAD + COL + 4, PAD + 2*(COL + 4)]

    method_data = [
        {
            'num': '01',
            'title': 'Structure',
            'sub': 'Swing high / low',
            'color': GREEN,
            'when': 'Chart có xu hướng rõ, khung H1–H4',
            'rule_sl': 'BUY: SL dưới đáy swing gần nhất − 2pip\nSELL: SL trên đỉnh swing gần nhất + 2pip',
            'rule_tp': 'TP tối thiểu = SL × 2  (R:R 1:2)',
            'example': 'VD: Entry Buy 2340, đáy swing 2330\n→ SL = 2328  |  TP = 2364',
            'badge': 'Chính xác nhất',
            'diff': 'Trung bình',
        },
        {
            'num': '02',
            'title': 'ATR ×1.5',
            'sub': 'Average True Range',
            'color': YELLOW,
            'when': 'Thị trường bình thường, không có news lớn',
            'rule_sl': 'SL = Entry ± (ATR × 1.5)',
            'rule_tp': 'TP = Entry ± (ATR × 3)',
            'example': 'VD: Entry Buy 2340, ATR(14)H1 = 5pip\n→ SL = 2332.5  |  TP = 2355',
            'badge': 'Có công thức',
            'diff': 'Dễ–TB',
        },
        {
            'num': '03',
            'title': 'Fixed Zone',
            'sub': 'Theo phiên GD',
            'color': ORANGE,
            'when': 'Mới bắt đầu, không có thời gian phân tích',
            'rule_sl': 'Asian:  SL 8–12pip\nLondon/NY:  SL 15–20pip\nOverlap:  SL 20–25pip',
            'rule_tp': 'TP = SL × 2',
            'example': 'VD: Phiên NY, vào Buy 2340\n→ SL 18pip = 2322  |  TP = 2358',
            'badge': 'Dễ nhất',
            'diff': 'Dễ',
        },
    ]

    card_h = 68 * mm
    for i, m in enumerate(method_data):
        x = cols_x[i]
        cy = y

        # Card background
        draw_rect(c, x, cy - card_h, COL, card_h, CARD, radius=6, stroke=BORDER)

        # Top color bar
        c.setFillColor(m['color'])
        c.roundRect(x, cy - 5*mm, COL, 5*mm, 5, stroke=0, fill=1)
        c.setFillColor(CARD)
        c.rect(x, cy - 5*mm, COL, 2.5*mm, stroke=0, fill=1)

        # Number + Title
        text(c, m['num'], x + 3*mm, cy - 4*mm, size=8, color=CARD)
        text(c, m['title'], x + 10*mm, cy - 4*mm, size=9, color=CARD)

        iy = cy - 9*mm
        text(c, m['sub'], x + 3*mm, iy, font='Helvetica', size=8, color=GRAY)

        # Badge
        bw = 24*mm
        draw_rect(c, x + COL - bw - 2*mm, iy - 1*mm, bw, 5*mm, m['color'], radius=3)
        text(c, m['badge'], x + COL - bw/2 - 2*mm, iy + 0.5*mm, size=7, color=CARD, align='center')

        iy -= 6*mm
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(x + 3*mm, iy, x + COL - 3*mm, iy)

        iy -= 5*mm
        text(c, 'KHI NÀO DÙNG:', x + 3*mm, iy, size=7, color=GRAY)
        iy -= 4*mm
        iy = wrapped_text(c, m['when'], x + 3*mm, iy, COL - 6*mm, size=8, leading=11)

        iy -= 3*mm
        text(c, 'CÔNG THỨC SL:', x + 3*mm, iy, size=7, color=GRAY)
        iy -= 4*mm
        iy = wrapped_text(c, m['rule_sl'], x + 3*mm, iy, COL - 6*mm, size=8, leading=11)

        iy -= 3*mm
        text(c, 'CÔNG THỨC TP:', x + 3*mm, iy, size=7, color=GRAY)
        iy -= 4*mm
        iy = wrapped_text(c, m['rule_tp'], x + 3*mm, iy, COL - 6*mm, size=8, leading=11)

        iy -= 3*mm
        draw_rect(c, x + 2*mm, iy - 10*mm, COL - 4*mm, 12*mm, CARD2, radius=3)
        iy -= 3*mm
        iy = wrapped_text(c, m['example'], x + 4*mm, iy, COL - 8*mm,
                          font='Helvetica', size=7.5, color=m['color'], leading=10)

    # ── Lot Size Formula ──────────────────────────────────────────────────────
    y -= (card_h + 6*mm)
    draw_rect(c, PAD, y - 22*mm, CW, 24*mm, CARD, radius=6, stroke=BORDER)
    text(c, 'CÔNG THỨC TÍNH LOT SIZE', PAD + 4*mm, y - 4*mm, size=9, color=YELLOW)

    formula_x = PAD + 4*mm
    text(c, 'Lot = (Vốn × % Rủi ro)  ÷  (SL theo pip × Pip value)',
         formula_x, y - 9*mm, font='Helvetica-Bold', size=9.5, color=WHITE)

    text(c, 'Pip value XAUUSD ≈ $1/pip với 0.1 lot   |   Rủi ro tối đa mỗi lệnh: 1–2% tài khoản',
         formula_x, y - 13.5*mm, font='Helvetica', size=8, color=GRAY)

    # Example boxes
    ex_data = [
        ('Vốn $500, SL 15pip, rủi ro 2%', '$500 × 2% = $10   →   $10 ÷ 15 = 0.07 lot'),
        ('Vốn $1000, SL 20pip, rủi ro 2%', '$1000 × 2% = $20   →   $20 ÷ 20 = 0.1 lot'),
        ('Vốn $2000, SL 20pip, rủi ro 1%', '$2000 × 1% = $20   →   $20 ÷ 20 = 0.1 lot'),
    ]
    ex_w = (CW - 2*4*mm) / 3
    for i, (label, result) in enumerate(ex_data):
        ex_x = PAD + i * (ex_w + 2*mm)
        draw_rect(c, ex_x + 4*mm, y - 20.5*mm, ex_w - 4*mm, 8*mm, CARD2, radius=3)
        text(c, label, ex_x + 5.5*mm, y - 17*mm, font='Helvetica', size=7, color=GRAY)
        text(c, result, ex_x + 5.5*mm, y - 20*mm, font='Helvetica-Bold', size=7.5, color=GREEN)

    # ── ATR Reference Table ───────────────────────────────────────────────────
    y -= 30*mm
    draw_rect(c, PAD, y - 22*mm, CW * 0.48, 24*mm, CARD, radius=6, stroke=BORDER)
    text(c, 'ATR XAUUSD THAM KHẢO', PAD + 4*mm, y - 4*mm, size=8, color=YELLOW)

    atr_rows = [
        ('Khung', 'ATR(14) thường', 'SL gợi ý', 'TP gợi ý'),
        ('H1',   '3–8 pip',        '5–12 pip', '10–24 pip'),
        ('H4',   '15–25 pip',      '22–37 pip','44–75 pip'),
        ('D1',   '80–150 pip',     '120–225p', '240–450p'),
    ]
    col_w = [CW * 0.48 / 4 - 2] * 4
    row_colors = [CARD2, CARD, CARD2, CARD]
    for ri, row in enumerate(atr_rows):
        ry = y - 7*mm - ri * 4*mm
        for ci, cell in enumerate(row):
            cx = PAD + 4*mm + ci * (CW * 0.48 / 4)
            fc = WHITE if ri == 0 else (GRAY if ci == 0 else WHITE)
            fs = 7 if ri == 0 else 7.5
            fn = 'Helvetica-Bold' if ri == 0 else 'Helvetica'
            text(c, cell, cx, ry, font=fn, size=fs, color=fc)

    # ── Session Table ─────────────────────────────────────────────────────────
    sx = PAD + CW * 0.48 + 4*mm
    sw = CW * 0.52 - 4*mm
    draw_rect(c, sx, y - 22*mm, sw, 24*mm, CARD, radius=6, stroke=BORDER)
    text(c, 'FIXED ZONE THEO PHIÊN', sx + 4*mm, y - 4*mm, size=8, color=YELLOW)

    session_rows = [
        ('Phiên', 'Giờ VN', 'SL pip', 'TP pip'),
        ('Asian',         '6h–15h',  '8–12',  '16–24'),
        ('London',        '15h–21h', '15–20', '30–40'),
        ('New York',      '20h–1h',  '15–20', '30–40'),
        ('Overlap L+NY',  '20h–21h', '20–25', '40–50'),
    ]
    for ri, row in enumerate(session_rows):
        ry = y - 7*mm - ri * 3.6*mm
        for ci, cell in enumerate(row):
            cx = sx + 4*mm + ci * (sw / 4)
            fc = WHITE if ri == 0 else (GRAY if ci <= 1 else WHITE)
            fs = 7 if ri == 0 else 7.5
            fn = 'Helvetica-Bold' if ri == 0 else 'Helvetica'
            text(c, cell, cx, ry, font=fn, size=fs, color=fc)

    # ── Red flags ─────────────────────────────────────────────────────────────
    y -= 30*mm
    draw_rect(c, PAD, y - 16*mm, CW, 18*mm, colors.HexColor('#1f0a0a'), radius=6, stroke=RED)
    text(c, '⚠  KHÔNG VÀO LỆNH KHI:', PAD + 4*mm, y - 4*mm, size=9, color=RED)

    flags = [
        '❌  15 phút trước / sau NFP, CPI, Fed meeting',
        '❌  Không xác định được xu hướng D1',
        '❌  ATR đột biến > 2 lần mức bình thường',
        '❌  Chưa tính lot size',
    ]
    fx = PAD + 4*mm
    fy = y - 8.5*mm
    half = len(flags) // 2
    for i, f in enumerate(flags):
        col_offset = 0 if i < half else CW / 2
        row = i if i < half else i - half
        text(c, f, fx + col_offset, fy - row * 4*mm,
             font='Helvetica', size=8, color=WHITE)

    # ── Footer ────────────────────────────────────────────────────────────────
    y = 12*mm
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(PAD, y + 4*mm, W - PAD, y + 4*mm)
    text(c, 'NEXUS VIP — Room tín hiệu XAUUSD', PAD, y, font='Helvetica', size=7.5, color=GRAY)
    text(c, 'www.tiemhoatmon.com', W/2, y, font='Helvetica', size=7.5, color=YELLOW, align='center')
    text(c, 'Winrate 82% | Hoàn tiền 30 ngày', W - PAD, y, font='Helvetica', size=7.5, color=GRAY, align='right')

    c.save()
    print(f'PDF saved: {OUT}')

if __name__ == '__main__':
    make_pdf()
