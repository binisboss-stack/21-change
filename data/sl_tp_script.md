# Script Video: Cách đặt SL/TP cho XAUUSD — không cần phân tích phức tạp
**Thời lượng:** ~20 phút | **Đối tượng:** F0 đang trade XAUUSD, chưa chắc về SL/TP

---

## PHẦN 1 — Hook (0:00 – 2:00)

Ok, bắt đầu thẳng vào vấn đề luôn.

Lý do anh/chị bị stop out không phải vì dự đoán sai chiều. Thường là vì đặt SL quá gần — vàng đi ngược một chút rồi quay lại đúng hướng, nhưng mình đã bị out từ trước rồi.

Hoặc ngược lại — không đặt SL, để lệnh chạy, lỗ ngày càng to.

Ý là, đặt SL/TP đúng không phải là "đoán giá đến đâu". Nó là quản lý xác suất. Mình không cần chart đúng 10/10, mình chỉ cần khi đúng thì lời nhiều hơn khi sai.

Trong video này tôi sẽ chỉ 3 cách đặt SL/TP cụ thể:

1. **Theo Structure** — swing high/low, chuẩn nhất
2. **Theo ATR** — dùng chỉ báo, có công thức
3. **Fixed Zone** — đơn giản nhất, dùng được ngay hôm nay

Cuối video có file cheat sheet 1 trang, in ra dán cạnh máy. Link ở phần mô tả.

---

## PHẦN 2 — Phương pháp 1: Đặt SL theo Structure (2:00 – 8:00)

### Structure là gì?

Structure là những vùng giá mà thị trường đã "dừng lại" hoặc "đổi hướng" — ví dụ như là đỉnh cũ, đáy cũ, vùng tích lũy.

Nhìn vào chart XAUUSD H1, anh/chị sẽ thấy: giá không đi thẳng lên hay thẳng xuống. Nó tạo ra các bậc thang — lên, dừng, lên tiếp. Mỗi điểm dừng đó là một structure.

### Quy tắc đặt SL theo Structure

**Vào lệnh Buy:**
SL đặt dưới đáy swing gần nhất — cách vài pip để tránh wick.

**Vào lệnh Sell:**
SL đặt trên đỉnh swing gần nhất — cách vài pip.

Tại sao? Vì nếu giá phá qua đỉnh/đáy đó thì xu hướng mình đang theo đã bị phá vỡ rồi. Ở trong lệnh lúc đó không còn ý nghĩa nữa.

### Ví dụ thực tế

Ví dụ như là: giá XAUUSD đang ở 2.340. Mình thấy đáy swing gần nhất ở 2.330. Vào lệnh Buy tại 2.340, SL đặt ở 2.328 (2 pip dưới đáy swing, tránh wick).

SL = 12 pip ($12 cho 1 mini lot).

TP đặt ở đâu? Tối thiểu R:R 1:2 — nghĩa là nếu SL = 12 pip thì TP = 24 pip trở lên. TP ở 2.364.

### Khi nào dùng Structure?

Khi chart có cấu trúc rõ ràng — xu hướng rõ, swing cao/thấp rõ. Khung H1, H4 dễ thấy nhất.

Không nên dùng khi chart đang đi ngang lộn xộn, không xác định được swing rõ ràng.

---

## PHẦN 3 — Phương pháp 2: Đặt SL theo ATR (8:00 – 14:00)

### ATR là gì?

ATR là Average True Range — biên độ dao động trung bình của nến trong N phiên gần nhất.

Nôm na: ATR(14) trên H1 cho biết trung bình mỗi nến giờ vàng dao động bao nhiêu pip.

Thêm ATR vào chart trong MT4/MT5: Insert → Indicators → Average True Range, period = 14.

### ATR của XAUUSD thường bao nhiêu?

- Khung H1: ATR thường dao động 3–8 pip ($3–$8 / mini lot)
- Khung H4: ATR thường 15–25 pip
- Khung D1: ATR thường 80–150 pip

Con số này thay đổi theo thị trường — news lớn thì ATR tăng vọt.

### Công thức đặt SL/TP theo ATR

**SL = Entry ± (ATR × 1.5)**
**TP = Entry ± (ATR × 3)**

Tức là SL cách entry 1.5 lần ATR, TP cách 3 lần ATR → R:R tự động 1:2.

### Ví dụ thực tế

Giá XAUUSD H1 = 2.340. ATR(14) hiện tại = 5 pip.

- Vào Buy tại 2.340
- SL = 2.340 − (5 × 1.5) = 2.340 − 7.5 = **2.332.5**
- TP = 2.340 + (5 × 3) = 2.340 + 15 = **2.355**

### Tại sao ATR × 1.5?

Vì SL cần đủ rộng để tránh nhiễu bình thường của thị trường. Nếu SL = ATR × 1, thì bình thường thị trường cũng có thể chạm SL trong khi xu hướng vẫn đúng.

1.5 là hệ số cân bằng giữa rủi ro chấp nhận được và độ "thở" cho lệnh.

### Khi nào dùng ATR?

Tốt nhất khi thị trường đang trong giai đoạn bình thường, không có news lớn. Trước khi NFP, CPI, Fed meeting — ATR tăng đột biến, công thức này sẽ cho SL rất rộng. Lúc đó không vào lệnh hoặc giảm lot size.

---

## PHẦN 4 — Phương pháp 3: Fixed Zone (14:00 – 18:00)

### Đơn giản nhất — dùng được ngay

Fixed Zone là cách đặt SL/TP cố định theo phiên giao dịch, không cần đọc chart phức tạp.

Phù hợp với người mới bắt đầu hoặc khi không có thời gian phân tích kỹ.

### Bảng Fixed Zone theo phiên

| Phiên | Giờ VN | SL gợi ý | TP gợi ý |
|---|---|---|---|
| Asian | 6h–15h | 8–12 pip | 16–24 pip |
| London | 15h–21h | 15–20 pip | 30–40 pip |
| New York | 20h–1h sáng | 15–20 pip | 30–40 pip |
| Overlap London-NY | 20h–21h | 20–25 pip | 40–50 pip |

Asian session ít biến động → SL hẹp hơn. London/NY biến động mạnh → cần SL rộng hơn.

### Quy tắc cứng khi dùng Fixed Zone

1. **Không vào lệnh trong 15 phút trước và sau news quan trọng** — SL sẽ bị xé bất kể đặt bao nhiêu.
2. **Chỉ vào lệnh theo hướng trend D1** — nếu D1 đang uptrend thì chỉ Buy, không Sell ngược chiều.
3. **Lot size phải tính trước** — SL 20 pip, tài khoản $1000, chỉ chấp nhận mất 2% = $20 → lot size = 0.1.

### Công thức tính lot size đơn giản

```
Lot size = (Vốn × % rủi ro) ÷ (SL theo pip × Pip value)
```

Pip value XAUUSD ≈ $1/pip với 0.1 lot (mini lot).

Ví dụ: Vốn $1000, rủi ro 2%, SL = 20 pip
→ Lot = (1000 × 0.02) ÷ 20 = 20 ÷ 20 = **0.1 lot**

---

## PHẦN 5 — Tổng kết + Hỏi & Đáp (18:00 – 20:00)

### So sánh 3 phương pháp

| | Structure | ATR | Fixed Zone |
|---|---|---|---|
| Độ khó | Trung bình | Dễ-Trung bình | Dễ |
| Thời gian setup | 5–10 phút | 2–3 phút | < 1 phút |
| Độ chính xác | Cao nhất | Cao | Trung bình |
| Phù hợp khi | Chart có cấu trúc rõ | Thị trường bình thường | Mới bắt đầu |

### Lộ trình gợi ý

**Tháng 1–2:** Dùng Fixed Zone trước. Làm quen nhịp thị trường, tập tính lot size đúng.

**Tháng 3–4:** Chuyển sang ATR. Học cách đọc ATR, điều chỉnh theo biến động thực tế.

**Tháng 5 trở đi:** Kết hợp Structure + ATR. Lúc này mình đã có cảm giác chart, hai cái kia sẽ tự nhiên hơn.

### Câu hỏi hay gặp nhất

**"SL bị hit liên tục, là do đặt sai hay do bad luck?"**
Nếu bị hit > 60% số lệnh → đặt SL quá gần. Thử nhân SL hiện tại lên 1.5x, xem có cải thiện không.

**"TP chưa đến thì giá quay đầu, có nên dời TP không?"**
Không dời TP xuống thấp hơn. Chỉ dời TP lên cao hơn khi có structure mới xuất hiện theo hướng mình đang đúng. Dời TP thấp xuống là tự phá R:R.

**"Vào đúng hướng nhưng SL vẫn bị hit, rồi giá đi đúng như mình nghĩ — bực lắm, phải làm sao?"**
Đây là "stop hunt" — market maker quét SL trước khi đi đúng hướng. Giải pháp: SL rộng hơn một chút (thêm 5–8 pip) + giảm lot size để risk không tăng.

---

## KẾT

Nhắc lại 3 điều quan trọng nhất:

1. SL phải đặt dựa trên thị trường, không phải dựa trên số tiền mình sẵn sàng mất. (Tính lot size sau, không phải đặt SL sau.)
2. R:R tối thiểu 1:2 — không thương lượng.
3. Lot size luôn tính trước khi vào lệnh.

File cheat sheet 1 trang tóm tắt toàn bộ trong phần mô tả. In ra, dán cạnh máy, mỗi lần vào lệnh nhìn vào đó.

Nếu có câu hỏi gì thì để lại comment hoặc nhắn thẳng vào group.

---
*Script by NEXUS VIP — Room tín hiệu XAUUSD*
