import React, { useState } from 'react';
import useStockData from './useStockData';

function StockForm() {
    const { setSignals } = useStockData();
    const [formData, setFormData] = useState({ symbol: '', name: '', shares: 1 });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
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
                acc[stock.symbol] = {
                    signal: stock.signal.toUpperCase(),
                    name: stock.name,
                    shares: stock.shares,
                    profit: stock.profit
                };
                return acc;
            }, {}));
        } catch (error) {
            console.error('Error adding stock:', error);
        }
    };

    return (
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
    );
}

export default StockForm;
