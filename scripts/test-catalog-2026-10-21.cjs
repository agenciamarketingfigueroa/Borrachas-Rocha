const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync('catalog.js', 'utf8');
const elements = new Map();
const element = id => {
  if (!elements.has(id)) elements.set(id, {innerHTML:'',value:'',showModal(){},addEventListener(){},querySelector(){return {hidden:false};}});
  return elements.get(id);
};
const context = vm.createContext({window:{},document:{querySelector:element,addEventListener(){}},console,Set,Map,URLSearchParams,location:{search:''}});
// Exercita as funções reais de cadastro, imagem, busca e detalhe, sem inicializar a página.
vm.runInContext(source.slice(0,source.indexOf('const init = async')),context);
vm.runInContext(`products = PU_PRODUCTS; productByCode = new Map(products.map(p => [p.code,p]));`,context);
const products = vm.runInContext('PU_PRODUCTS',context);
assert.equal(products.length,143);
assert.equal(new Set(products.map(p=>p.code)).size,143);
const search=q=>vm.runInContext(`state.query=${JSON.stringify(q)}; products.filter(searchMatches).map(p=>p.code)`,context);
for(const p of products.filter(p=>p.originalCode)) for(const code of p.originalCode.split(' / ')) {
  assert(search(code).includes(p.code),`${p.code}: ${code}`);
  assert(search(code.toLowerCase().replace(/[. -]/g,'')).includes(p.code));
}
assert(search('070641170').includes('0614A PU'));
assert(search('3415025').includes('8013 PU'));
assert(search('MR455699').includes('0819 PU'));
assert(search('600511413A').includes('1013A PU'));
assert(search('2031367').includes('6053 PU'));
assert(search('2470850').includes('6053 PU'));
for(const p of products) {
  const image=vm.runInContext(`pathForImage(productByCode.get(${JSON.stringify(p.code)}))`,context);
  assert(image && fs.existsSync(decodeURI(image)),`${p.code}: imagem ausente ${image}`);
}
vm.runInContext(`openProduct('0614A PU')`,context);
assert(element('#dialog-content').innerHTML.includes('070641170'));
assert.equal(products.filter(p=>p.catalog==='amortecedor').length,14);
assert.equal(products.filter(p=>p.catalog==='geral').length,129);
assert.equal(products.find(p=>p.code==='0836 PU').brand,'Mitsubishi');
for(const code of ['1056 PU','2051 PU','2081C PU','2119 PU','8010 PU']) assert(!products.find(p=>p.code===code));
console.log('OK: 143 produtos, 79 referências OEM pesquisáveis, imagens, variantes, detalhes e separação 129/14.');
