import React from 'react';
import useStockData from './useStockData';

function StockTable() {
    const { signals, fetchSellReason, sellReasons } = useStockData();

    const handleDelete = async (symbol) => {
        try {
            const response = await fetch(`http://localhost:5001/stocks/${symbol}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error('Failed to delete stock');
            }
            // Refresh the stock list after deletion
            setSignals((prevSignals) => {
                const updatedSignals = { ...prevSignals };
                delete updatedSignals[symbol];
                return updatedSignals;
            });
        } catch (error) {
            console.error('Error deleting stock:', error);
        }
    };

    return (
        <div className="table-responsive">
            <table className="table table-striped">
                <thead className="table-dark">
                    <tr>
                        <th>Full Name</th>
                        <th>Symbol</th>
                        <th>Shares</th>
                        <th>Signal</th>
                        <th>Profit</th>
                        <th>Reason</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(signals).map(([symbol, { signal, name, shares, profit }], index) => (
                        <tr key={index}>
                            <td>{name || 'Unknown'}</td>
                            <td>{symbol.toUpperCase()}</td>
                            <td>{shares || 0}</td>
                            <td>
                                {signal === 'SELL' ? (
                                    <span
                                        className={`signal signal-sell`}
                                        title={sellReasons[symbol] || 'Fetching reason...'}
                                        onMouseEnter={() => {
                                            if (!sellReasons[symbol]) fetchSellReason(symbol);
                                        }}
                                    >
                                        {signal}
                                    </span>
                                ) : (
                                    <span
                                        className={`signal ${signal === 'BUY' ? 'signal-buy' : 'signal-hold'}`}
                                    >
                                        {signal}
                                    </span>
                                )}
                            </td>
                            <td>{profit || '0 PLN'}</td>
                            <td>{sellReasons[symbol] || 'Fetching reason...'}</td>
                            <td>
                                <button
                                    className="btn btn-danger btn-sm"
                                    onClick={() => handleDelete(symbol)}
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default StockTable;
