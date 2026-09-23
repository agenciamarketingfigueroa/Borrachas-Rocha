/* Rascunho local do pedido interno. Adicione preços padrão, em centavos, por código. */
(function () {
  const AUTH_SESSION_KEY = 'borrachas-rocha-internal-access-v1';
  const TEST_PASSWORD = '1234';
  const STORAGE_KEY = 'borrachas-rocha-internal-order-v1';
  const WHATSAPP_NUMBER = '';
  const CATALOG_PRICES_CENTS = {};
  const form = document.querySelector('#internal-form');
  const searchInput = document.querySelector('#internal-search');
  const results = document.querySelector('#internal-results');
  const itemsElement = document.querySelector('#internal-items');
  const status = document.querySelector('#internal-status');
  const money = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
  let products = [];
  let order = loadOrder();

  function showInternalArea() {
    document.querySelector('#internal-login').hidden = true;
    document.querySelector('#internal-content').hidden = false;
    document.querySelector('#internal-logout').hidden = false;
  }
  document.querySelector('#internal-open-order').addEventListener('click', function () {
    document.querySelector('#internal-tools').hidden = true;
    document.querySelector('#internal-order').hidden = false;
    window.scrollTo(0, 0);
    document.querySelector('#internal-back').focus();
  });
  document.querySelector('#internal-back').addEventListener('click', function () {
    document.querySelector('#internal-order').hidden = true;
    document.querySelector('#internal-tools').hidden = false;
    window.scrollTo(0, 0);
    document.querySelector('#internal-open-order').focus();
  });
  try { if (sessionStorage.getItem(AUTH_SESSION_KEY) === '1') showInternalArea(); }
  catch (error) { /* O formulário continua disponível sem lembrar o acesso. */ }
  document.querySelector('#internal-login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const input = document.querySelector('#internal-password');
    if (input.value !== TEST_PASSWORD) {
      document.querySelector('#internal-login-error').textContent = 'Senha incorreta. Tente novamente.';
      input.select();
      return;
    }
    try { sessionStorage.setItem(AUTH_SESSION_KEY, '1'); } catch (error) { /* Acesso só nesta página. */ }
    input.value = '';
    document.querySelector('#internal-login-error').textContent = '';
    showInternalArea();
    document.querySelector('#internal-open-order').focus();
  });
  document.querySelector('#internal-password').addEventListener('input', function () {
    document.querySelector('#internal-login-error').textContent = '';
  });
  document.querySelector('#internal-logout').addEventListener('click', function () {
    try { sessionStorage.removeItem(AUTH_SESSION_KEY); } catch (error) { /* Sem sessão armazenada. */ }
    window.location.reload();
  });

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"']/g, function (char) {
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#039;' }[char];
    });
  }
  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  }
  function quantity(value) {
    const number = Number(value);
    return Number.isFinite(number) ? Math.max(0, Math.min(9999, Math.floor(number))) : 0;
  }
  function parsePrice(value) {
    const text = String(value || '').trim().replace(/^R\$\s*/, '').replace(/\s/g, '');
    if (!text) return null;
    if (!/^(?:\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?|\d+(?:[,.]\d{1,2})?)$/.test(text)) return NaN;
    const number = Number(text.includes(',') ? text.replace(/\./g, '').replace(',', '.') : (/^\d{1,3}(?:\.\d{3})+$/.test(text) ? text.replace(/\./g, '') : text));
    return Number.isFinite(number) && number <= 9999999 ? Math.round(number * 100) : NaN;
  }
  function displayPrice(cents) {
    return cents === null ? '' : (cents / 100).toFixed(2).replace('.', ',');
  }
  function freshOrder() { return { customer:'', deadline:'', carrier:'', items:[] }; }
  function loadOrder() {
    const fresh = freshOrder();
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (!saved || !Array.isArray(saved.items)) return fresh;
      ['customer', 'deadline', 'carrier'].forEach(function (field) { fresh[field] = String(saved[field] || '').slice(0, 120); });
      fresh.items = saved.items.slice(0, 100).filter(function (item) { return item && typeof item.code === 'string' && Array.isArray(item.options) && item.options.length > 0; }).map(function (item) {
        return { code:item.code.slice(0, 50), options:item.options.slice(0, 12).map(function (option) {
          return { key:String(option.key || '').slice(0, 60), qty:quantity(option.qty), priceCents:Number.isSafeInteger(option.priceCents) && option.priceCents >= 0 && option.priceCents <= 999999900 ? option.priceCents : null };
        }) };
      });
    } catch (error) { return fresh; }
    return fresh;
  }
  function saveOrder() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(order)); }
    catch (error) { status.textContent = 'Este navegador não conseguiu salvar o rascunho.'; }
  }
  function optionsFor(product) {
    if (product.code === 'BR-5015') return [
      { key:'BR-5015', label:'Interno Ø 30,0 mm', orderCode:'BR-5015', qty:0 },
      { key:'BR-5015A', label:'Interno Ø 32,0 mm', orderCode:'BR-5015A', qty:0 }
    ];
    const name = String(product.name || '');
    const pattern = /\b(BR-\d+[A-Z]?|[A-E])\s*:?\s*((?:(?:diâmetro|diametro)\s+)?(?:interno|externo|pino)?\s*(?:ø|Ø|⌃)?\s*\d+(?:[.,]\d+)?\s*mm(?:\s*(?:de\s*)?altura)?)/gi;
    const found = [];
    let match;
    while ((match = pattern.exec(name)) !== null) {
      const key = match[1].toUpperCase();
      if (!found.some(function (option) { return option.key === key; })) found.push({
        key:key, label:(key.startsWith('BR-') ? key : 'Opção ' + key) + ' · ' + match[2].replace(/\s+/g, ' ').trim(),
        orderCode:key.startsWith('BR-') ? key : product.code, qty:0
      });
    }
    if (found.length > 1) return found;
    const measurements = name.match(/(?:interno|externo|altura|pino)\s*(?:ø|Ø|⌃|:)?\s*\d+(?:[.,]\d+)?\s*mm/gi) || [];
    return [{ key:'standard', label:measurements.length === 1 ? measurements[0].replace(/\s+/g, ' ').trim() : 'Quantidade de peças', orderCode:product.code, qty:1 }];
  }
  function resolvedOptions(item, product) {
    return optionsFor(product).map(function (definition) {
      const saved = item.options.find(function (option) { return option.key === definition.key; });
      return Object.assign({}, definition, {
        qty:saved ? quantity(saved.qty) : 0,
        priceCents:saved ? saved.priceCents : (CATALOG_PRICES_CENTS[definition.orderCode] ?? null)
      });
    });
  }
  function rows() {
    return order.items.flatMap(function (item) {
      const product = window.getCatalogProduct(item.code);
      if (!product) return [];
      return resolvedOptions(item, product).filter(function (option) { return option.qty > 0; }).map(function (option) { return { product:product, option:option }; });
    });
  }
  function totals() {
    const selected = rows();
    return {
      quantity:selected.reduce(function (sum, row) { return sum + row.option.qty; }, 0),
      cents:selected.reduce(function (sum, row) { return sum + (row.option.priceCents === null ? 0 : row.option.priceCents * row.option.qty); }, 0),
      missing:selected.filter(function (row) { return row.option.priceCents === null; }).length
    };
  }
  function renderResults() {
    const query = normalize(searchInput.value);
    if (!query) {
      document.querySelector('#internal-search-count').textContent = 'Digite para encontrar uma peça.';
      results.innerHTML = '';
      return;
    }
    const terms = query.split(/\s+/).filter(Boolean);
    const matches = products.filter(function (product) {
      const text = normalize([product.code, product.name, product.brand, product.application, product.specs].join(' '));
      return terms.every(function (term) { return text.includes(term); });
    }).sort(function (a, b) {
      const aCode = normalize(a.code), bCode = normalize(b.code);
      return Number(!aCode.startsWith(query)) - Number(!bCode.startsWith(query)) || a.code.localeCompare(b.code, 'pt-BR', { numeric:true });
    });
    document.querySelector('#internal-search-count').textContent = matches.length + (matches.length === 1 ? ' peça encontrada' : ' peças encontradas') + (matches.length > 12 ? ' · mostrando as 12 primeiras' : '');
    results.innerHTML = matches.slice(0, 12).map(function (product) {
      const image = window.getCatalogProductImage(product.code);
      return '<article class="internal-result"><div class="internal-result-photo">' + (image ? '<img src="' + escapeHtml(image) + '" alt="" loading="lazy" />' : '<span>Sem foto</span>') + '</div><div class="internal-result-info"><span class="internal-code">' + escapeHtml(product.code) + '</span><h3>' + escapeHtml(product.name) + '</h3><p>' + escapeHtml(product.brand) + (product.application ? ' · ' + escapeHtml(product.application) : '') + '</p></div><button type="button" data-add="' + escapeHtml(product.code) + '">Adicionar</button></article>';
    }).join('') || '<p class="internal-no-results">Nenhuma peça encontrada. Confira o código ou tente outro termo.</p>';
  }
  function renderOrder() {
    itemsElement.innerHTML = order.items.map(function (item, index) {
      const product = window.getCatalogProduct(item.code);
      if (!product) return '';
      const image = window.getCatalogProductImage(product.code);
      const options = resolvedOptions(item, product);
      return '<article class="internal-item"><div class="internal-item-head"><div class="internal-item-photo">' + (image ? '<img src="' + escapeHtml(image) + '" alt="" loading="lazy" />' : '<span>Sem foto</span>') + '</div><div class="internal-item-info"><span class="internal-code">' + escapeHtml(product.code) + '</span><h3>' + escapeHtml(product.name) + '</h3><p>' + escapeHtml(product.brand) + ' · ' + escapeHtml(product.material) + '</p></div><button type="button" class="internal-remove" data-remove="' + index + '" aria-label="Remover ' + escapeHtml(product.code) + '">×</button></div><div class="internal-options">' + options.map(function (option, optionIndex) {
        return '<div class="internal-option"><span class="internal-option-name">' + escapeHtml(option.label) + '</span><label>Qtd. <input type="number" min="0" max="9999" step="1" inputmode="numeric" value="' + option.qty + '" data-qty="' + index + ':' + optionIndex + '" aria-label="Quantidade de ' + escapeHtml(option.orderCode) + '" /></label><label>Valor unit. <span class="internal-currency">R$</span><input type="text" inputmode="decimal" placeholder="0,00" value="' + displayPrice(option.priceCents) + '" data-price="' + index + ':' + optionIndex + '" aria-label="Valor unitário de ' + escapeHtml(option.orderCode) + '" /></label>' + (option.qty > 0 && option.priceCents !== null ? '<span class="internal-subtotal">' + money.format(option.qty * option.priceCents / 100) + '</span>' : '') + '</div>';
      }).join('') + '</div></article>';
    }).join('') || '<div class="internal-empty"><strong>Nenhuma peça adicionada.</strong><p>Use a busca ao lado para começar.</p></div>';
    const total = totals();
    document.querySelector('#internal-quantity').textContent = total.quantity + (total.quantity === 1 ? ' peça' : ' peças');
    document.querySelector('#internal-total').textContent = money.format(total.cents / 100);
    document.querySelector('#internal-price-note').textContent = total.missing ? total.missing + (total.missing === 1 ? ' peça sem valor informado.' : ' peças sem valor informado.') : 'Os valores são opcionais nesta etapa.';
    document.querySelector('#internal-clear').disabled = !order.items.length && !order.customer && !order.deadline && !order.carrier;
  }
  function addProduct(code) {
    const product = window.getCatalogProduct(code);
    if (!product) return;
    const existing = order.items.find(function (item) { return item.code === code; });
    if (existing) {
      const options = resolvedOptions(existing, product);
      if (options.length === 1) existing.options[0].qty = quantity(existing.options[0].qty + 1);
    } else {
      order.items.push({ code:code, options:optionsFor(product).map(function (option) { return { key:option.key, qty:option.qty, priceCents:CATALOG_PRICES_CENTS[option.orderCode] ?? null }; }) });
    }
    saveOrder(); renderOrder();
    status.textContent = product.code + ' adicionado ao pedido.';
    if (window.matchMedia('(max-width: 800px)').matches) document.querySelector('#summary-heading').scrollIntoView({ behavior:'smooth', block:'start' });
  }
  function formattedDate(value) {
    const parts = value.split('-');
    return parts.length === 3 ? parts[2] + '/' + parts[1] + '/' + parts[0] : value;
  }
  function message() {
    const selected = rows();
    const total = totals();
    const lines = ['*PEDIDO PARA EXPEDIÇÃO — BORRACHAS ROCHA*', '', '*Cliente:* ' + order.customer.trim(), '*Prazo:* ' + formattedDate(order.deadline), '*Transportadora:* ' + order.carrier.trim(), '', '*Peças:*'];
    selected.forEach(function (row) {
      const product = row.product, option = row.option;
      lines.push('', '*' + option.orderCode + ' — ' + product.name + '*', 'Montadora: ' + product.brand + ' | Material: ' + product.material);
      if (option.label !== 'Quantidade de peças') lines.push('Medida: ' + option.label);
      lines.push('Quantidade: ' + option.qty + ' un.');
      lines.push('Valor unitário: ' + (option.priceCents === null ? 'Não informado' : money.format(option.priceCents / 100)));
      if (option.priceCents !== null) lines.push('Subtotal: ' + money.format(option.priceCents * option.qty / 100));
    });
    lines.push('', '*Total de peças:* ' + total.quantity);
    lines.push('*' + (total.missing ? 'Total dos itens com valor' : 'Valor total') + ':* ' + money.format(total.cents / 100));
    if (total.missing) lines.push('*Atenção:* ' + total.missing + (total.missing === 1 ? ' peça sem valor.' : ' peças sem valor.'));
    return lines.join('\n');
  }
  function ready() {
    if (!form.reportValidity()) return false;
    if (!totals().quantity) { status.textContent = 'Adicione uma peça e informe a quantidade antes de enviar.'; searchInput.focus(); return false; }
    order.customer = form.elements.customer.value.trim();
    order.deadline = form.elements.deadline.value;
    order.carrier = form.elements.carrier.value.trim();
    saveOrder();
    return true;
  }

  ['customer', 'deadline', 'carrier'].forEach(function (field) {
    form.elements[field].value = order[field];
    form.elements[field].addEventListener('input', function () { order[field] = this.value; saveOrder(); document.querySelector('#internal-clear').disabled = false; });
  });
  searchInput.addEventListener('input', renderResults);
  searchInput.addEventListener('keydown', function (event) { if (event.key === 'Enter') event.preventDefault(); });
  results.addEventListener('click', function (event) { const button = event.target.closest('[data-add]'); if (button) addProduct(button.dataset.add); });
  itemsElement.addEventListener('click', function (event) {
    const button = event.target.closest('[data-remove]');
    if (!button) return;
    order.items.splice(Number(button.dataset.remove), 1); saveOrder(); renderOrder(); status.textContent = 'Peça removida.';
  });
  itemsElement.addEventListener('change', function (event) {
    const qty = event.target.closest('[data-qty]');
    const price = event.target.closest('[data-price]');
    const input = qty || price;
    if (!input) return;
    const indices = (qty ? qty.dataset.qty : price.dataset.price).split(':').map(Number);
    const item = order.items[indices[0]];
    const option = item && item.options[indices[1]];
    if (!option) return;
    if (qty) option.qty = quantity(qty.value);
    if (price) {
      const cents = parsePrice(price.value);
      if (Number.isNaN(cents)) { price.setCustomValidity('Informe um valor válido, como 25,90.'); price.reportValidity(); return; }
      price.setCustomValidity(''); option.priceCents = cents;
    }
    saveOrder(); renderOrder();
  });
  itemsElement.addEventListener('input', function (event) { if (event.target.matches('[data-price]')) event.target.setCustomValidity(''); });
  document.querySelector('#internal-clear').addEventListener('click', function () {
    if (!window.confirm('Limpar todos os dados e peças deste pedido?')) return;
    order = freshOrder();
    ['customer', 'deadline', 'carrier'].forEach(function (field) { form.elements[field].value = ''; });
    saveOrder(); renderOrder(); status.textContent = 'Pedido limpo.';
  });
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!ready()) return;
    if (!WHATSAPP_NUMBER) { status.textContent = 'Número da Expedição ainda não configurado. Use “Copiar resumo do pedido”.'; return; }
    window.open('https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(message()), '_blank', 'noopener,noreferrer');
    status.textContent = 'WhatsApp aberto. Confira a mensagem e confirme o envio.';
  });
  document.querySelector('#internal-copy').addEventListener('click', async function () {
    if (!ready()) return;
    try { await navigator.clipboard.writeText(message()); status.textContent = 'Resumo copiado. Cole na conversa da Expedição.'; }
    catch (error) { status.textContent = 'Não foi possível copiar. Tente novamente em uma conexão segura.'; }
  });
  document.addEventListener('catalog-ready', function () {
    products = window.getCatalogProducts();
    order.items = order.items.filter(function (item) { return Boolean(window.getCatalogProduct(item.code)); });
    renderResults(); renderOrder();
  });
  renderOrder();
})();
