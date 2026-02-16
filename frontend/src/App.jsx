import { useState, useEffect } from 'react'
import { portfolioApi } from './api/portfolioApi';
import Summary from './components/Summary';
import Assets from './components/Assets';
import AddAsset from './components/AddAsset';

function App() {
  // Stato per il valore totale del portafoglio
  const [totalValue, setTotalValue] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [currency, ] = useState('USD');

  const [assets, setAssets] = useState([]);

  useEffect(() => {
    const loadPortfolioData = async () => {
      try {
        // Chiamata API per ottenere il valore totale del portafoglio
        const data = await portfolioApi.get_total_portfolio_value(currency);
        setTotalValue(data.total_value);

        // Chiamata API per ottenere la lista degli asset
        const assetsData = await portfolioApi.get_assets();
        setAssets(assetsData.assets);
      } catch (error) {
        console.error('Error fetching total portfolio value:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadPortfolioData();
  }, [currency]);

  return (
    <>
      <Summary total={totalValue} currency={currency} isLoading={isLoading} />
      <AddAsset onAddAsset={() => {
        portfolioApi.get_assets().then(setAssets);
      }} />
      <Assets assets={assets} onSort={(sort_by, order) => {
        portfolioApi.get_assets(sort_by, order).then(setAssets);
      }} currentSort={null} currentOrder={null} />
    </>
  )
}

export default App
