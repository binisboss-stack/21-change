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
            message: (data.get('message') || '').toString().trim(),
            source: (window.SITE_SOURCE || window.location.origin || '').trim(),
            submitted_at: now.toISOString(),
            submitted_at_vn: now.toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' })
        };

        if (!payload.name || !payload.phone) {
            setStatus('Vui lòng nhập Họ tên và Số điện thoại.', 'error');
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

            form.reset();
            setStatus('Đã gửi thành công! Chúng tôi sẽ liên hệ bạn sớm.', 'success');
        } catch (err) {
            setStatus('Gửi thất bại. Kiểm tra URL Webhook trên Make.com và thử lại.', 'error');
            console.error('Webhook error:', err);
        } finally {
            submitBtn.disabled = false;
        }
    });
})();
