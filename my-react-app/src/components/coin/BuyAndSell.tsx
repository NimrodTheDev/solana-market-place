import { useState } from 'react';


interface BuyAndSellProps {
    coinData?: {
        ticker?: string;
        current_price?: string;
    };
}

function BuyAndSell({ coinData }: BuyAndSellProps) {
    const [activeTab, setActiveTab] = useState<'buy' | 'sell'>('buy');
    const [amount, setAmount] = useState('0.001');

    // Mock data for holders
    const topHolders = [
        { address: '8rqb2fJrj...', percentage: '92%' },
        { address: '8rqb2fJrj...', percentage: '0.97%' },
        { address: '8rqb2fJrj...', percentage: '0.97%' },
        { address: '8rqb2fJrj...', percentage: '0.97%' },
        { address: '8rqb2fJrj...', percentage: '0.97%' },
        { address: '8rqb2fJrj...', percentage: '0.97%' },
    ];

    const holderAnalytics = [
        { label: 'Total Holders', value: '200,000' },
        { label: 'T2 Holders', value: '99' },
        { label: 'Holders with 500K-500K', value: '25%' },
        { label: 'Holders with 500K-49M', value: '25%' },
    ];

    return (
        <div className="bg-custom-dark-blue rounded-lg p-4  text-white md:mr-12 lg:mr-24 w-full">
            {/* Buy/Sell Tabs */}
            <div className="flex justify-between lg:w-64 mb-4">
                <button
                    onClick={() => setActiveTab('buy')}
                    className={` py-2 px-4 rounded-md w-24  font-medium ${activeTab === 'buy'
                        ? 'bg-custom-light-purple text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                        }`}
                >
                    Buy
                </button>
                <button
                    onClick={() => setActiveTab('sell')}
                    className={` py-2 px-4 rounded-md w-24 font-medium ${activeTab === 'sell'
                        ? 'bg-custom-light-purple text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                        }`}
                >
                    Sell
                </button>
            </div>

            {/* Amount Input */}
            <div className="mb-4">

                <div className="relative">
                    <input
                        type="number"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="w-full bg-custom-dark-blue border border-gray-600 rounded-md px-3 py-2 text-white focus:outline-none focus:border-purple-500"
                        step="0.001"
                        min="0"
                    />
                    <span className="absolute right-3 top-2 text-gray-400">SOL</span>
                </div>
            </div>

            {/* Connect Wallet Button */}
            <button className="w-full bg-custom-light-purple hover:bg-purple-700 text-white font-medium py-3 px-4 rounded-md mb-6 transition-colors">
                Connect Wallet to trade
            </button>

            {/* Top Holders Section */}
            <div className="mb-6">
                <h3 className="text-white font-medium mb-3">Top Holders</h3>
                <div className="space-y-2">
                    {topHolders.map((holder, index) => (
                        <div key={index} className="flex items-center justify-between">
                            <div className="flex items-center">
                                <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center mr-2">
                                    <span className="text-xs font-bold text-black">🏆</span>
                                </div>
                                <span className="text-custom-light-purple text-sm font-mono">
                                    {holder.address}
                                </span>
                            </div>
                            <span className="text-gray-300 text-sm">{holder.percentage}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Holder Analytics Section */}
            <div>
                <h3 className="text-white font-medium mb-3">Holder Analytics</h3>
                <div className="space-y-2">
                    {holderAnalytics.map((analytic, index) => (
                        <div key={index} className="flex items-center justify-between">
                            <div className="flex items-center">
                                <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center mr-2">
                                    <span className="text-xs font-bold text-black">🏆</span>
                                </div>
                                <span className="text-custom-light-purple text-sm">
                                    {analytic.label}
                                </span>
                            </div>
                            <span className="text-gray-300 text-sm">{analytic.value}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default BuyAndSell;