"""
Admin panel server for brain.db
Run: python admin_server.py
Then open: http://localhost:5000/admin
"""
import sqlite3
import os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'brain.db')
ADMIN_DIR = os.path.join(BASE_DIR, 'admin')

app = Flask(__name__)


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
            conn.commit()
            row = conn.execute('SELECT * FROM customers WHERE id=?', (cur.lastrowid,)).fetchone()
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
        row = conn.execute('''
            SELECT o.*, c.name AS customer_name, p.name AS product_name
            FROM orders o
            LEFT JOIN customers c ON c.id = o.customer_id
            LEFT JOIN products p ON p.id = o.product_id
            WHERE o.id=?
        ''', (cur.lastrowid,)).fetchone()
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
                "SELECT id FROM customers WHERE UPPER(name) LIKE ?",
                ('%' + customer_name + '%',)
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


if __name__ == '__main__':
    os.makedirs(ADMIN_DIR, exist_ok=True)
    print('Admin panel: http://localhost:5000/admin')
    app.run(debug=True, port=5000)
