import React, { useState } from "react";

const AddAsset = ({ onSave }) => {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [price, setPrice] = useState(1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (symbol && quantity > 0 && price > 0) {
      onSave({ symbol, quantity, price });
      setPrice(1);
      setQuantity(1);
      setSymbol("");

    }
  };

  return (
    <div className="add-asset-container">
      <h3>Aggiungi Asset</h3>
      <form onSubmit={handleSubmit} className="add-asset-form">
        <div className="input-group">
          <label htmlFor="symbol">Simbolo:</label>
          <input
            type="text"
            placeholder="Simbolo dell'asset"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="quantity">Quantità:</label>
          <input
            type="number"
            placeholder="Quantità"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            min="1"
            step="1"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="price">Prezzo:</label>
          <input
            type="number"
            placeholder="Prezzo"
            value={price}
            onChange={(e) => setPrice(parseFloat(e.target.value))}
            min="1"
            step="0.01"
            required
          />
        </div>
        <button type="submit">Aggiungi Asset</button>
      </form>
    </div>
  );
};

export default AddAsset;