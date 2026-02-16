import React from 'react';

const Summary = ({total, currency, isLoading}) => {
    return (
        <div className="summary">
            <h2>Portfolio Summary</h2>
            {isLoading ? (
                <p>Loading...</p>
            ) : (
                <p>Valore totale: {total} {currency}</p>
            )}
        </div>
    );
}

export default Summary;