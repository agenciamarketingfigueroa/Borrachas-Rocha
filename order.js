/* Pedido local: nenhum dado é enviado até o cliente abrir o WhatsApp. */
(function () {
  const STORAGE_KEY = 'borrachas-rocha-order-v1';
  const WHATSAPP_NUMBER = '5531996165270';
  const customerFields = ['name', 'street', 'number', 'zip', 'complement', 'city', 'state'];
  const cartDialog = document.querySelector('#cart-dialog');
  const productDialog = document.querySelector('#product-dialog');
  const form = document.querySelector('#cart-form');
  const itemsElement = document.querySelector('#cart-items');
  let order = loadOrder();

  function cleanText(value, limit) {
    return String(value || '').slice(0, limit || 300);
  }
  function html(value) {
    return cleanText(value, 500).replace(/[&<>"']/g, function (char) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[char];
    });
  }
  function quantity(value) {
    const number = Number(value);
    return Number.isFinite(number) ? Math.max(0, Math.min(9999, Math.floor(number))) : 0;
  }
  function emptyOrder() {
    return { items: [], customer: Object.fromEntries(customerFields.map(function (key) { return [key, '']; })) };
  }
  function loadOrder() {
    const fresh = emptyOrder();
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (!stored || !Array.isArray(stored.items)) return fresh;
      fresh.customer = Object.fromEntries(customerFields.map(function (key) {
        return [key, cleanText(stored.customer && stored.customer[key], 300)];
      }));
      fresh.items = stored.items.slice(0, 100).filter(function (item) {
        return item && typeof item.code === 'string' && Array.isArray(item.options);
      }).map(function (item) {
        return {
          code: cleanText(item.code, 50),
          name: cleanText(item.name, 300),
          brand: cleanText(item.brand, 80),
          material: cleanText(item.material, 30),
          image: /^assets\/img\//.test(item.image || '') ? cleanText(item.image, 500) : '',
          options: item.options.slice(0, 12).map(function (option) {
            return {
              key: cleanText(option.key, 60),
              label: option.label === 'Conforme código da peça' ? 'Quantidade de peças' : cleanText(option.label, 110),
              orderCode: cleanText(option.orderCode, 50),
              qty: quantity(option.qty)
            };
          })
        };
      });
    } catch (error) {
      return fresh;
    }
    return fresh;
  }
  function saveOrder() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(order)); }
    catch (error) { document.querySelector('#cart-save-note').textContent = 'Este navegador não permitiu salvar o pedido.'; }
  }
  function optionsFor(product) {
    if (product.code === 'BR-5015') {
      return [
        { key:'BR-5015', label:'Interno Ø 30,0 mm', orderCode:'BR-5015', qty:0 },
        { key:'BR-5015A', label:'Interno Ø 32,0 mm', orderCode:'BR-5015A', qty:0 }
      ];
    }
    const name = String(product.name || '');
    const pattern = /\b(BR-\d+[A-Z]?|[A-E])\s*:?\s*((?:(?:diâmetro|diametro)\s+)?(?:interno|externo|pino)?\s*(?:ø|Ø|⌀)?\s*\d+(?:[.,]\d+)?\s*mm(?:\s*(?:de\s*)?altura)?)/gi;
    const found = [];
    let match;
    while ((match = pattern.exec(name)) !== null) {
      const key = match[1].toUpperCase();
      const measure = match[2].replace(/\s+/g, ' ').trim();
      if (!found.some(function (option) { return option.key === key; })) {
        found.push({
          key: key,
          label: (key.startsWith('BR-') ? key : 'Opção ' + key) + ' · ' + measure,
          orderCode: key.startsWith('BR-') ? key : product.code,
          qty: 0
        });
      }
    }
    if (found.length > 1) return found;
    const measurements = name.match(/(?:interno|externo|altura|pino)\s*(?:ø|Ø|⌀|:)?\s*\d+(?:[.,]\d+)?\s*mm/gi) || [];
    const label = measurements.length === 1 ? measurements[0].replace(/\s+/g, ' ').trim() : 'Quantidade de peças';
    return [{ key:'standard', label:label, orderCode:product.code, qty:1 }];
  }
  function totalQuantity() {
    return order.items.reduce(function (sum, item) {
      return sum + item.options.reduce(function (itemSum, option) { return itemSum + option.qty; }, 0);
    }, 0);
  }
  function displayName(value) {
    const name = cleanText(value, 300);
    const beforeMeasure = name.split(/\b(?:[A-E]\s*:?\s*)?(?:interno|externo|diâmetro|diametro|altura|pino)\s*(?:ø|Ø|⌀)?\s*\d/i)[0].replace(/\b[A-E]\s*:?\s*$/, '').trim();
    const result = beforeMeasure.length >= 12 ? beforeMeasure : name;
    return result.length > 105 ? result.slice(0, 102).trimEnd() + '…' : result;
  }
  function imageFor(item) {
    const current = window.getCatalogProductImage && window.getCatalogProductImage(item.code);
    return current || item.image || '';
  }
  function render() {
    const total = totalQuantity();
    const count = document.querySelector('#cart-count');
    count.textContent = String(total);
    document.querySelector('#cart-toggle').setAttribute('aria-label', 'Abrir pedido com ' + total + ' peças');
    document.querySelector('#cart-total').textContent = total + ' ' + (total === 1 ? 'peça no pedido' : 'peças no pedido');
    document.querySelector('#cart-submit').disabled = total === 0;
    document.querySelector('#cart-clear').disabled = order.items.length === 0 && !customerFields.some(function (key) { return order.customer[key]; });
    itemsElement.innerHTML = order.items.length ? order.items.map(function (item, itemIndex) {
      const src = imageFor(item);
      const photo = (src ? '<img src="' + html(src) + '" alt="" loading="lazy" />' : '') + '<span class="cart-photo-fallback"' + (src ? ' hidden' : '') + '>Sem foto</span>';
      return '<article class="cart-item"><div class="cart-item-head"><div class="cart-item-photo">' + photo + '</div><div class="cart-item-details"><div class="cart-item-identifiers"><span class="cart-item-code" aria-label="Código da peça: ' + html(item.code) + '">' + html(item.code) + '</span><span class="cart-item-brand" aria-label="Montadora: ' + html(item.brand) + '">' + html(item.brand) + '</span></div><h3>' + html(displayName(item.name)) + '</h3><span class="cart-item-material">' + html(item.material) + '</span></div><button class="cart-remove" type="button" data-remove-item="' + itemIndex + '" aria-label="Remover ' + html(item.code) + '">×</button></div><div class="cart-options">' +
        item.options.map(function (option, optionIndex) {
          return '<label class="cart-option"><span>' + html(option.label) + '</span><input type="number" min="0" max="9999" step="1" inputmode="numeric" value="' + option.qty + '" data-item-index="' + itemIndex + '" data-option-index="' + optionIndex + '" aria-label="Quantidade de ' + html(item.code) + ', ' + html(option.label) + '" /></label>';
        }).join('') + '</div>' +
        (item.options.length > 1 && !item.options.some(function (option) { return option.qty > 0; }) ? '<p class="cart-hint">Informe a quantidade desejada em cada medida.</p>' : '') +
      '</article>';
    }).join('') : '<div class="cart-empty"><strong>Seu pedido está vazio.</strong><p>Abra uma peça do catálogo e clique em “Adicionar ao pedido”.</p></div>';
  }
  function openCart() {
    render();
    if (!cartDialog.open) cartDialog.showModal();
  }
  function addProduct(code) {
    const product = window.getCatalogProduct && window.getCatalogProduct(code);
    if (!product) return;
    const existing = order.items.find(function (item) { return item.code === code; });
    if (existing) {
      if (existing.options.length === 1) existing.options[0].qty = quantity(existing.options[0].qty + 1);
    } else {
      order.items.push({
        code: product.code,
        name: product.name,
        brand: product.brand,
        material: product.material,
        image: window.getCatalogProductImage ? window.getCatalogProductImage(code) : '',
        options: optionsFor(product)
      });
    }
    saveOrder();
    if (productDialog.open) productDialog.close();
    openCart();
  }
  function whatsappMessage() {
    const lines = ['*PEDIDO — BORRACHAS ROCHA*', '', '*Peças solicitadas:*'];
    order.items.forEach(function (item) {
      const selected = item.options.filter(function (option) { return option.qty > 0; });
      if (!selected.length) return;
      lines.push('', '*' + item.code + ' — ' + displayName(item.name) + '*', '*Montadora:* ' + item.brand + ' | *Material:* ' + item.material);
      selected.forEach(function (option) {
        const detail = option.label === 'Quantidade de peças' ? '' : ' — ' + option.label;
        lines.push('• ' + option.qty + ' un.' + detail + (option.orderCode !== item.code ? ' | *Código:* ' + option.orderCode : ''));
      });
    });
    lines.push('', '*Total de peças:* ' + totalQuantity(), '', '*Cliente:* ' + order.customer.name,
      '', '*Endereço de entrega:*',
      '*Rua:* ' + order.customer.street,
      '*Número:* ' + order.customer.number,
      '*CEP:* ' + order.customer.zip);
    if (order.customer.complement) lines.push('*Complemento:* ' + order.customer.complement);
    lines.push('*Cidade:* ' + order.customer.city,
      '*Estado:* ' + order.customer.state.toUpperCase());
    return lines.join('\n');
  }

  customerFields.forEach(function (key) {
    const input = form.elements.namedItem(key);
    input.value = order.customer[key];
    input.addEventListener('input', function () {
      order.customer[key] = input.value;
      saveOrder();
      document.querySelector('#cart-clear').disabled = false;
    });
  });
  document.querySelector('#cart-toggle').addEventListener('click', openCart);
  document.querySelector('#cart-close').addEventListener('click', function () { cartDialog.close(); });
  document.querySelector('#cart-clear').addEventListener('click', function () {
    if (!window.confirm('Limpar todas as peças e os dados deste pedido?')) return;
    order = emptyOrder();
    customerFields.forEach(function (key) { form.elements.namedItem(key).value = ''; });
    saveOrder();
    render();
  });
  document.querySelector('#product-dialog').addEventListener('click', function (event) {
    const button = event.target.closest('[data-add-product]');
    if (button) addProduct(button.dataset.addProduct);
  });
  itemsElement.addEventListener('click', function (event) {
    const button = event.target.closest('[data-remove-item]');
    if (!button) return;
    order.items.splice(Number(button.dataset.removeItem), 1);
    saveOrder();
    render();
  });
  itemsElement.addEventListener('error', function (event) {
    if (!event.target.matches('.cart-item-photo img')) return;
    event.target.hidden = true;
    event.target.parentNode.querySelector('.cart-photo-fallback').hidden = false;
  }, true);
  itemsElement.addEventListener('input', function (event) {
    const input = event.target.closest('[data-option-index]');
    if (!input) return;
    const item = order.items[Number(input.dataset.itemIndex)];
    const option = item && item.options[Number(input.dataset.optionIndex)];
    if (!option) return;
    option.qty = quantity(input.value);
    saveOrder();
    const hint = input.closest('.cart-item').querySelector('.cart-hint');
    if (hint) hint.hidden = item.options.some(function (entry) { return entry.qty > 0; });
    const total = totalQuantity();
    document.querySelector('#cart-count').textContent = String(total);
    document.querySelector('#cart-total').textContent = total + ' ' + (total === 1 ? 'peça no pedido' : 'peças no pedido');
    document.querySelector('#cart-submit').disabled = total === 0;
  });
  itemsElement.addEventListener('change', function (event) {
    const input = event.target.closest('[data-option-index]');
    if (input) { input.value = String(quantity(input.value)); render(); }
  });
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (totalQuantity() === 0) return;
    customerFields.forEach(function (key) { order.customer[key] = form.elements.namedItem(key).value.trim(); });
    saveOrder();
    const url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(whatsappMessage());
    window.open(url, '_blank', 'noopener,noreferrer');
  });
  document.addEventListener('catalog-ready', render);
  render();
})();
