import { useState, useEffect, use } from 'react'
import { portfolioApi } from './api/portfolioApi';
import Summary from './components/Summary';
import Assets from './components/Assets';
import AddAsset from './components/AddAsset';
import './App.css';

function App() {
  // Stato per il valore totale del portafoglio
  const [totalValue, setTotalValue] = useState(0);
  const [isLoadingValue, setIsLoadingValue] = useState(true);
  const [currency, ] = useState('USD');
  const [sortBy, setSortBy] = useState('price');
  //const [sortOrder, setSortOrder] = useState('desc');

  const [assets, setAssets] = useState([]);
  const [isLoadingAssets, setIsLoadingAssets] = useState(true);

  const loadPortfolioValue = async () => {
    setIsLoadingValue(true);
    try {
      const data = await portfolioApi.get_total_portfolio_value(currency);
      setTotalValue(data.total_value);
    } catch (error) {
      console.error('Error fetching total portfolio value:', error);
    } finally {
      setIsLoadingValue(false);
    }
  };

  const loadPortfolioAssets = async (sort_by) => {
    setIsLoadingAssets(true);
      try {
        // Chiamata API per ottenere la lista degli asset
        const assetsData = await portfolioApi.get_assets(sort_by);
        setAssets(assetsData.assets);
      } catch (error) {
        console.error('Error fetching total portfolio value:', error);
      } finally {
        setIsLoadingAssets(false);
      }
    };

  useEffect(() => {
    loadPortfolioValue();
  }, []);

  useEffect(() => {
    loadPortfolioAssets(sortBy);
  }, [sortBy]);

  return (
    <div className="app-container">
      <Summary total={totalValue} currency={currency} isLoading={isLoadingValue} />
      <div className="controls-row">
        <AddAsset 
          onAssetAdded={() => {
            loadPortfolioAssets(sortBy);
            loadPortfolioValue();
          }} 
          isLoading={isLoadingAssets} 
        />
        <div className="sort-box">
          <label>Ordina per: </label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="price">Prezzo</option>
            <option value="total_quantity">Quantità</option>
            <option value="market_value">Valore di Mercato</option>
          </select>
        </div>
      </div>
      <Assets assets={assets} isLoading={isLoadingAssets}/>
    </div>
  )
}

export default App
