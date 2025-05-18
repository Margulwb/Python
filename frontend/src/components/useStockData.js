import { useState, useEffect } from 'react';

const useStockData = () => {
    const [signals, setSignals] = useState({});
    const [sellReasons, setSellReasons] = useState({});

    useEffect(() => {
        const fetchStocks = async () => {
            try {
                const response = await fetch('http://localhost:5001/stocks');
                if (!response.ok) {
                    throw new Error('Failed to fetch stocks');
                }
                const data = await response.json();
                setSignals(data.reduce((acc, stock) => {
                    acc[stock.symbol] = {
                        signal: stock.signal ? stock.signal.toUpperCase() : 'UNKNOWN',
                        name: stock.name,
                        shares: stock.shares,
                        profit: stock.profit
                    };
                    return acc;
                }, {}));
            } catch (error) {
                console.error('Error fetching stocks:', error);
            }
        };

        fetchStocks();

        const interval = setInterval(fetchStocks, 60000);
        return () => clearInterval(interval);
    }, []);

    const fetchSellReason = async (symbol) => {
        try {
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

    return { signals, sellReasons, fetchSellReason, setSignals };
};

export default useStockData;
