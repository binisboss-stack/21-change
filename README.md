# Landing Page — StockVN / Tiệm Hoa T Mon

Landing page marketing 10-step funnel (HTML/CSS/JS thuần), form đăng ký, CTA liên hệ và deploy production.

## Liên kết production

| Mục | URL |
|-----|-----|
| Website | https://www.tiemhoatmon.com |
| Vercel | https://21-change.vercel.app |
| GitHub | https://github.com/binisboss-stack/21-change |

## Cấu trúc project

```
├── index.html              # Trang landing chính
├── config.js               # Webhook Make, liên hệ, nguồn site (SỬA FILE NÀY)
├── config.example.js       # Mẫu cấu hình
├── js/
│   ├── form.js             # Gửi form → Make.com webhook
│   └── contact.js          # Gắn link Zalo / Gọi / Email từ CONTACT
├── images/
├── netlify.toml            # Cấu hình deploy tĩnh (tuỳ chọn Netlify)
├── CHAT_LOG.md             # Lịch sử phát triển landing
└── README.md               # Tài liệu này
```

## Tính năng đã hoàn thành

- [x] Giao diện dark + vàng, responsive
- [x] Form đăng ký → **Make.com** (Custom Webhook)
- [x] **Google Sheets** (module Add a row trên Make)
- [x] CTA: Mua ngay, Đặt hàng ngay, Nhắn Zalo, Gọi ngay, Email
- [x] Bong bóng liên hệ cố định góc phải dưới (mobile + desktop)
- [x] Deploy **GitHub** + **Vercel** + domain `www.tiemhoatmon.com`

## Cấu hình — `config.js`

```javascript
// Webhook Make.com
window.MAKE_WEBHOOK_URL = 'https://hook.eu1.make.com/XXXXX';

// Nguồn ghi vào Make / Google Sheet
window.SITE_SOURCE = 'https://www.tiemhoatmon.com/';

// Liên hệ thật (SĐT, Zalo, Email)
window.CONTACT = {
    phone: '0901234567',
    phoneDisplay: '0901 234 567',
    zaloUrl: 'https://zalo.me/0901234567',
    email: 'hotro@stockvn.vn',
    emailSubject: 'Đăng ký Room VIP StockVN'
};
```

Sau khi sửa `config.js` trên máy → commit & push để Vercel cập nhật.

## Dữ liệu form gửi lên Make.com

| Field | Mô tả |
|-------|--------|
| `name` | Họ tên |
| `phone` | Số điện thoại / Zalo |
| `email` | Email (tuỳ chọn) |
| `message` | Ghi chú |
| `source` | `SITE_SOURCE` (vd. https://www.tiemhoatmon.com/) |
| `submitted_at` | ISO datetime |
| `submitted_at_vn` | Giờ Việt Nam (map vào cột Thời gian trên Sheet) |

---

## 1. Make.com — Webhook form

1. [make.com](https://www.make.com) → **Create scenario**
2. Module **Webhooks** → **Custom webhook** → **Create a webhook**
3. Copy URL → dán vào `MAKE_WEBHOOK_URL` trong `config.js`
4. **Run once** → gửi form thử trên web → **OK** (xác nhận cấu trúc dữ liệu)
5. Bật scenario **ON**

---

## 2. Google Sheets (qua Make)

### Tạo Sheet — dòng 1

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Thời gian | Họ tên | Số điện thoại | Email | Ghi chú | Nguồn |

### Trên Make

1. Bấm **+** sau module Webhooks
2. **Google Sheets** → **Add a row**
3. Connect Google → chọn spreadsheet
4. Map cột:

| Cột Sheet | Field webhook |
|-----------|----------------|
| Thời gian | `submitted_at_vn` |
| Họ tên | `name` |
| Số điện thoại | `phone` |
| Email | `email` |
| Ghi chú | `message` |
| Nguồn | `source` |

5. Save → bật **ON** → test form → kiểm tra dòng mới trên Sheet

> Mỗi lần gửi form (gói Free): ~2 operations (Webhook + Sheets).

---

## 3. Git + Vercel — Deploy & cập nhật

### Lần đầu (đã làm)

```powershell
cd "C:\Users\HOME\Downloads\landing_page_xauusd\landing_page_xauusd"
git remote add origin https://github.com/binisboss-stack/21-change.git
git branch -M main
git push -u origin main
```

Vercel import repo `21-change` → Framework: **Other** → không cần Build Command.

### Mỗi lần sửa web sau này

```powershell
git add .
git commit -m "Mo ta thay doi"
git push
```

Vercel tự deploy lại trong 1–2 phút.

### Domain

- Vercel → Project **21-change** → **Settings** → **Domains**
- Domain: `www.tiemhoatmon.com`
- Cập nhật DNS theo hướng dẫn Vercel nếu báo *Action required*

---

## Chạy local

Mở `index.html` bằng trình duyệt (kéo thả) hoặc extension **Live Server**.

Đảm bảo `config.js` đã có `MAKE_WEBHOOK_URL` trước khi test form.

---

## Checklist vận hành

- [x] Website online: https://www.tiemhoatmon.com
- [x] Form → Make.com
- [x] Google Sheets nhận lead
- [x] CTA Zalo / Gọi / Đặt hàng
- [ ] Cập nhật `CONTACT` trong `config.js` bằng SĐT & email thật (nếu chưa đổi)

---

## Lưu ý bảo mật

`config.js` chứa URL webhook — file **public** trên Vercel. Với landing page thông thường chấp nhận được; nếu cần ẩn webhook sau này có thể chuyển sang Vercel Serverless Function.

---

## Lịch sử phát triển

Xem chi tiết các giai đoạn thiết kế (XAUUSD → StockVN → form → deploy) trong [CHAT_LOG.md](./CHAT_LOG.md).
