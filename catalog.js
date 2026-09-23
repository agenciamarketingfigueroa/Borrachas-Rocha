/* Catálogo gerado a partir das aplicações dos catálogos Borrachas Rocha. */
const RUBBER_PAYLOAD = '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';

const PU_PRODUCTS = [
  ['1026 PU','Volkswagen','Bucha do feixe de mola dianteira','VW 6.90 / 8.100 / 8.120 / 8.150'],
  ['1030 PU','Volkswagen','Calço do feixe de molas','VW L80 / 6.90 / 7.90 / 7.100 / 7.110 / 8.100 / 8.150 e MB Accelo'],
  ['1046A PU','Agrale','Bucha do quarto eixo traseiro','HBZ'],
  ['1048 PU','Volkswagen','Bucha central da barra estabilizadora dianteira','VW 9.170 / 11.180 Delivery 2018 em diante'],
  ['1048A PU','Volkswagen','Bucha central da barra estabilizadora traseira','VW 9.170 / 11.180 Delivery 2018 em diante'],
  ['1053 PU','Volkswagen','Bucha da ponta da barra estabilizadora traseira','VW 11.180 / 9.170 / Delivery'],
  ['1061 PU','Volkswagen','Bucha do feixe de molas e suporte traseiro','VW 9.170 / 11.180 Delivery 2018 em diante'],
  ['1062 PU','Volkswagen','Bucha do feixe de molas e suporte traseiro','VW 6.160 / 4.150 / 4.160 / Express 2018 em diante'],
  ['2062 PU','Mercedes','Bucha do feixe de molas dianteiro','MB Atego'],
  ['2063A PU','Mercedes','Bucha do feixe de molas dianteiro - parte traseira','MB Atego'],
  ['2063B PU','Mercedes','Bucha do feixe de molas dianteiro - parte traseira','MB Atego'],
  ['2063C PU','Mercedes','Bucha do feixe de molas dianteiro - parte traseira','MB Atego'],
  ['2074A PU','Mercedes','Bucha do suporte da mola dianteira','MB Atego / Sprinter'],
  ['2074B PU','Mercedes','Bucha do suporte da mola dianteira','MB Atego / Sprinter'],
  ['2074C PU','Mercedes','Bucha do suporte da mola dianteira','MB Atego'],
  ['2078A PU','Mercedes','Bucha do suporte da mola dianteira e traseira','MB Accelo 815 / 915 / 1016'],
  ['2081B PU','Mercedes','Bucha do feixe de mola traseira','MB Atego'],
  ['2108 PU','Mercedes','Bucha da barra estabilizadora dianteira','MB Actros 2031 / 2655 / 33315'],
  ['2112 PU','Mercedes','Bucha da ponta da barra estabilizadora dianteira','MB Actros / Axor'],
  ['2114 PU','Mercedes','Bucha da ponta da barra estabilizadora traseira','MB Actros / Axor'],
  ['0627 PU','Iveco','Bucha da barra de torção dianteira','Iveco Daily 70C16 / 70C17 / 70C17 HD 65-170 / 70-170 / 2019 em diante'],
  ['0628 PU','Iveco','Bucha da barra de torção dianteira','Iveco Daily 70C16 / 70C17 / 70C17 HD 65-170 / 70-170 / 2019 em diante'],
  ['0630 PU','Iveco','Kit de buchas da barra de torção dianteira','Iveco Daily 35-140 / 35-13 / 38-13 / 40-12 / 40-13 / 49-10 / 49-12 / 50-13 / 59-12'],
  ['0631 PU','Iveco','Bucha superior da barra de torção dianteira','Iveco Daily 35-140 / 35-13 / 38-13 / 40-12 / 40-13 / 49-10 / 49-12'],
  ['0632 PU','Iveco','Bucha inferior da barra de torção dianteira','Iveco Daily 35-140 / 35-13 / 38-13 / 40-12 / 40-13 / 49-10 / 49-12'],
  ['0633 PU','Iveco','Bucha superior da barra de torção dianteira','Iveco Daily 35-140 / 35-13 / 38-13 / 40-12 / 40-13 / 49-10 / 49-12'],
  ['6002 PU','Scania','Bucha da barra estabilizadora dianteira','Scania 124'],
  ['6052 PU','Scania','Bucha do feixe de molas parte traseira','Scania suspensão a ar'],
  ['7010 PU','Volvo','Bucha do feixe de molas dianteiro','Volvo VM 240 / 260'],
  ['7014 PU','Volvo','Bucha do feixe de molas dianteiro','Volvo VM 240 / 260 / 330'],
  ['8011 PU','Randon','Bucha do tensor do motor','Randon 2300'],
  ['8024 PU','Suspensys','Bucha da balança','Suspensys'],
  ['3056 PU','Ford','Bucha inferior do amortecedor dianteiro','Ranger 2012 a 2022'],
  ['3058 PU','Ford','Bucha inferior do amortecedor dianteiro','Ranger 2012 a 2022'],
  ['5021 PU','Toyota','Bucha inferior do amortecedor dianteiro','Hilux 2005 a 2022'],
  ['5022 PU','Toyota','Bucha inferior do amortecedor dianteiro','Hilux 2005 a 2022'],
  ['5023 PU','Toyota','Bucha inferior do amortecedor dianteiro','Hilux 2005 a 2022'],
  ['5029 PU','Toyota','Bucha inferior do amortecedor dianteiro','Hilux 2005 a 2022'],
  ['9028 PU','Chevrolet','Bucha inferior do amortecedor dianteiro','S10 2012 a 2022'],
  ['0828 PU','Mitsubishi','Bucha inferior do amortecedor dianteiro','L200 Triton 2008 a 2022'],
  ['0828A PU','Mitsubishi','Bucha inferior do amortecedor dianteiro','L200 Triton 2008 a 2022'],
  ['0828C PU','Mitsubishi','Bucha inferior do amortecedor dianteiro','Pajero / L200 Triton 2008 a 2022'],
  ['0912 PU','Nissan Frontier','Bucha inferior do amortecedor dianteiro','Frontier 2008 a 2022'],
  ['0912A PU','Nissan Frontier','Bucha inferior do amortecedor dianteiro','Frontier 2008 a 2022'],
  ['6058 PU','Scania','Separador anti ruído da mola dianteira','Scania NTG 2019 em diante','Comprimento: 100 mm | Largura: 90 mm | Entre pinos: 45 mm','6058 PU.jpg'],
  ['8002 PU','Rodoviária','Borracha rodoviária com aba','','Altura: 50 mm | Diâmetro: 62 mm | Interno do furo: 36 mm','8002 PU.jpg'],
  ['8003 PU','Randon','Borracha Randon sem aba','','Altura: 50 mm | Diâmetro: 71 mm | Interno do furo: 38 mm','8003 PU.jpg'],
  ['6057 PU','Scania','Bucha tranca da cabine traseira','Scania NTG 2019 em diante','','6057 PU.jpg'],
  ['8001 PU','Rodoviária','Borracha rodoviária sem aba','','Altura: 50 mm | Diâmetro: 62 mm | Interno do furo: 36 mm','8001 PU.jpg'],
  ['8004 PU','Randon','Borracha Randon com aba','','Altura: 50 mm | Diâmetro: 71 mm | Interno do furo: 38 mm','8004 PU.jpg'],
  ['8023 PU','Jost','Coxim da 5ª roda (2 polegadas)','Jost','','8023 PU.jpg'],
  ['5003 PU','Toyota','Borracha da mola dianteira','Toyota Band 1992 em diante','','5003 PU.jpg'],
  ['5004 PU','Toyota','Borracha da mola traseira','Toyota Band 1992 em diante','','5004 PU.jpg'],
  ['0611D PU','Iveco','Bucha da barra estabilizadora dianteira','Iveco Tector / Stralis','Comprimento total: 82 mm | Diâmetro do corpo: 70 mm | Entre abas: 71 mm | Interno do furo: 48 mm','0611D PU.jpg'],
  ['3079 PU','Ford','Borracha do amortecedor dianteiro inferior','Ranger','Comprimento: 50 mm | Diâmetro externo: 54 mm | Interno do furo: 20 mm','3079 PU.jpg'],
  ['3039 PU','Ford','Borracha da ponta estabilizadora dianteira','Ford 815','Comprimento: 45 mm | Diâmetro externo: 34 mm | Interno do furo: 12 mm','3039 PU.jpg'],
  ['0616A PU','Iveco','Bucha da mola e suporte traseiro','Iveco Daily; aplicar em mola com 70 mm de largura','Comprimento: 80 mm | Diâmetro: 40 mm | Interno do furo: 16 mm','0616A PU.jpg'],
  ['0610A PU','Iveco','Bucha da ponta estabilizadora dianteira','Iveco Stralis','Comprimento: 50 mm | Diâmetro: 61 mm | Interno do furo: 28 mm','0610A PU.jpg'],
  ['0836 PU','Iveco','Bucha da mola dianteira e traseira','Iveco ônibus Mascarello','Comprimento: 80 mm | Diâmetro: 60 mm | Interno do furo: 16 mm','0836 PU.jpg'],
  ['1024 PU','Volkswagen','Bucha da barra estabilizadora dianteira','VW 13.190','Interno do furo: 35 mm','1024 PU.jpg'],
  ['1014 PU','Volkswagen','Borracha da barra estabilizadora dianteira','VW 12.140 - 24.250','Interno do furo: 44 mm','1014 PU.jpg'],
  ['1013 PU','Volkswagen','Borracha da barra estabilizadora traseira','VW 6.90 - 8.150','Interno do furo: 32 mm','1013 PU.jpg'],
  ['1013A PU','Volkswagen','Borracha da barra estabilizadora traseira','VW 6.90 - 8.150','Interno do furo: 30 mm',''],
  ['1055 PU','Volkswagen','Bucha silenciosa da mola traseira','VW 11.180 - Delivery','Comprimento: 88 mm | Diâmetro externo: 53 mm | Interno do furo: 18 mm','1055 PU.jpg'],
  ['1011 PU','Volkswagen','Borracha da ponta estabilizadora dianteira','VW 12.140 - 24.250','Olhal: 43 mm','1011 PU.jpg'],
  ['1068 PU','Volkswagen','Bucha da barra estabilizadora dianteira superior','VW Meteor','Comprimento: 60 mm | Diâmetro externo (olhal): 65 mm | Interno do furo: 37 mm','1068 PU.jpg'],
  ['1067 PU','Volkswagen','Bucha da barra estabilizadora dianteira inferior','VW Meteor','Altura: 60 mm | Diâmetro externo: 85 mm | Interno do furo: 49 mm','1067 PU.jpg'],
  ['1008 PU','Volkswagen','Borracha estabilizadora dianteira','VW 6.90 - 8.150','Olhal: 28 mm','1008 PU.jpg'],
  ['1010 PU','Volkswagen','Borracha da ponta estabilizadora traseira','VW 6.90 - 8.150','Olhal: 35 mm','1010 PU.jpg'],
  ['1069 PU','Volkswagen','Bucha da ponta estabilizadora dianteira','VW Meteor','Comprimento: 64 mm | Diâmetro externo: 58 mm | Interno do furo: 20 mm','1069 PU.jpg'],
  ['2010 PU','Mercedes','Borracha da barra estabilizadora com tubo dianteiro/traseiro','MB 710','Olhal: 30 mm','2010 PU.jpg'],
  ['2008 PU','Mercedes','Borracha da barra estabilizadora com tubo dianteiro/traseiro','MB 608','Olhal: 26 mm','2008 PU.jpg'],
  ['2095 PU','Mercedes','Batente guia do grampo da mola dianteira','MB Axor (fora de estrada)','Altura: 109 mm','2095 PU.jpg'],
  ['2039 PU','Mercedes','Borracha da mola dianteira','MB 608','','2039 PU.jpg'],
  ['2054 PU','Mercedes','Borracha da mola da cabine','MB 1620','','2054 PU.jpg'],
  ['2078C PU','Mercedes','Bucha silenciosa do olho da mola traseira/dianteira','MB Accelo','','2078C PU.jpg'],
  ['2120 PU','Mercedes','Bucha da ponta estabilizadora traseira inferior','MB Arocs','','2120 PU.jpg'],
  ['2121 PU','Mercedes','Bucha da ponta estabilizadora dianteira inferior','MB Arocs','Comprimento: 57 mm | Diâmetro do olhal: 75 mm | Interno do furo: 20 mm','2121 PU.jpg']
].map(function (item) {
  return { code:item[0], brand:item[1], name:item[2], application:item[3], specs:item[4] || '', material:'PU', image:item[5] === undefined ? item[0] + '.png' : item[5] };
});

const state = { query:'', brand:'', material:'', year:'', limit:24, sort:'relevance' };
let products = [];
let productByCode = new Map();
window.getCatalogProduct = function (code) { return productByCode.get(code); };
window.getCatalogProducts = function () { return products.slice(); };
const $ = function (selector) { return document.querySelector(selector); };
const normalize = function (value) {
  return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
};
const escapeHtml = function (value) {
  return String(value || '').replace(/[&<>"']/g, function (char) {
    return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'})[char];
  });
};
const SITE_CUTOUT_CODES = new Set([
  '0610A PU','0611D PU','0616A PU','0828C PU','1008 PU','1010 PU','1011 PU',
  '1013 PU','1014 PU','1024 PU','1055 PU','1067 PU','1068 PU','1069 PU',
  '2008 PU','2010 PU','2039 PU','2054 PU','2078C PU','2095 PU','2120 PU',
  '2121 PU','3039 PU','3079 PU','5003 PU','5004 PU','6057 PU','6058 PU',
  '8001 PU','8002 PU','8003 PU','8004 PU','8023 PU'
]);
const pathForImage = function (product) {
  if (SITE_CUTOUT_CODES.has(product.code)) return encodeURI('assets/img/Peças de PU/recortes/' + product.code + '.png');
  if (!product.image) return '';
  if (product.material === 'PU') return encodeURI('assets/img/Peças de PU/' + product.image);
  return encodeURI('assets/img/Peças de Borracha/' + product.image);
};
window.getCatalogProductImage = function (code) {
  const product = productByCode.get(code);
  return product ? pathForImage(product) : '';
};
const decodeCatalog = async function () {
  const binary = atob(RUBBER_PAYLOAD);
  const bytes = Uint8Array.from(binary, function (char) { return char.charCodeAt(0); });
  if (!('DecompressionStream' in window)) throw new Error('Navegador sem descompressão');
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  return new Response(stream).json();
};
const getBrands = function () {
  return Array.from(new Set(products.map(function (product) { return product.brand; }))).sort(function(a,b) {
    return a.localeCompare(b, 'pt-BR');
  });
};
const BRAND_LOGOS = {
  'Agrale':'Agrale.png', 'Chevrolet':'Chevrolet.png', 'Fiat Ducato':'Fiat.svg',
  'Ford':'Ford.png', 'Hyundai':'Hyundai.svg', 'Iveco':'Iveco.png',
  'Jost':'JOST.png', 'Kia':'Kia.svg', 'Mercedes':'Mercedes-Benz.png',
  'Mercedes-Benz Sprinter':'Mercedes-Benz.png', 'Mitsubishi':'Mitsubishi.png',
  'Nissan Frontier':'Nissan.png', 'Randon':'Randon.png', 'Scania':'Scania.png',
  'Suspensys':'Suspensys.png', 'Toyota':'Toyota.png', 'Volkswagen':'Volkswagen.png',
  'Volvo':'Volvo.png'
};
const fillSelect = function (selector, label) {
  const select = $(selector);
  const active = select.value;
  select.innerHTML = '<option value="">' + label + '</option>' + getBrands().map(function (brand) {
    return '<option value="' + escapeHtml(brand) + '">' + escapeHtml(brand) + '</option>';
  }).join('');
  select.value = active;
};
const yearMatches = function (product, year) {
  if (!year) return true;
  const years = (product.application.match(/\b(19|20)\d{2}\b/g) || []).map(Number);
  if (!years.length) return true;
  const requested = Number(year);
  if (/em diante/i.test(product.application)) return requested >= years[0];
  if (years.length >= 2 && /\b(a|ao|até|ate|em diante)\b/i.test(product.application)) {
    const first = Math.min.apply(null, years), last = Math.max.apply(null, years);
    return requested >= first && requested <= last;
  }
  return years.includes(requested);
};
const searchMatches = function (product) {
  const terms = normalize(state.query).replace(/\b(19|20)\d{2}\b/g, ' ').replace(/\bbr\b/g, ' ').split(/\s+/).filter(function(term){ return term.length > 1; });
  const haystack = normalize([product.code, product.brand, product.name, product.application, product.specs].join(' '));
  const implicitYear = (state.query.match(/\b(19|20)\d{2}\b/) || [])[0];
  return terms.every(function (term) { return haystack.includes(term); }) && yearMatches(product, state.year || implicitYear);
};
const filteredProducts = function () {
  const filtered = products.filter(function(product) {
    return (!state.brand || product.brand === state.brand) && (!state.material || product.material === state.material) && yearMatches(product, state.year) && searchMatches(product);
  });
  return filtered.sort(function(a,b) {
    if (state.sort === 'code') return a.code.localeCompare(b.code, 'pt-BR', {numeric:true});
    if (state.sort === 'name') return a.name.localeCompare(b.name, 'pt-BR');
    const aScore = normalize(a.code + ' ' + a.name).indexOf(normalize(state.query)) === 0 ? 0 : 1;
    const bScore = normalize(b.code + ' ' + b.name).indexOf(normalize(state.query)) === 0 ? 0 : 1;
    return aScore - bScore || a.code.localeCompare(b.code, 'pt-BR', {numeric:true});
  });
};
const productCard = function (product) {
  const src = pathForImage(product);
  const photo = src
    ? '<img src="' + src + '" alt="' + escapeHtml(product.name) + '" loading="lazy" onerror="this.remove();this.parentNode.querySelector(\'.image-fallback\').hidden=false" /><span class="image-fallback" hidden>' + escapeHtml(product.code.replace('BR-','')) + '</span>'
    : '<span class="image-fallback">' + escapeHtml(product.code.replace('BR-','')) + '</span>';
  return '<article class="product-card" tabindex="0" role="button" data-code="' + escapeHtml(product.code) + '" aria-label="Ver detalhes de ' + escapeHtml(product.code) + '"><div class="product-photo ' + (product.material === 'PU' ? 'pu' : '') + '">' + photo + '<span class="material-badge ' + (product.material === 'PU' ? 'pu' : '') + '">' + (product.material === 'PU' ? 'PU' : 'BORRACHA') + '</span></div><div class="product-copy"><span class="product-code">' + escapeHtml(product.code) + '</span><h3>' + escapeHtml(product.name) + '</h3><div class="product-brand">' + escapeHtml(product.brand) + '</div></div></article>';
};
const renderChips = function () {
  $('#brand-chips').innerHTML = getBrands().map(function(brand) {
    const logo = BRAND_LOGOS[brand];
    const image = logo ? '<img class="brand-chip-logo" src="' + encodeURI('assets/img/montadoras/' + logo) + '" alt="" loading="lazy" decoding="async" />' : '';
    return '<button class="brand-chip ' + (state.brand === brand ? 'active' : '') + '" type="button" data-brand="' + escapeHtml(brand) + '" aria-pressed="' + (state.brand === brand) + '">' + image + '<span class="brand-chip-label">' + escapeHtml(brand) + '</span></button>';
  }).join('');
};
const render = function (resetLimit) {
  if (resetLimit) state.limit = 24;
  const matches = filteredProducts();
  const shown = matches.slice(0, state.limit);
  $('#result-count').textContent = matches.length + ' ' + (matches.length === 1 ? 'peça encontrada' : 'peças encontradas');
  $('#product-grid').innerHTML = shown.length ? shown.map(productCard).join('') : '<div class="empty-state"><strong>Nenhuma peça encontrada.</strong><br />Tente outro modelo, código ou remova os filtros.</div>';
  $('#load-more').hidden = shown.length >= matches.length;
  $('#clear-filters').hidden = !state.query && !state.brand && !state.material && !state.year;
  $('#active-filters').innerHTML = [
    state.query && 'Busca: ' + state.query,
    state.brand,
    state.material,
    state.year && 'Ano: ' + state.year
  ].filter(Boolean).map(function(label){ return '<span class="active-filter">' + escapeHtml(label) + '</span>'; }).join('');
  renderChips();
};
const syncControls = function () {
  $('#search').value = state.query; $('#brand').value = state.brand; $('#brand-side').value = state.brand;
  $('#material').value = state.material; $('#material-side').value = state.material;
  $('#year').value = state.year; $('#year-side').value = state.year; $('#sort').value = state.sort;
};
const applyFilters = function (reset) { syncControls(); render(reset); };
const openProduct = function (code) {
  const product = productByCode.get(code);
  if (!product) return;
  const src = pathForImage(product);
  const image = src ? '<img src="' + src + '" alt="' + escapeHtml(product.name) + '" />' : '<span class="image-fallback">' + escapeHtml(product.code) + '</span>';
  const application = product.application ? '<p><strong>Aplicação:</strong><br />' + escapeHtml(product.application) + '</p>' : '';
  const specs = product.specs ? '<p><strong>Medidas:</strong><br />' + product.specs.split(' | ').map(escapeHtml).join('<br />') + '</p>' : '';
  $('#dialog-content').innerHTML = '<div class="dialog-inner"><div class="dialog-image">' + image + '</div><div class="dialog-copy"><span class="dialog-code">' + escapeHtml(product.code) + '</span><h2>' + escapeHtml(product.name) + '</h2><p class="dialog-material">' + escapeHtml(product.material === 'PU' ? 'Poliuretano de alta performance' : 'Linha de borracha') + ' · ' + escapeHtml(product.brand) + '</p>' + application + specs + '<button class="add-to-order" type="button" data-add-product="' + escapeHtml(product.code) + '">Adicionar ao pedido <span aria-hidden="true">→</span></button></div></div>';
  $('#product-dialog').showModal();
};
const bind = function () {
  $('#search-form').addEventListener('submit', function(event) { event.preventDefault(); state.query = $('#search').value.trim(); state.brand = $('#brand').value; state.material = $('#material').value; state.year = $('#year').value.replace(/\D/g,'').slice(0,4); applyFilters(true); document.querySelector('#catalogo').scrollIntoView({behavior:'smooth'}); });
  [['#brand','#brand-side','brand'],['#material','#material-side','material'],['#year','#year-side','year']].forEach(function(item) {
    $(item[0]).addEventListener('change', function(event) { state[item[2]] = event.target.value; applyFilters(true); });
    $(item[1]).addEventListener('change', function(event) { state[item[2]] = event.target.value; applyFilters(true); });
  });
  $('#sort').addEventListener('change', function(event) { state.sort = event.target.value; render(false); });
  $('#brand-chips').addEventListener('click', function(event) { const button = event.target.closest('[data-brand]'); if (!button) return; state.brand = button.dataset.brand; applyFilters(true); document.querySelector('#catalogo').scrollIntoView({behavior:'smooth'}); });
  $('#load-more').addEventListener('click', function(){ state.limit += 24; render(false); });
  $('#clear-filters').addEventListener('click', function(){ state.query='';state.brand='';state.material='';state.year='';applyFilters(true); });
  $('#product-grid').addEventListener('click', function(event){ const card = event.target.closest('[data-code]'); if (card) openProduct(card.dataset.code); });
  $('#product-grid').addEventListener('keydown', function(event){ if ((event.key === 'Enter' || event.key === ' ') && event.target.dataset.code) { event.preventDefault(); openProduct(event.target.dataset.code); } });
  $('.dialog-close').addEventListener('click', function(){ $('#product-dialog').close(); });
};
const init = async function () {
  try {
    const rubber = await decodeCatalog();
    products = rubber.concat(PU_PRODUCTS);
  } catch (error) {
    products = PU_PRODUCTS;
    if ($('#result-count')) $('#result-count').textContent = 'Não foi possível carregar a linha de borracha neste navegador.';
  }
  productByCode = new Map(products.map(function(product) { return [product.code, product]; }));
  if ($('#search-form')) {
    fillSelect('#brand', 'Todas as montadoras'); fillSelect('#brand-side', 'Todas');
    bind(); render(true);
  }
  document.dispatchEvent(new Event('catalog-ready'));
};
init();
