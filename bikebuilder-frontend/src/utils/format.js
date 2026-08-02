export const titleCase = s =>
    String(s).replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

export const money = n => `$${(parseFloat(n) || 0).toFixed(2)}`;

export const sumPrice = components =>
    components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);

export const sumWeight = components =>
    components.reduce((sum, c) => sum + (parseFloat(c.weight_grams) || 0), 0);
