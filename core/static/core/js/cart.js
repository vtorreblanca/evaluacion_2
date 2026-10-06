// Funciones del carrito: solo se aceptan productos conocidos y cantidades de 1 a 99.
(function (root) {
  'use strict';
  function normalize(value, products) {
    const result = {};
    if (!value || typeof value !== 'object' || Array.isArray(value)) return result;
    products.forEach(p => {
      const q = value[p.id];
      if (Number.isInteger(q) && q > 0) result[p.id] = Math.min(99, q);
    });
    return result;
  }
  function update(cart, id, delta, products) {
    const next = normalize(cart, products);
    if (!products.some(p => p.id === id) || !Number.isInteger(delta)) return next;
    const quantity = Math.min(99, (next[id] || 0) + delta);
    if (quantity <= 0) delete next[id]; else next[id] = quantity;
    return next;
  }
  function total(cart, products) {
    const clean = normalize(cart, products);
    return products.reduce((sum, p) => sum + p.price * (clean[p.id] || 0), 0);
  }
  const api = {normalize, update, total};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ShopCart = api;
})(typeof window !== 'undefined' ? window : globalThis);
