import React, { useState } from "react";
import { portfolioApi } from "../api/portfolioApi";

const AddAsset = ({loadPortfolioData}) => {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState(1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (symbol && quantity > 0) {
        try {
            const data = await portfolioApi.add_asset(symbol, quantity);
            if(data.error) {
                alert(data.error);
                return;
            }
            setSymbol("");
            setQuantity(1);
            loadPortfolioData();
        } catch (error) {
            console.error("Error adding asset:", error);
        }
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