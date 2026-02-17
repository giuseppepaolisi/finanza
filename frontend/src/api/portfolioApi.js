
const API_BASE_URL = 'http://localhost:8000/portfolio';

export const portfolioApi = {
    // Valore totale del portafoglio
    get_total_portfolio_value: async (currency) => {
        try {
            const response = await fetch(`${API_BASE_URL}/value/${currency}`);
            if (!response.ok) {
            throw new Error(response.message || 'Failed to fetch total portfolio value');
            } else {
                const data = await response.json();
                return data;
            }
        } catch (error) {
            console.error('Error fetching total portfolio value:', error);
            throw error;
        }
    },

    // Lista di assets
    get_assets: async (sort_by = 'price', order = 'desc') => {
        try {
            const response = await fetch(`${API_BASE_URL}/assets/${sort_by}/${order}`);
            if (!response.ok) {
                throw new Error(response.message || 'Fetch asset fallita');
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching assets:', error);
            throw error;
        }
    },

    // Aggiungi un nuovo asset
    add_asset: async (symbol, quantity, price) => {
        try {
            const response = await fetch(`${API_BASE_URL}/assets`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(
                    { 
                        symbol: symbol, 
                        quantity: quantity,
                        price: price
                    }),
            });
            if (!response.ok) {
                throw new Error(response.message || 'Non è possibile aggiungere l\'asset');
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error adding asset:', error);
            throw error;
        }
    },

};