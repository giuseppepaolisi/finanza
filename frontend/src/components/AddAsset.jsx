import React, { useState } from "react";
import { portfolioApi } from "../api/portfolioApi";

const AddAsset = () => {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (symbol && quantity > 0) {
        portfolioApi.add_asset(symbol, quantity)
            .then(() => {
                setSymbol("");
                setQuantity(0);
            })
            .catch(error => {
                console.error("Error adding asset:", error);
            });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Simbolo dell'asset"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Quantità"
        value={quantity}
        onChange={(e) => setQuantity(parseFloat(e.target.value))}
        min="1"
        step="1"
        required
      />
      <button type="submit">Aggiungi Asset</button>
    </form>
  );
};

export default AddAsset;