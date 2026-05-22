"""
Admin panel server for brain.db
Run: python admin_server.py
Then open: http://localhost:5000/admin
"""
import sqlite3
import os
import threading
import resend
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, abort

# ── Resend config ────────────────────────────────────────────────────────────

_resend_key = os.environ.get('RESEND_API_KEY', '')
if not _resend_key:
    _resend_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resend_config.txt')
    try:
        with open(_resend_key_path) as _f:
            _resend_key = _f.read().strip()
    except FileNotFoundError:
        pass

if _resend_key:
    resend.api_key = _resend_key
    RESEND_ENABLED = True
    print('[Resend] API key loaded OK')
else:
    RESEND_ENABLED = False
    print('[Resend] No API key found — email disabled')

RESEND_FROM = os.environ.get('RESEND_FROM', 'onboarding@resend.dev')
SITE_URL = os.environ.get('SITE_URL', 'https://www.tiemhoatmon.com')


def _html(name, subject_line, body_paragraphs):
    body = ''.join(f'<p style="margin:0 0 16px">{p}</p>' for p in body_paragraphs)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{subject_line}</title></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:32px 0">
<tr><td align="center">
<table width="560" cellpadding="0" cellspacing="0"
  style="background:#fff;border-radius:8px;padding:40px;max-width:560px">
<tr><td style="font-size:15px;line-height:1.7;color:#222">
<p style="margin:0 0 8px;font-size:12px;color:#888;letter-spacing:1px">NEXUS VIP GROUP</p>
{body}
<hr style="border:none;border-top:1px solid #eee;margin:32px 0">
<p style="font-size:12px;color:#aaa;margin:0">
Bạn nhận được email này vì đã đăng ký tại tiemhoatmon.com.<br>
Nhắn Zalo hoặc reply email này nếu cần hỗ trợ.
</p>
</td></tr></table>
</td></tr></table>
</body></html>"""


def _email1(name):
    subject = f'Chào {name} — mình nhận được thông tin rồi 👋'
    html = _html(name, subject, [
        f'Ê {name},',
        'Mình vừa nhận được đăng ký của bạn rồi.',
        'Đội ngũ sẽ liên hệ lại trong 1 tiếng — qua Zalo hoặc điện thoại — để xác nhận slot và hướng dẫn bước tiếp theo.',
        'Trong lúc chờ, có 1 thứ bạn nên biết:',
        'Ý là, 80% người trade XAUUSD thua không phải vì phân tích sai — mà vì không có điểm cắt lỗ rõ ràng. Mình sẽ gửi bạn cái này trong 2 ngày tới.',
        '— NEXUS VIP',
    ])
    return subject, html


def _email2(name):
    subject = 'Tại sao 90% trader mất tiền — không phải vì chọn sai lệnh'
    html = _html(name, subject, [
        f'Ê {name},',
        'Mình hỏi thật: bạn đã bao giờ vào đúng hướng nhưng vẫn bị stop out chưa?',
        'Giá đi ngược một chút, chạm SL, rồi quay về đúng hướng mình đoán. Bực không?',
        'Đây là lý do: SL đặt quá gần. Thị trường luôn có nhiễu ngắn hạn trước khi đi đúng hướng. Nếu SL không đủ "thở", lệnh chết trước khi kịp thắng.',
        'Ví dụ như là: XAUUSD trên khung H1, biên độ dao động trung bình mỗi nến là 5–8 pip. SL tối thiểu nên cách entry 12–15 pip — dưới đó là đặt bẫy cho chính mình.',
        '<strong>Quy tắc đơn giản:</strong><br>1. SL đặt dưới đáy swing gần nhất (không phải dưới entry)<br>2. TP ít nhất gấp đôi SL (R:R tối thiểu 1:2)<br>3. Tính lot size SAU KHI có SL — không phải trước',
        'Vậy thì sao? Ý là dù thị trường sai, bạn vẫn kiểm soát được mình mất bao nhiêu.',
        'Ngày mai mình sẽ gửi thêm 1 thứ nữa.',
        '— NEXUS VIP',
    ])
    return subject, html


def _email3(name):
    subject = 'Còn 7 suất — Room VIP đang mở'
    html = _html(name, subject, [
        f'Ê {name},',
        'Hôm qua mình nói về SL/TP.',
        'Nhưng biết quy tắc và có người nhắc bạn áp dụng đúng mỗi ngày — là 2 thứ khác nhau hoàn toàn.',
        'NEXUS VIP GROUP đang mở thêm 1 đợt nhỏ — tối đa 50 thành viên để đảm bảo chất lượng tín hiệu không bị loãng.',
        '<strong>Bạn nhận được:</strong><br>'
        '• Tín hiệu XAUUSD real-time, ghi rõ Entry + TP + SL — copy vào app là xong<br>'
        '• Nhận trước 9h tối, không cần thức khuya<br>'
        '• Khoá học F0 kèm theo (video, có cheat sheet)<br>'
        '• Buổi review danh mục 1-1 mỗi tháng<br>'
        '• Hoàn tiền 100% trong 30 ngày nếu không hài lòng — không hỏi lý do',
        'Winrate 82% qua cả chu kỳ bull & bear — có lịch sử lệnh thật để bạn tự kiểm chứng.',
        f'<a href="{SITE_URL}/thanh-toan.html" '
        f'style="display:inline-block;background:#f5a623;color:#000;padding:12px 28px;'
        f'border-radius:6px;text-decoration:none;font-weight:bold;margin:8px 0">'
        f'👉 Đăng ký ngay</a>',
        'Hoặc nhắn Zalo để hỏi trước khi quyết định — không ai thúc ép gì cả.',
        '— NEXUS VIP',
    ])
    return subject, html


def _send(to_email, subject, html_body):
    if not RESEND_ENABLED:
        print(f'[Resend] DISABLED — would send "{subject}" to {to_email}')
        return
    try:
        resend.Emails.send({
            'from': RESEND_FROM,
            'to': [to_email],
            'subject': subject,
            'html': html_body,
        })
        print(f'[Resend] OK Sent "{subject}" to {to_email}')
    except Exception as exc:
        print(f'[Resend] ERROR sending to {to_email}: {exc}')


def _after(seconds, fn, *args):
    t = threading.Timer(seconds, fn, args=args)
    t.daemon = True
    t.start()


def trigger_email_sequence(email, name):
    is_test = '+test' in email.lower()
    # Resend chỉ nhận exact email — bỏ phần +alias khi gửi
    send_to = email.lower().replace('+test', '') if is_test else email
    d2 = 5 if is_test else 2 * 24 * 3600    # 5 giây hoặc 2 ngày
    d3 = 12 if is_test else 3 * 24 * 3600   # 12 giây hoặc 3 ngày

    s1, h1 = _email1(name)
    _send(send_to, s1, h1)

    s2, h2 = _email2(name)
    _after(d2, _send, send_to, s2, h2)

    s3, h3 = _email3(name)
    _after(d3, _send, send_to, s3, h3)

    mode = 'TEST (cả 3 email gửi ngay)' if is_test else 'LIVE (email 2 sau 2 ngày, email 3 sau 3 ngày)'
    print(f'[Resend] Sequence triggered for {email} — {mode}')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_data_dir = os.environ.get('DATA_DIR', BASE_DIR)
DB_PATH = os.path.join(_data_dir, 'brain.db')
ADMIN_DIR = os.path.join(BASE_DIR, 'admin')

app = Flask(__name__)


def init_db():
    os.makedirs(_data_dir, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                name             TEXT    NOT NULL,
                price            INTEGER NOT NULL DEFAULT 0,
                description      TEXT,
                slots_remaining  INTEGER DEFAULT NULL,
                is_active        INTEGER DEFAULT 1,
                created_at       TEXT
            );
            CREATE TABLE IF NOT EXISTS customers (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                phone         TEXT UNIQUE,
                zalo          TEXT,
                email         TEXT,
                service       TEXT DEFAULT '',
                source        TEXT DEFAULT 'website',
                registered_at TEXT,
                note          TEXT
            );
            CREATE TABLE IF NOT EXISTS orders (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id  INTEGER NOT NULL REFERENCES customers(id),
                product_id   INTEGER NOT NULL REFERENCES products(id),
                amount       INTEGER NOT NULL DEFAULT 0,
                status       TEXT NOT NULL DEFAULT 'pending',
                payment_ref  TEXT,
                ordered_at   TEXT,
                paid_at      TEXT,
                note         TEXT
            );
        """)
        conn.commit()


@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return '', 204


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def row_to_dict(row):
    return dict(row) if row else None


# ── Serve admin UI ──────────────────────────────────────────────────────────

@app.route('/')
def root():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:filename>')
def root_static(filename):
    # Don't catch /admin or /api routes
    if filename.startswith('admin') or filename.startswith('api'):
        abort(404)
    return send_from_directory(BASE_DIR, filename)


@app.route('/admin')
@app.route('/admin/')
def admin_index():
    return send_from_directory(ADMIN_DIR, 'index.html')


@app.route('/admin/<path:filename>')
def admin_static(filename):
    return send_from_directory(ADMIN_DIR, filename)


# ── Products ────────────────────────────────────────────────────────────────

@app.route('/api/products', methods=['GET'])
def list_products():
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM products ORDER BY id').fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@app.route('/api/products', methods=['POST'])
def create_product():
    d = request.json or {}
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_db() as conn:
        cur = conn.execute(
            'INSERT INTO products (name, price, description, slots_remaining, is_active, created_at) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (d.get('name', ''), int(d.get('price', 0)), d.get('description', ''),
             int(d.get('slots_remaining', 0)), int(d.get('is_active', 1)), now)
        )
        conn.commit()
        row = conn.execute('SELECT * FROM products WHERE id=?', (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@app.route('/api/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    d = request.json or {}
    with get_db() as conn:
        conn.execute(
            'UPDATE products SET name=?, price=?, description=?, slots_remaining=?, is_active=? WHERE id=?',
            (d.get('name'), int(d.get('price', 0)), d.get('description'),
             int(d.get('slots_remaining', 0)), int(d.get('is_active', 1)), pid)
        )
        conn.commit()
        row = conn.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
    if not row:
        abort(404)
    return jsonify(row_to_dict(row))


@app.route('/api/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    with get_db() as conn:
        conn.execute('DELETE FROM products WHERE id=?', (pid,))
        conn.commit()
    return jsonify({'ok': True})


# ── Customers ───────────────────────────────────────────────────────────────

@app.route('/api/customers', methods=['GET'])
def list_customers():
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM customers ORDER BY id DESC').fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@app.route('/api/customers', methods=['POST'])
def create_customer():
    d = request.json or {}
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with get_db() as conn:
            cur = conn.execute(
                'INSERT INTO customers (name, phone, zalo, email, service, source, registered_at, note) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (d.get('name', ''), d.get('phone', ''), d.get('zalo', ''),
                 d.get('email', ''), d.get('service', ''),
                 d.get('source', 'admin'), now, d.get('note', ''))
            )
            customer_id = cur.lastrowid
            # Auto-create pending order for website registrations
            if d.get('source') == 'website' and d.get('service'):
                product = conn.execute(
                    "SELECT * FROM products WHERE name LIKE ? AND is_active=1 LIMIT 1",
                    ('%' + d.get('service') + '%',)
                ).fetchone()
                if product:
                    conn.execute(
                        'INSERT INTO orders (customer_id, product_id, amount, status, payment_ref, ordered_at, note) '
                        'VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (customer_id, product['id'], product['price'], 'pending', '', now, 'Đăng ký từ website')
                    )
                    conn.execute(
                        'UPDATE products SET slots_remaining = MAX(0, slots_remaining - 1) WHERE id=?',
                        (product['id'],)
                    )
            conn.commit()
            row = conn.execute('SELECT * FROM customers WHERE id=?', (customer_id,)).fetchone()
        # Gửi email sequence nếu có địa chỉ email
        if d.get('email'):
            threading.Thread(
                target=trigger_email_sequence,
                args=(d['email'], d.get('name', 'bạn')),
                daemon=True
            ).start()
        return jsonify(row_to_dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Số điện thoại đã tồn tại'}), 409


@app.route('/api/customers/<int:cid>', methods=['PUT'])
def update_customer(cid):
    d = request.json or {}
    try:
        with get_db() as conn:
            conn.execute(
                'UPDATE customers SET name=?, phone=?, zalo=?, email=?, service=?, source=?, note=? WHERE id=?',
                (d.get('name'), d.get('phone'), d.get('zalo'),
                 d.get('email'), d.get('service'), d.get('source'), d.get('note'), cid)
            )
            conn.commit()
            row = conn.execute('SELECT * FROM customers WHERE id=?', (cid,)).fetchone()
        if not row:
            abort(404)
        return jsonify(row_to_dict(row))
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Số điện thoại đã tồn tại'}), 409


@app.route('/api/customers/<int:cid>', methods=['DELETE'])
def delete_customer(cid):
    with get_db() as conn:
        conn.execute('DELETE FROM customers WHERE id=?', (cid,))
        conn.commit()
    return jsonify({'ok': True})


# ── Orders ──────────────────────────────────────────────────────────────────

@app.route('/api/orders', methods=['GET'])
def list_orders():
    with get_db() as conn:
        rows = conn.execute('''
            SELECT o.*, c.name AS customer_name, c.phone AS customer_phone,
                   p.name AS product_name
            FROM orders o
            LEFT JOIN customers c ON c.id = o.customer_id
            LEFT JOIN products p ON p.id = o.product_id
            ORDER BY o.id DESC
        ''').fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@app.route('/api/orders', methods=['POST'])
def create_order():
    d = request.json or {}
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_db() as conn:
        product = conn.execute('SELECT * FROM products WHERE id=?', (d.get('product_id'),)).fetchone()
        if not product:
            return jsonify({'error': 'Không tìm thấy sản phẩm'}), 404
        if product['slots_remaining'] is not None and product['slots_remaining'] <= 0:
            return jsonify({'error': 'Sản phẩm đã hết slot'}), 400

        cur = conn.execute(
            'INSERT INTO orders (customer_id, product_id, amount, status, payment_ref, ordered_at, note) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (int(d.get('customer_id', 0)), int(d.get('product_id', 0)),
             int(d.get('amount', 0)), d.get('status', 'pending'),
             d.get('payment_ref', ''), now, d.get('note', ''))
        )
        # Decrement slots
        conn.execute(
            'UPDATE products SET slots_remaining = MAX(0, slots_remaining - 1) WHERE id=?',
            (d.get('product_id'),)
        )
        conn.commit()
        order_row = conn.execute('''
            SELECT o.*, c.name AS customer_name, c.email AS customer_email,
                   p.name AS product_name
            FROM orders o
            LEFT JOIN customers c ON c.id = o.customer_id
            LEFT JOIN products p ON p.id = o.product_id
            WHERE o.id=?
        ''', (cur.lastrowid,)).fetchone()
    row = order_row
    # Gửi email xác nhận đơn hàng
    if row and row['customer_email']:
        cname = row['customer_name'] or 'bạn'
        pname = row['product_name'] or 'Sản phẩm'
        amount_fmt = f"{int(row['amount']):,}".replace(',', '.')
        confirm_subject = f'Xác nhận đơn hàng — {pname}'
        confirm_html = _html(cname, confirm_subject, [
            f'Ê {cname},',
            f'Đơn hàng của bạn đã được xác nhận.',
            f'<strong>Sản phẩm:</strong> {pname}<br><strong>Số tiền:</strong> {amount_fmt}đ',
            'Bước tiếp theo: đội ngũ sẽ liên hệ qua Zalo trong vòng 1 tiếng để gửi link vào group và tài liệu khoá học.',
            'Nếu chưa thấy ai liên hệ sau 2 tiếng — nhắn thẳng vào Zalo để được hỗ trợ ngay.',
            'Cảm ơn bạn đã tin tưởng. Mình sẽ không làm bạn thất vọng.',
            '— NEXUS VIP',
        ])
        threading.Thread(
            target=_send,
            args=(row['customer_email'], confirm_subject, confirm_html),
            daemon=True
        ).start()
    return jsonify(row_to_dict(row)), 201


@app.route('/api/orders/<int:oid>', methods=['PUT'])
def update_order(oid):
    d = request.json or {}
    paid_at = d.get('paid_at')
    if d.get('status') == 'paid' and not paid_at:
        paid_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_db() as conn:
        conn.execute(
            'UPDATE orders SET customer_id=?, product_id=?, amount=?, status=?, payment_ref=?, paid_at=?, note=? WHERE id=?',
            (int(d.get('customer_id', 0)), int(d.get('product_id', 0)),
             int(d.get('amount', 0)), d.get('status'), d.get('payment_ref'),
             paid_at, d.get('note'), oid)
        )
        conn.commit()
        row = conn.execute('''
            SELECT o.*, c.name AS customer_name, p.name AS product_name
            FROM orders o
            LEFT JOIN customers c ON c.id = o.customer_id
            LEFT JOIN products p ON p.id = o.product_id
            WHERE o.id=?
        ''', (oid,)).fetchone()
    if not row:
        abort(404)
    return jsonify(row_to_dict(row))


@app.route('/api/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    with get_db() as conn:
        order = conn.execute('SELECT * FROM orders WHERE id=?', (oid,)).fetchone()
        if order:
            # Restore slot on delete
            conn.execute(
                'UPDATE products SET slots_remaining = slots_remaining + 1 WHERE id=?',
                (order['product_id'],)
            )
        conn.execute('DELETE FROM orders WHERE id=?', (oid,))
        conn.commit()
    return jsonify({'ok': True})


# ── Sepay Webhook ────────────────────────────────────────────────────────────

SEPAY_IPS = {
    '172.236.138.20', '172.233.83.68', '171.244.35.2',
    '151.158.108.68', '151.158.109.79', '103.255.238.139'
}

@app.route('/webhook/sepay', methods=['POST'])
def sepay_webhook():
    data = request.get_json(silent=True) or {}

    transfer_type   = data.get('transferType', '')
    amount          = int(data.get('transferAmount', 0))
    content         = (data.get('content') or data.get('description') or '').strip()
    transaction_id  = str(data.get('id', ''))
    transaction_date= data.get('transactionDate', '')

    # Chỉ xử lý giao dịch tiền vào
    if transfer_type != 'in' or amount <= 0:
        return jsonify({'success': True})

    # Tìm khách hàng theo nội dung CK: "NEXUSVIP <tên>"
    customer_name = None
    if 'NEXUSVIP' in content.upper():
        parts = content.upper().split('NEXUSVIP', 1)
        if len(parts) > 1:
            customer_name = parts[1].strip()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with get_db() as conn:
        customer_id = None

        if customer_name:
            row = conn.execute(
                "SELECT id FROM customers WHERE LENGTH(name) > 2 AND ? LIKE '%' || UPPER(name) || '%'",
                (customer_name,)
            ).fetchone()
            if row:
                customer_id = row['id']

        # Tìm đơn hàng pending của khách (nếu có) và cập nhật thành paid
        if customer_id:
            pending_order = conn.execute(
                "SELECT id FROM orders WHERE customer_id=? AND status='pending' ORDER BY id DESC LIMIT 1",
                (customer_id,)
            ).fetchone()

            if pending_order:
                conn.execute(
                    "UPDATE orders SET status='paid', paid_at=?, payment_ref=?, amount=? WHERE id=?",
                    (now, 'SEPAY-' + transaction_id, amount, pending_order['id'])
                )
            else:
                # Tạo đơn mới với trạng thái paid
                product = conn.execute(
                    "SELECT id FROM products WHERE is_active=1 ORDER BY id LIMIT 1"
                ).fetchone()
                product_id = product['id'] if product else 1
                conn.execute(
                    "INSERT INTO orders (customer_id, product_id, amount, status, payment_ref, ordered_at, paid_at, note) "
                    "VALUES (?, ?, ?, 'paid', ?, ?, ?, ?)",
                    (customer_id, product_id, amount,
                     'SEPAY-' + transaction_id, now, now,
                     'Tự động từ Sepay webhook - ' + content)
                )
                conn.execute(
                    "UPDATE products SET slots_remaining = MAX(0, slots_remaining - 1) WHERE id=?",
                    (product_id,)
                )

        conn.commit()

    print(f'[Sepay] {transaction_date} | {amount:,}đ | "{content}" | customer_id={customer_id}')
    return jsonify({'success': True})


# ── Payment status (polling từ frontend) ────────────────────────────────────

@app.route('/api/payment-status', methods=['GET'])
def payment_status():
    phone = request.args.get('phone', '').strip()
    if not phone:
        return jsonify({'status': 'unknown'})
    with get_db() as conn:
        row = conn.execute('''
            SELECT o.status FROM orders o
            JOIN customers c ON c.id = o.customer_id
            WHERE c.phone = ?
            ORDER BY o.id DESC LIMIT 1
        ''', (phone,)).fetchone()
    if not row:
        return jsonify({'status': 'pending'})
    return jsonify({'status': row['status']})


# ── Stats ────────────────────────────────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def stats():
    with get_db() as conn:
        total_customers = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
        total_orders = conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
        paid_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status='paid'").fetchone()[0]
        total_revenue = conn.execute("SELECT COALESCE(SUM(amount),0) FROM orders WHERE status='paid'").fetchone()[0]
        slots = conn.execute('SELECT slots_remaining FROM products WHERE id=1').fetchone()
    return jsonify({
        'total_customers': total_customers,
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'total_revenue': total_revenue,
        'slots_remaining': slots[0] if slots else 0
    })


init_db()

if __name__ == '__main__':
    os.makedirs(ADMIN_DIR, exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f'Admin panel: http://localhost:{port}/admin')
    app.run(host='0.0.0.0', debug=debug, port=port)
