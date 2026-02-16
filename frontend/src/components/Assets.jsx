import React from 'react';
import MoveUpRight from 'lucide-react/dist/esm/icons/move-up-right.js';
import MoveDownLeft from 'lucide-react/dist/esm/icons/move-down-left.js';
import Minus from 'lucide-react/dist/esm/icons/minus.js';

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
                <td>{asset.average_price} {asset.currency}</td>
                <td className="profit-loss-cell">
                    {asset.profit_loss === 0 ? (
                        <span><Minus className="w-4 h-4 inline mr-1" /></span>
                    ) : asset.profit_loss > 0 ? (
                        <span className="profit"><MoveUpRight color="green" /></span>
                    ) : (
                        <span className="loss"><MoveDownLeft color="red"/></span>
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