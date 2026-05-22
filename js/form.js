(function () {
    const form = document.getElementById('register-form');
    if (!form) return;

    const submitBtn = form.querySelector('[type="submit"]');
    const statusEl = document.getElementById('form-status');

    function setStatus(message, type) {
        if (!statusEl) return;
        statusEl.textContent = message;
        statusEl.className = 'form-status form-status--' + type;
        statusEl.hidden = !message;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const webhookUrl = (window.MAKE_WEBHOOK_URL || '').trim();
        if (!webhookUrl) {
            setStatus('Chưa cấu hình Webhook. Mở file config.js và dán URL từ Make.com.', 'error');
            return;
        }

        const data = new FormData(form);
        const now = new Date();
        const payload = {
            name: (data.get('name') || '').toString().trim(),
            phone: (data.get('phone') || '').toString().trim(),
            email: (data.get('email') || '').toString().trim(),
            service: (data.get('service') || '').toString().trim(),
            source: (window.SITE_SOURCE || window.location.origin || '').trim(),
            submitted_at: now.toISOString(),
            submitted_at_vn: now.toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' })
        };

        if (!payload.name || !payload.phone || !payload.email || !payload.service) {
            setStatus('Vui lòng điền đầy đủ thông tin bắt buộc.', 'error');
            return;
        }

        submitBtn.disabled = true;
        setStatus('Đang gửi...', 'loading');

        try {
            const res = await fetch(webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                throw new Error('HTTP ' + res.status);
            }

            // Lưu khách hàng vào brain.db (không block nếu admin server offline)
            var adminUrl = (window.ADMIN_API_URL || 'http://localhost:5000').replace(/\/$/, '');
            fetch(adminUrl + '/api/customers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: payload.name,
                    phone: payload.phone,
                    email: payload.email,
                    service: payload.service,
                    source: 'website'
                })
            }).catch(function () {});

            form.reset();
            setStatus('Đã nhận thông tin! Vui lòng chuyển khoản bên dưới để giữ suất.', 'success');

            // Hiện QR thanh toán với nội dung CK gắn tên khách + dịch vụ
            var desc = 'NEXUSVIP ' + payload.name;
            var qrImg    = document.getElementById('payment-qr');
            var descEl   = document.getElementById('payment-desc');
            var paySection = document.getElementById('payment-section');
            if (qrImg && descEl && paySection) {
                descEl.textContent = desc;
                qrImg.src = 'https://qr.sepay.vn/img?acc=05541117101&bank=TPB&des='
                            + encodeURIComponent(desc);
                paySection.removeAttribute('hidden');
                paySection.scrollIntoView({ behavior: 'smooth', block: 'center' });

                // Polling kiểm tra thanh toán mỗi 4 giây
                var pollCount = 0;
                var pollInterval = setInterval(function () {
                    pollCount++;
                    if (pollCount > 75) { clearInterval(pollInterval); return; } // dừng sau 5 phút
                    fetch(adminUrl + '/api/payment-status?phone=' + encodeURIComponent(payload.phone))
                        .then(function (r) { return r.json(); })
                        .then(function (data) {
                            if (data.status === 'paid' || data.status === 'success') {
                                clearInterval(pollInterval);
                                paySection.setAttribute('hidden', '');
                                setStatus('Thanh toán thành công! Cảm ơn bạn đã đăng ký. Chúng tôi sẽ liên hệ sớm nhất.', 'success');
                                document.getElementById('form-status').scrollIntoView({ behavior: 'smooth', block: 'center' });
                            }
                        })
                        .catch(function () {});
                }, 4000);
            }
        } catch (err) {
            setStatus('Gửi thất bại. Kiểm tra URL Webhook trên Make.com và thử lại.', 'error');
            console.error('Webhook error:', err);
        } finally {
            submitBtn.disabled = false;
        }
    });
})();
