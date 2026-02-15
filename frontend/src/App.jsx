import { useState, useEffect } from 'react'
import { portfolioApi } from './api/portfolioApi';
import Summary from './components/Summary';

function App() {
  // Stato per il valore totale del portafoglio
  const [totalValue, setTotalValue] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [currency, setCurrency] = useState('USD');

  useEffect(() => {
    const fetchTotalValue = async () => {
      try {
        const data = await portfolioApi.get_total_portfolio_value(currency);
        setTotalValue(data.total_value);
        setCurrency(data.currency);
      } catch (error) {
        console.error('Error fetching total portfolio value:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTotalValue();
  }, [currency]);
  
  return (
    <>
      <Summary total={totalValue} currency={currency} isLoading={isLoading} />
    </>
  )
}

export default App
