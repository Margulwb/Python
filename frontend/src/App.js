import React, { useEffect, useState } from 'react';

function App() {
    const [signals, setSignals] = useState({});
    const [formData, setFormData] = useState({ symbol: '', name: '', shares: 1 });
    const [sellReasons, setSellReasons] = useState({});

    useEffect(() => {
        const fetchStocks = async () => {
            try {
                const response = await fetch('http://localhost:5001/stocks'); // Fetch stocks from the database
                if (!response.ok) {
                    throw new Error('Failed to fetch stocks');
                }
                const data = await response.json();
                console.log('Fetched stocks:', data); // Log the fetched stocks
                console.log('Fetched stocks from backend:', data); // Log the fetched stocks
                setSignals(data.reduce((acc, stock) => {
                    acc[stock.symbol] = stock.signal.toUpperCase(); // Convert signal to uppercase
                    return acc;
                }, {}));
            } catch (error) {
                console.error('Error fetching stocks:', error);
            }
        };

        fetchStocks();

        const interval = setInterval(fetchStocks, 60000); // Refresh every 60 seconds
        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, []);

    const stockDetails = {
        cdr: { name: 'CD Projekt Red', shares: 1, profit: '100 PLN' },
        rbw: { name: 'Rainbow', shares: 1, profit: '50 PLN' },
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5001/stocks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });
            if (!response.ok) {
                throw new Error('Failed to add stock');
            }
            setFormData({ symbol: '', name: '', shares: 1 });

            // Fetch updated stock list after adding a new stock
            const updatedResponse = await fetch('http://localhost:5001/stocks');
            if (!updatedResponse.ok) {
                throw new Error('Failed to fetch updated stocks');
            }
            const updatedData = await updatedResponse.json();
            setSignals(updatedData.reduce((acc, stock) => {
                acc[stock.symbol] = stock.signal.toUpperCase(); // Convert signal to uppercase
                return acc;
            }, {}));
        } catch (error) {
            console.error('Error adding stock:', error);
        }
    };

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

    const fetchSellReason = async (symbol) => {
        try {
            console.log('Fetching reason for:', symbol);
            const response = await fetch(`http://localhost:5001/signals/reason/${symbol}`);
            if (!response.ok) {
                throw new Error('Failed to fetch sell reason');
            }
            const data = await response.json();
            setSellReasons((prevReasons) => ({ ...prevReasons, [symbol]: data.reason }));
        } catch (error) {
            console.error('Error fetching sell reason:', error);
            setSellReasons((prevReasons) => ({ ...prevReasons, [symbol]: 'No reason available' }));
        }
    };

    return (
        <div className="App">
            <header className="bg-primary text-white text-center py-3">
                <h1>Stock Signal Dashboard</h1>
            </header>
            <main className="container mt-4">
                <form onSubmit={handleSubmit} className="mb-4">
                    <div className="row g-3">
                        <div className="col-md-4">
                            <input
                                type="text"
                                name="symbol"
                                placeholder="Symbol"
                                value={formData.symbol}
                                onChange={handleInputChange}
                                className="form-control"
                                required
                            />
                        </div>
                        <div className="col-md-4">
                            <input
                                type="text"
                                name="name"
                                placeholder="Name"
                                value={formData.name}
                                onChange={handleInputChange}
                                className="form-control"
                                required
                            />
                        </div>
                        <div className="col-md-4">
                            <input
                                type="number"
                                name="shares"
                                placeholder="Shares"
                                value={formData.shares}
                                onChange={handleInputChange}
                                className="form-control"
                                required
                            />
                        </div>
                    </div>
                    <button type="submit" className="btn btn-success mt-3">Add Stock</button>
                </form>
                {Object.keys(signals).length > 0 ? (
                    <div className="table-responsive">
                        <table className="table table-striped">
                            <thead className="table-dark">
                                <tr>
                                    <th>Full Name</th>
                                    <th>Symbol</th>
                                    <th>Shares</th>
                                    <th>Signal</th>
                                    <th>Profit</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {Object.entries(signals).map(([symbol, signal], index) => (
                                    <tr key={index}>
                                        <td>{stockDetails[symbol]?.name || 'Unknown'}</td>
                                        <td>{symbol.toUpperCase()}</td>
                                        <td>{stockDetails[symbol]?.shares || 0}</td>
                                        <td>
                                            {signal === 'SELL' ? (
                                                <span
                                                    style={{
                                                        display: 'inline-block',
                                                        padding: '0.3em 0.6em',
                                                        fontSize: '0.9em',
                                                        fontWeight: 'bold',
                                                        color: 'white',
                                                        backgroundColor: 'red',
                                                        borderRadius: '0.5em',
                                                        textTransform: 'uppercase',
                                                        cursor: 'pointer',
                                                    }}
                                                    title={sellReasons[symbol] || 'Fetching reason...'}
                                                    onMouseEnter={() => {
                                                        if (!sellReasons[symbol]) fetchSellReason(symbol);
                                                    }}
                                                >
                                                    {signal}
                                                </span>
                                            ) : (
                                                <span
                                                    style={{
                                                        display: 'inline-block',
                                                        padding: '0.3em 0.6em',
                                                        fontSize: '0.9em',
                                                        fontWeight: 'bold',
                                                        color: 'white',
                                                        backgroundColor: signal === 'BUY' ? 'green' : 'gray',
                                                        borderRadius: '0.5em',
                                                        textTransform: 'uppercase',
                                                    }}
                                                >
                                                    {signal}
                                                </span>
                                            )}
                                        </td>
                                        <td>{stockDetails[symbol]?.profit || '0 PLN'}</td>
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
                ) : (
                    <p className="text-center">Loading signals...</p>
                )}
            </main>
        </div>
    );
}

export default App;
