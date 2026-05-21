(function () {
  'use strict';

  // ─── KỊCH BẢN (từ sales_script.md) ──────────────────────────────────────────
  var NODES = {
    welcome: {
      messages: [
        'Ủa, anh/chị ghé qua rồi 👋',
        'Em là bot hỗ trợ của NEXUS VIP GROUP — room tín hiệu XAUUSD thực chiến.',
        'Anh/chị đang tìm hiểu về room hay muốn xem kết quả lệnh thật trước?'
      ],
      quickReplies: [
        { text: '1️⃣  Xem kết quả lệnh gần đây', next: 'winrate' },
        { text: '2️⃣  Room có gì — phí bao nhiêu', next: 'offer' },
        { text: '3️⃣  Tôi chưa biết gì về XAUUSD', next: 'f0' }
      ]
    },

    winrate: {
      messages: [
        'Số này lấy từ lịch sử lệnh thật — có screenshot từng lệnh, có Entry + TP + SL + kết quả.',
        'Anh/chị có thể tự check: em gửi lịch sử 3 tháng, vào TradingView kéo lại chart là biết ngay.',
        'Không cần tin em — tự kiểm chứng là chắc nhất.'
      ],
      quickReplies: [
        { text: 'Gửi lịch sử lệnh cho tôi', next: 'history' },
        { text: 'Room có gì — phí bao nhiêu?', next: 'offer' },
        { text: 'Vốn tối thiểu bao nhiêu?', next: 'capital' }
      ]
    },

    offer: {
      messages: [
        'Chương trình hiện tại: miễn phí hoàn toàn trải nghiệm.',
        'Để lại tin nhắn — em gửi bảng giá cụ thể + ưu đãi đang áp dụng cho anh/chị luôn.',
        '(Giá thay đổi theo đợt — hỏi sớm còn kịp giá tốt nha.)'
      ],
      quickReplies: [
        { text: '👉  Để lại thông tin ngay', next: 'register', cta: true },
        { text: 'Winrate 82% có thật không?', next: 'winrate' },
        { text: 'Tín hiệu gửi qua đâu?', next: 'platform' },
        { text: 'Phí này có phù hợp với bạn không?', next: 'price_check' }
      ]
    },

    f0: {
      messages: [
        'Được, thật sự.',
        'Khi vào room anh/chị được tặng kèm video khoá học F0 — từ cách mở tài khoản, đặt lệnh, đọc chart cơ bản.',
        'Ví dụ: lệnh bot gửi ghi rõ "Buy 3330 – TP 3345 – SL 3320" — anh/chị chỉ cần copy y chang vào app là xong.'
      ],
      quickReplies: [
        { text: 'Phí tham gia bao nhiêu?', next: 'offer' },
        { text: 'Tín hiệu gửi qua đâu?', next: 'platform' },
        { text: 'Vốn tối thiểu là bao nhiêu?', next: 'capital' }
      ]
    },

    platform: {
      messages: [
        'Gửi qua Telegram — nhanh nhất, không bị miss thông báo.',
        'Thường trước khi phiên NY mở (khoảng 8–9h tối VN) và phiên London (2–3h sáng).',
        'Anh/chị không cần thức khuya — lệnh có SL/TP cài sẵn, đặt xong là ngủ được.'
      ],
      quickReplies: [
        { text: 'Phí bao nhiêu?', next: 'offer' },
        { text: 'Vốn tối thiểu bao nhiêu?', next: 'capital' },
        { text: 'Tôi không có thời gian theo dõi', next: 'notime' }
      ]
    },

    capital: {
      messages: [
        'Không có giới hạn tối thiểu.',
        'Nhưng để dễ quản lý rủi ro, nên có ít nhất $1000.',
        'Ý là dù vốn nhỏ, tỷ lệ % lãi vẫn như nhau — vốn lớn thì số tiền tuyệt đối lớn hơn thôi.'
      ],
      quickReplies: [
        { text: 'Phí tham gia bao nhiêu?', next: 'offer' },
        { text: 'Thị trường đang xấu, có nên vào không?', next: 'bearmarket' },
        { text: '👉  Đăng ký thử 30 ngày', next: 'register', cta: true }
      ]
    },

    notime: {
      messages: [
        'Không cần theo suốt ngày — thật sự.',
        'Anh/chị đặt lệnh theo tín hiệu (5 phút), cài SL/TP sẵn, xong việc. Lệnh tự chạy, tự đóng.',
        'Ví dụ: Katherine — nhân viên văn phòng trong room — chỉ check Telegram buổi sáng. Tài khoản vẫn tăng đều.'
      ],
      quickReplies: [
        { text: 'Phí bao nhiêu?', next: 'offer' },
        { text: '👉  Thử xem', next: 'register', cta: true },
        { text: 'Tôi đã vào nhiều room rồi bị lừa', next: 'scam' }
      ]
    },

    bearmarket: {
      messages: [
        'Đây thật ra là lúc tốt nhất để vào.',
        'Vì room sẽ chỉ cho anh/chị biết chính xác vùng nào là đáy thật — thay vì anh/chị mua bừa rồi tự hỏi "đây có phải đáy chưa?"',
        'Winrate 82% tính cả trong giai đoạn bearish — không chỉ khi thị trường dễ.'
      ],
      quickReplies: [
        { text: 'Phí bao nhiêu?', next: 'offer' },
        { text: '👉  Đăng ký thử', next: 'register', cta: true },
        { text: 'Không hài lòng thì sao?', next: 'refund' }
      ]
    },

    scam: {
      messages: [
        'Ok, em hiểu — và không phán xét gì đâu.',
        'Điểm khác nhau: mỗi lệnh của NEXUS đều có SL cứng — tức là dù có gì xảy ra, lệnh tự đóng trước khi lỗ quá ngưỡng cho phép.',
        'Anh/chị có thể xem 10 lệnh gần nhất — tự check trên chart xem Entry + TP có khớp không. Không khớp thì không vào, đơn giản vậy thôi.'
      ],
      quickReplies: [
        { text: 'Cho xem lịch sử lệnh', next: 'history' },
        { text: 'Không hài lòng thì sao?', next: 'refund' },
        { text: 'Phí bao nhiêu?', next: 'offer' }
      ]
    },

    refund: {
      messages: [
        'Hoàn tiền 100% trong 30 ngày — không hỏi lý do.',
        'Ý là anh/chị test thật sự, không phải test trên giấy. Trong 30 ngày chất lượng không như cam kết — lấy tiền lại, không drama.',
        'Nên thật ra không có rủi ro gì khi thử cả.'
      ],
      quickReplies: [
        { text: '👉  Đăng ký ngay', next: 'register', cta: true },
        { text: 'Phí cụ thể bao nhiêu?', next: 'offer' }
      ]
    },

    history: {
      messages: [
        'Em gửi anh/chị lịch sử 3 tháng lệnh thật liền.',
        'Để tiện hơn, anh/chị để lại thông tin — em gửi ngay qua Telegram.'
      ],
      quickReplies: [
        { text: '👉  Để lại thông tin', next: 'register', cta: true },
        { text: 'Không hài lòng thì sao?', next: 'refund' }
      ]
    },

    register: {
      messages: [
        'Đơn giản lắm:',
        '1️⃣  Điền tên + số điện thoại vào form\n2️⃣  Em liên hệ lại trong 1 tiếng — tư vấn + xác nhận slot\n3️⃣  Sau khi xác nhận → nhận link vào group + tài liệu khoá học ngay',
        'Anh/chị muốn bắt đầu không?'
      ],
      quickReplies: [
        { text: '👉  Điền form ngay', next: '_form', cta: true },
        { text: 'Hỏi thêm chút nữa', next: 'more' }
      ]
    },

    more: {
      messages: [
        'Ok, hỏi đi — em ở đây.'
      ],
      quickReplies: [
        { text: 'Winrate 82% có thật không?', next: 'winrate' },
        { text: 'Tín hiệu gửi qua đâu?', next: 'platform' },
        { text: 'Không hài lòng thì sao?', next: 'refund' },
        { text: 'Tôi đã vào nhiều room rồi bị lừa', next: 'scam' }
      ]
    },

    // Hỏi về phí — 3 lựa chọn
    price_check: {
      messages: [
        'Với anh/chị thì phí này thế nào — ok hay còn băn khoăn gì không?'
      ],
      quickReplies: [
        { text: 'Có, tôi nghĩ ổn', next: 'register', cta: true },
        { text: 'Để tôi suy nghĩ thêm', next: 'think_more' },
        { text: 'Tôi không đủ vốn', next: 'capital' }
      ]
    },

    // Khách nói "để suy nghĩ thêm" → chốt ngược
    think_more: {
      messages: [
        'Ok, không vấn đề.',
        'Anh/chị đang phân vân điều gì nhất? Giá, chất lượng tín hiệu, hay còn gì khác?',
        'Hỏi thẳng đi — em giải thích cái đó xong, anh/chị quyết định dễ hơn.'
      ],
      quickReplies: [
        { text: 'Giá chưa phù hợp với tôi', next: 'price_concern' },
        { text: 'Chưa tin vào chất lượng', next: 'winrate' },
        { text: 'Cần hỏi ý kiến vợ / chồng trước', next: 'ask_family' },
        { text: '👉  Thử 30 ngày — hoàn tiền nếu không ok', next: 'refund', cta: true }
      ]
    },

    price_concern: {
      messages: [
        'Anh/chị đang trade với vốn bao nhiêu?',
        'Ý là nếu vốn $1000, với lợi nhuận trung bình 35%/năm của Room thì một năm tăng thêm $350. Phí Room chỉ một phần nhỏ — anh/chị nghĩ có xứng không?',
        'Ngoài ra còn 30 ngày hoàn tiền 100% nếu không hài lòng — nên không có rủi ro gì khi thử cả.'
      ],
      quickReplies: [
        { text: '👉  Thử xem — hoàn tiền nếu không ok', next: 'register', cta: true },
        { text: 'Vẫn còn phân vân', next: 'think_more' }
      ]
    },

    ask_family: {
      messages: [
        'Ok, hợp lý lắm — quyết định đầu tư nên hỏi ý kiến nhau.',
        'Để lại tin nhắn — em gửi bản tóm tắt ngắn để anh/chị chia sẻ cho vợ/chồng đọc cùng.',
        'Dễ giải thích hơn là tóm tắt miệng.'
      ],
      quickReplies: [
        { text: '👉  Để lại thông tin nhận tài liệu', next: 'register', cta: true },
        { text: 'Ok để hỏi xong rồi báo lại', next: 'followup' }
      ]
    },

    followup: {
      messages: [
        'Không sao — anh/chị hỏi xong cứ nhắn lại đây.',
        'Em để sẵn lịch sử lệnh 3 tháng và bảng giá để anh/chị và vợ/chồng cùng xem nhé.'
      ],
      quickReplies: [
        { text: '👉  Để lại thông tin nhận tài liệu', next: 'register', cta: true }
      ]
    }
  };

  // ─── KEYWORD ROUTING cho free-text input ─────────────────────────────────────
  var KEYWORD_MAP = [
    { keywords: ['winrate', '82', 'tỷ lệ', 'lịch sử lệnh', 'kiểm chứng', 'thật không', 'xác nhận'], node: 'winrate' },
    { keywords: ['phí', 'giá', 'bao nhiêu tiền', 'chi phí', 'mất bao nhiêu', 'trả bao nhiêu', 'free', 'miễn phí'], node: 'offer' },
    { keywords: ['f0', 'mới', 'chưa biết', 'không biết gì', 'xauusd là gì', 'vàng là gì', 'newbie', 'tôi mới'], node: 'f0' },
    { keywords: ['telegram', 'zalo', 'gửi qua', 'kênh nào', 'nền tảng', 'app nào', 'mấy giờ gửi', 'gửi lúc'], node: 'platform' },
    { keywords: ['vốn', 'tối thiểu', ' $', 'đô', 'usd', 'bao nhiêu vốn', 'cần bao nhiêu'], node: 'capital' },
    { keywords: ['thời gian', 'bận', 'không có thời', 'theo dõi', 'suốt ngày', 'ngày làm', 'bận rộn'], node: 'notime' },
    { keywords: ['xấu', 'bearish', 'giảm', 'bear', 'đợi lên', 'chờ lên', 'thị trường xấu'], node: 'bearmarket' },
    { keywords: ['lừa đảo', 'scam', 'lừa', 'mất tiền', 'room trước', 'không tin', 'nghi ngờ', 'bị lừa'], node: 'scam' },
    { keywords: ['hoàn tiền', 'không hài lòng', 'trả lại', 'đảm bảo', 'bảo hành', 'refund', '30 ngày'], node: 'refund' },
    { keywords: ['đăng ký', 'mua', 'tham gia', 'vào room', 'form', 'làm sao', 'bắt đầu', 'vào như thế nào'], node: 'register' },
    { keywords: ['suy nghĩ', 'cân nhắc', 'nghĩ thêm', 'chưa chắc', 'chưa quyết', 'phân vân', 'để nghĩ', 'cần nghĩ', 'hỏi thêm rồi', 'chưa vội'], node: 'think_more' }
  ];

  // ─── DOM ─────────────────────────────────────────────────────────────────────
  var toggleBtn     = document.getElementById('chatbot-toggle');
  var chatWindow    = document.getElementById('chatbot-window');
  var messagesEl    = document.getElementById('chatbot-messages');
  var quickRepliesEl= document.getElementById('chatbot-quick-replies');
  var inputEl       = document.getElementById('chatbot-input');
  var sendBtn       = document.getElementById('chatbot-send-btn');
  var closeBtnEl    = document.getElementById('cb-close-btn');
  var badgeEl       = document.getElementById('chatbot-badge');
  var iconChat      = document.getElementById('cb-icon-chat');
  var iconClose     = document.getElementById('cb-icon-close');

  if (!toggleBtn) return;

  var isOpen      = false;
  var isBotTyping = false;
  var greeted     = false;

  // ─── OPEN / CLOSE ────────────────────────────────────────────────────────────
  function openChat() {
    isOpen = true;
    chatWindow.removeAttribute('hidden');
    chatWindow.classList.add('cb-open');
    chatWindow.addEventListener('animationend', function () {
      chatWindow.classList.remove('cb-open');
    }, { once: true });
    iconChat.style.display  = 'none';
    iconClose.style.display = '';
    badgeEl.style.display   = 'none';
    if (!greeted) {
      greeted = true;
      setTimeout(function () { goToNode('welcome'); }, 500);
    }
    setTimeout(function () { inputEl.focus(); }, 400);
  }

  function closeChat() {
    isOpen = false;
    chatWindow.setAttribute('hidden', '');
    iconChat.style.display  = '';
    iconClose.style.display = 'none';
  }

  toggleBtn.addEventListener('click', function () {
    isOpen ? closeChat() : openChat();
  });
  closeBtnEl.addEventListener('click', closeChat);

  // ─── MESSAGES ────────────────────────────────────────────────────────────────
  function addBotMessage(text) {
    var el = document.createElement('div');
    el.className = 'cb-msg cb-msg--bot';
    el.textContent = text;
    messagesEl.appendChild(el);
    scrollBottom();
  }

  function addUserMessage(text) {
    var el = document.createElement('div');
    el.className = 'cb-msg cb-msg--user';
    el.textContent = text;
    messagesEl.appendChild(el);
    scrollBottom();
  }

  function showTyping() {
    var el = document.createElement('div');
    el.className = 'cb-typing';
    el.id = 'cb-typing-indicator';
    el.innerHTML = '<span></span><span></span><span></span>';
    messagesEl.appendChild(el);
    scrollBottom();
  }

  function hideTyping() {
    var el = document.getElementById('cb-typing-indicator');
    if (el) el.remove();
  }

  function scrollBottom() {
    requestAnimationFrame(function () {
      messagesEl.scrollTop = messagesEl.scrollHeight;
    });
  }

  // ─── QUICK REPLIES ───────────────────────────────────────────────────────────
  function setQuickReplies(replies) {
    quickRepliesEl.innerHTML = '';
    if (!replies || !replies.length) return;
    replies.forEach(function (r) {
      var btn = document.createElement('button');
      btn.className = 'cb-qr-btn' + (r.cta ? ' cb-qr-btn--cta' : '');
      btn.textContent = r.text;
      btn.addEventListener('click', function () { onQuickReply(r); });
      quickRepliesEl.appendChild(btn);
    });
  }

  function onQuickReply(reply) {
    if (isBotTyping) return;
    addUserMessage(reply.text);
    setQuickReplies([]);
    if (reply.next === '_form') {
      goToForm();
    } else {
      setTimeout(function () { goToNode(reply.next); }, 350);
    }
  }

  // ─── NODE NAVIGATION ─────────────────────────────────────────────────────────
  function goToNode(nodeKey) {
    var node = NODES[nodeKey];
    if (!node) return;
    setQuickReplies([]);
    playMessages(node.messages, 0, function () {
      setQuickReplies(node.quickReplies);
    });
  }

  function playMessages(msgs, idx, done) {
    if (idx >= msgs.length) {
      isBotTyping = false;
      if (done) done();
      return;
    }
    isBotTyping = true;
    var preDelay = idx === 0 ? 350 : 450;
    setTimeout(function () {
      showTyping();
      var duration = Math.min(500 + msgs[idx].length * 14, 1500);
      setTimeout(function () {
        hideTyping();
        addBotMessage(msgs[idx]);
        playMessages(msgs, idx + 1, done);
      }, duration);
    }, preDelay);
  }

  // ─── SCROLL TO FORM ───────────────────────────────────────────────────────────
  function goToForm() {
    closeChat();
    var form = document.getElementById('register-form');
    if (!form) return;
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(function () {
      var first = form.querySelector('input');
      if (first) first.focus();
    }, 700);
  }

  // ─── FREE TEXT INPUT ──────────────────────────────────────────────────────────
  function handleInput() {
    var text = inputEl.value.trim();
    if (!text || isBotTyping) return;
    inputEl.value = '';
    addUserMessage(text);
    setQuickReplies([]);
    var lower = text.toLowerCase();
    var matched = null;
    for (var i = 0; i < KEYWORD_MAP.length; i++) {
      var entry = KEYWORD_MAP[i];
      for (var j = 0; j < entry.keywords.length; j++) {
        if (lower.indexOf(entry.keywords[j].toLowerCase()) !== -1) {
          matched = entry.node;
          break;
        }
      }
      if (matched) break;
    }
    setTimeout(function () { goToNode(matched || 'more'); }, 400);
  }

  sendBtn.addEventListener('click', handleInput);
  inputEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') handleInput();
  });

  // ─── BADGE: hiện sau 3s để kéo attention ─────────────────────────────────────
  setTimeout(function () {
    if (!isOpen) {
      badgeEl.style.display = 'flex';
    }
  }, 3000);

})();
