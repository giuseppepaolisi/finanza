
const API_BASE_URL = 'http://localhost:8000/portfolio';

export const portfolioApi = {
    get_total_portfolio_value: async (currency) => {
        try {
            const response = await fetch(`${API_BASE_URL}/value/${currency}`);
            if (!response.ok) {
            throw new Error('Failed to fetch total portfolio value');
            } else {
                const data = await response.json();
                return data;
            }
        } catch (error) {
        console.error('Error fetching total portfolio value:', error);
        throw error;
        }
    }
};