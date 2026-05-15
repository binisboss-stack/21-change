(function () {
    const c = window.CONTACT || {};
    const phone = (c.phone || '').replace(/\s/g, '');
    const telHref = phone ? 'tel:+84' + phone.replace(/^0/, '') : '#';
    const zaloHref = c.zaloUrl || (phone ? 'https://zalo.me/' + phone : '#');
    const email = c.email || '';
    const emailHref = email
        ? 'mailto:' + email + '?subject=' + encodeURIComponent(c.emailSubject || 'Liên hệ từ website')
        : '#';

    document.querySelectorAll('[data-cta="zalo"]').forEach(function (el) {
        el.href = zaloHref;
        el.target = '_blank';
        el.rel = 'noopener noreferrer';
    });

    document.querySelectorAll('[data-cta="phone"]').forEach(function (el) {
        el.href = telHref;
    });

    document.querySelectorAll('[data-cta="email"]').forEach(function (el) {
        el.href = emailHref;
    });

    document.querySelectorAll('[data-cta="order"]').forEach(function (el) {
        el.href = '#register-form';
    });

    document.querySelectorAll('[data-contact="phone"]').forEach(function (el) {
        el.textContent = c.phoneDisplay || c.phone || '—';
    });

    document.querySelectorAll('[data-contact="email"]').forEach(function (el) {
        el.textContent = email || '—';
    });
})();
