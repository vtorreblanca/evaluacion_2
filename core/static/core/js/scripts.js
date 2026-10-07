/* Inacap Shop: interacción del carrito */
'use strict';

window.SHOP_PRODUCTS = window.SHOP_PRODUCTS || [];
const products = window.SHOP_PRODUCTS;
const model = window.ShopCart;
const key = 'inacap-shop-cart-v1';
const dialog = document.querySelector('#cart-dialog');
const items = document.querySelector('#cart-items');
const money = value => new Intl.NumberFormat('es-CL', {style:'currency', currency:'CLP', maximumFractionDigits:0}).format(value);

let cart = {}, noticeTimer, lastFocus;

try { 
  cart = model.normalize(JSON.parse(localStorage.getItem(key)), products); 
} catch (_) { 
  cart = {}; 
}

function announce(message) {
  clearTimeout(noticeTimer);
  const n = document.querySelector('#notice');
  if (n) {
    n.textContent = message;
    noticeTimer = setTimeout(() => { n.textContent = ''; }, 3500);
  }
}

function save() {
  try { 
    localStorage.setItem(key, JSON.stringify(cart)); 
  } catch (_) { 
    announce('El carrito funciona, pero este navegador no permite guardarlo.'); 
  }
}

function button(text, label, action, id) {
  const node = document.createElement('button');
  node.type = 'button'; 
  node.className = 'btn btn-outline-dark btn-sm';
  node.textContent = text; 
  node.setAttribute('aria-label', label);
  node.dataset.action = action; 
  node.dataset.id = id;
  return node;
}

function render() {
  const totalCount = Object.values(cart).reduce((a, b) => a + b, 0);
  document.querySelectorAll('[data-count]').forEach(n => n.textContent = totalCount);
  
  if (!items) return;
  items.replaceChildren();

  const selected = products.filter(p => cart[p.id]);

  if (!selected.length) {
    const empty = document.createElement('p');
    empty.textContent = 'Tu carrito está vacío. Añade un producto desde Inicio.';
    items.append(empty);
  } else {
    selected.forEach(p => {
      const row = document.createElement('article'); 
      row.className = 'cart-line';
      
      const image = document.createElement('img'); 
      image.src = p.image || '/static/core/assets/images.jpeg'; 
      image.alt = p.name;
      
      const info = document.createElement('div');
      const title = document.createElement('h3'); 
      title.textContent = p.name;
      
      const price = document.createElement('p'); 
      price.className = 'mb-1';
      price.textContent = `${money(p.price)} × ${cart[p.id]} = ${money(p.price * cart[p.id])}`;
      
      const controls = document.createElement('div'); 
      controls.className = 'quantity';
      const amount = document.createElement('span'); 
      amount.textContent = `${cart[p.id]} unidad${cart[p.id] === 1 ? '' : 'es'}`;
      
      const minus = button('−', `Restar una unidad de ${p.name}`, 'minus', p.id);
      const plus = button('+', `Sumar una unidad de ${p.name}`, 'plus', p.id); 
      plus.disabled = cart[p.id] >= 99;
      
      controls.append(minus, amount, plus, button('Quitar', `Quitar ${p.name}`, 'remove', p.id));
      info.append(title, price, controls); 
      row.append(image, info); 
      items.append(row);
    });
  }

  const totalEl = document.querySelector('#cart-total');
  if (totalEl) totalEl.textContent = money(model.total(cart, products));
  
  const clearBtn = document.querySelector('#clear-cart');
  if (clearBtn) clearBtn.disabled = !selected.length;
}

// Delegación global para botones "Agregar al carrito"
document.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-add]');
  if (!btn) return;

  const sku = btn.dataset.add;
  let p = products.find(item => item.id === sku);

  // Si no está registrado en products.js, se genera desde el DOM
  if (!p) {
    const card = btn.closest('.product') || btn.closest('.card');
    const name = card?.querySelector('.card-title')?.textContent?.trim() || sku;
    const rawPrice = card?.querySelector('.format-clp-price')?.getAttribute('data-raw-price') || "0";
    const img = card?.querySelector('img')?.getAttribute('src') || '';
    
    p = {
      id: sku,
      name: name,
      price: parseInt(rawPrice, 10) || 0,
      image: img,
      category: 'General'
    };
    products.push(p);
  }

  if (cart[p.id] >= 99) { 
    announce('Máximo de 99 unidades por producto.'); 
    return; 
  }

  cart = model.update(cart, p.id, 1, products); 
  render(); 
  announce(`${p.name} añadido al carrito.`); 
  save();
});

// Abrir carrito
document.querySelectorAll('[data-open-cart]').forEach(b => b.addEventListener('click', () => {
  lastFocus = b; 
  render(); 
  if (dialog) dialog.showModal();
}));

// Cerrar carrito
document.querySelectorAll('[data-close-cart]').forEach(b => b.addEventListener('click', () => {
  if (dialog) dialog.close();
}));

if (dialog) {
  dialog.addEventListener('close', () => { 
    if (lastFocus) lastFocus.focus(); 
  });
}

// Acciones dentro del carrito (+, -, Quitar)
if (items) {
  items.addEventListener('click', e => {
    const target = e.target.closest('button[data-action]'); 
    if (!target) return;
    
    const {id, action} = target.dataset;
    if (action === 'remove') {
      delete cart[id];
    } else {
      cart = model.update(cart, id, action === 'plus' ? 1 : -1, products);
    }
    render(); 
    save();
  });
}

// Vaciar carrito
const clearBtn = document.querySelector('#clear-cart');
if (clearBtn) {
  clearBtn.addEventListener('click', () => {
    cart = {}; 
    render(); 
    save(); 
    if (dialog) dialog.querySelector('[data-close-cart]')?.focus();
  });
}

window.addEventListener('storage', e => {
  if (e.key !== key && e.key !== null) return;
  try { 
    cart = model.normalize(JSON.parse(e.newValue), products); 
  } catch (_) { 
    cart = {}; 
  }
  render();
});

// Render inicial
document.addEventListener('DOMContentLoaded', render);
render();
