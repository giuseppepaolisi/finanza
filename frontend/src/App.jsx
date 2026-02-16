import { useState, useEffect, use } from 'react'
import { portfolioApi } from './api/portfolioApi';
import Summary from './components/Summary';
import Assets from './components/Assets';
import AddAsset from './components/AddAsset';

function App() {
  // Stato per il valore totale del portafoglio
  const [totalValue, setTotalValue] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [currency, ] = useState('USD');
  const [sortBy, setSortBy] = useState('price');
  //const [sortOrder, setSortOrder] = useState('desc');

  const [assets, setAssets] = useState([]);

  const loadPortfolioValue = async () => {
    try {
      const data = await portfolioApi.get_total_portfolio_value(currency);
      setTotalValue(data.total_value);
    } catch (error) {
      console.error('Error fetching total portfolio value:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadPortfolioAssets = async (sort_by) => {
      try {
        // Chiamata API per ottenere la lista degli asset
        const assetsData = await portfolioApi.get_assets(sort_by);
        setAssets(assetsData.assets);
      } catch (error) {
        console.error('Error fetching total portfolio value:', error);
      } finally {
        setIsLoading(false);
      }
    };

  useEffect(() => {
    loadPortfolioValue();
  }, []);

  useEffect(() => {
    loadPortfolioAssets(sortBy);
  }, [sortBy]);

  return (
    <>
      <Summary total={totalValue} currency={currency} isLoading={isLoading} />
      <AddAsset loadPortfolioAssets={loadPortfolioAssets} />
      Ordina per: <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="price">Prezzo</option>
        <option value="total_quantity">Quantità</option>
        <option value="market_value">Valore di Mercato</option>
      </select>
      <Assets assets={assets} onSort={(sort_by, order) => {
        portfolioApi.get_assets(sort_by, order).then(setAssets);
      }} currentSort={null} currentOrder={null} />
    </>
  )
}

export default App
