import React, { useState } from "react";
import { portfolioApi } from "../api/portfolioApi";
import { toast } from "react-hot-toast";

const AddAsset = ({ onAssetAdded }) => {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [price, setPrice] = useState(1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (symbol && quantity > 0 && price > 0) {
        try {
            const data = await portfolioApi.add_asset(symbol, quantity, price);
            if(data.error) {
                toast.error(data.message);
                return;
            }
            setSymbol("");
            setQuantity(1);
            setPrice(1);
            toast.success('Asset aggiunto!');
            if (onAssetAdded) {
              onAssetAdded();
            }
        } catch (error) {
            toast.error(error.message);
            console.error("Error adding asset:", error);
        }
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