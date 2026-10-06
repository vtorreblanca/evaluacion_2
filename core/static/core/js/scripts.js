/* Inacap Shop: interacción de la versión estática. */
'use strict';
const products = window.SHOP_PRODUCTS;
const model = window.ShopCart;
const key = 'inacap-shop-cart-v1';
const dialog = document.querySelector('#cart-dialog');
const items = document.querySelector('#cart-items');
const money = value => new Intl.NumberFormat('es-CL', {style:'currency', currency:'CLP', maximumFractionDigits:0}).format(value);
let cart = {}, noticeTimer, lastFocus;
try { cart = model.normalize(JSON.parse(localStorage.getItem(key)), products); } catch (_) { cart = {}; }
function announce(message) {
  clearTimeout(noticeTimer);
  document.querySelector('#notice').textContent = message;
  noticeTimer = setTimeout(() => {document.querySelector('#notice').textContent = '';}, 3500);
}
function save() {
  try { localStorage.setItem(key, JSON.stringify(cart)); }
  catch (_) { announce('El carrito funciona, pero este navegador no permite guardarlo.'); }
}
function button(text, label, action, id) {
  const node = document.createElement('button');
  node.type = 'button'; node.className = 'btn btn-outline-dark btn-sm';
  node.textContent = text; node.setAttribute('aria-label', label);
  node.dataset.action = action; node.dataset.id = id;
  return node;
}
function render() {
  document.querySelectorAll('[data-count]').forEach(n => n.textContent = Object.values(cart).reduce((a,b) => a+b,0));
  items.replaceChildren();
  const selected = products.filter(p => cart[p.id]);
  if (!selected.length) {
    const empty = document.createElement('p');
    empty.textContent = 'Tu carrito está vacío. Añade un producto desde Inicio.';
    items.append(empty);
  }
  selected.forEach(p => {
    const row = document.createElement('article'); row.className = 'cart-line';
    const image = document.createElement('img'); image.src = p.image; image.alt = p.name;
    const info = document.createElement('div');
    const title = document.createElement('h3'); title.textContent = p.name;
    const price = document.createElement('p'); price.className = 'mb-1';
    price.textContent = `${money(p.price)} × ${cart[p.id]} = ${money(p.price * cart[p.id])}`;
    const controls = document.createElement('div'); controls.className = 'quantity';
    const amount = document.createElement('span'); amount.textContent = `${cart[p.id]} unidad${cart[p.id] === 1 ? '' : 'es'}`;
    const minus = button('−', `Restar una unidad de ${p.name}`, 'minus', p.id);
    const plus = button('+', `Sumar una unidad de ${p.name}`, 'plus', p.id); plus.disabled = cart[p.id] >= 99;
    controls.append(minus, amount, plus, button('Quitar', `Quitar ${p.name}`, 'remove', p.id));
    info.append(title, price, controls); row.append(image, info); items.append(row);
  });
  document.querySelector('#cart-total').textContent = money(model.total(cart, products));
  document.querySelector('#clear-cart').disabled = !selected.length;
}
document.querySelectorAll('[data-add]').forEach(b => b.addEventListener('click', () => {
  const p = products.find(p => p.id === b.dataset.add);
  if (!p) return;
  if (cart[p.id] >= 99) { announce('Máximo de 99 unidades por producto.'); return; }
  cart = model.update(cart, p.id, 1, products); render(); announce(`${p.name} añadido al carrito.`); save();
}));
document.querySelectorAll('[data-open-cart]').forEach(b => b.addEventListener('click', () => {
  lastFocus = b; render(); dialog.showModal();
}));
document.querySelectorAll('[data-close-cart]').forEach(b => b.addEventListener('click', () => dialog.close()));
dialog.addEventListener('close', () => { if (lastFocus) lastFocus.focus(); });
items.addEventListener('click', e => {
  const target = e.target.closest('button[data-action]'); if (!target) return;
  const {id, action} = target.dataset;
  if (action === 'remove') delete cart[id];
  else cart = model.update(cart, id, action === 'plus' ? 1 : -1, products);
  render(); save();
  const replacement = [...items.querySelectorAll('button')].find(b => b.dataset.id === id && b.dataset.action === action && !b.disabled);
  (replacement || items.querySelector('button') || dialog.querySelector('[data-close-cart]')).focus();
});
document.querySelector('#clear-cart').addEventListener('click', () => {
  cart = {}; render(); save(); dialog.querySelector('[data-close-cart]').focus();
});
window.addEventListener('storage', e => {
  if (e.key !== key && e.key !== null) return;
  try { cart = model.normalize(JSON.parse(e.newValue), products); } catch (_) { cart = {}; }
  render();
});
render();
