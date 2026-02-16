// src/components/AssetList.jsx
import React from 'react';

const Assets = ({ assets}) => {

  return (
    <div className="asset-list-container">
      <h3>I tuoi Asset</h3>
      {assets.length === 0 ? (
        <p>Nessun asset presente nel portafoglio.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Nome</th>
              <th >
                Quantità
              </th>
              <th>
                Prezzo Attuale 
              </th>
              <th>
                Valore Mercato
              </th>
              <th>
                Prezzo Medio di Carico
              </th>
              <th>
                Profit / Loss
              </th>
            </tr>
          </thead>
          <tbody>
            {assets.map((asset) => (
              <tr key={asset.symbol}>
                <td className="symbol-cell">{asset.symbol}</td>
                <td>{asset.name}</td>
                <td>{asset.total_quantity}</td>
                <td>{asset.current_price} {asset.currency}</td>
                <td className="value-cell">
                    {asset.market_value} {asset.currency}
                </td>
                <td>{asset.average_price}</td>
                <td className="profit-loss-cell">
                    {asset.profit_loss === 0 ? (
                        <span>-</span>
                    ) : asset.profit_loss > 0 ? (
                        <span className="profit">profit</span>
                    ) : (
                        <span className="loss">loss</span>
                    )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Assets;