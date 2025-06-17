import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { useState } from 'react';
import { useSolana } from '../../solanaClient';
import { useParams } from 'react-router-dom';
import { PublicKey } from '@solana/web3.js';
import { Link } from 'react-router-dom';
import { Toast, useToast } from '../general/Toast';

interface BuyAndSellProps {
    coinData?: {
        ticker?: string;
        current_price?: string;
    };
}

function BuyAndSell({coinData}: BuyAndSellProps) {
    const [activeTab, setActiveTab] = useState<'buy' | 'sell'>('buy');
    const [amount, setAmount] = useState('0.001');
    const {BuyTokenMint, SellTokenMint} = useSolana()
    const { id } = useParams();
    const { showToast, toastMessage, toastType, showToastMessage, setShowToast } = useToast();

    const handleSell = async () => {
        if (SellTokenMint && id) {
            try {
                const amount = 1; // or whatever amount you want to sell
                const { tx, sellerTokenAccount } = await SellTokenMint(new PublicKey(id), amount);
                console.log('Sell transaction:', tx);
                console.log('Seller token account:', sellerTokenAccount.toString());
                showToastMessage(
                    <Link to={`https://explorer.solana.com/tx/${tx}?cluster=devnet`} target='_blank' className='underline'>
                        Tokens sold successfully! View on Explorer
                    </Link>,
                    "success"
                );
            } catch (error) {
                console.error('Error selling tokens:', error);
                showToastMessage("Failed to sell tokens. Please try again.", "error");
            }   
        }
    };
        
    // Mock data for holders
    const topHolders: {
        address: string;
        percentage: string;
    }[] = [
        // { address: '8rqb2fJrj...', percentage: '92%' },
        // { address: '8rqb2fJrj...', percentage: '0.97%' },
        // { address: '8rqb2fJrj...', percentage: '0.97%' },
        // { address: '8rqb2fJrj...', percentage: '0.97%' },
        // { address: '8rqb2fJrj...', percentage: '0.97%' },
    ];

    const holderAnalytics: {
        label: string;
        value: string;
    }[] = [
        // { label: 'Total Holders', value: '200,000' },
        // { label: 'T2 Holders', value: '99' },
        // { label: 'Holders with 500K-500K', value: '25%' },
        // { label: 'Holders with 500K-49M', value: '25%' },
    ];

    return (
        <div className="bg-custom-dark-blue rounded-lg p-4  text-white md:mr-12 lg:mr-24 w-full">
            {/* Buy/Sell Tabs */}
            <div className="flex justify-between lg:w-64 mb-4">
                <button
                    onClick={() => {
                        setActiveTab('buy')
                        if (BuyTokenMint && id) {
                            BuyTokenMint(new PublicKey(id), Number(amount))
                                .then((res) => {
                                    console.log(res);
                                    showToastMessage(
                                        <Link to={`https://explorer.solana.com/tx/${res.tx}?cluster=devnet`} target='_blank' className='underline'>
                                            Tokens bought successfully! View on Explorer
                                        </Link>,
                                        "success"
                                    );
                                })
                                .catch((error) => {
                                    console.error('Error buying tokens:', error);
                                    showToastMessage("Failed to buy tokens. Please try again.", "error");
                                });
                        }
                    }}
                    className={` py-2 px-4 rounded-md w-24  font-medium ${activeTab === 'buy'
                        ? 'bg-custom-light-purple text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                        }`}
                >
                    Buy
                </button>
                <button
                    onClick={() => {
                        setActiveTab('sell')
                        handleSell()
                    }}
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
                        className="w-full bg-custom-dark-blue border border-gray-600 rounded-md px-3 py-2 text-white focus:outline-none focus:border-purple-500 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        step="0.001"
                        min="0"
                    />
                    <span className="absolute right-3 top-2 text-gray-400">{coinData?.ticker}</span>
                </div>
            </div>

            {/* Connect Wallet Button */}
            <WalletMultiButton />

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

            {showToast && (
                <Toast
                    message={toastMessage}
                    type={toastType}
                    onClose={() => setShowToast(false)}
                />
            )}
        </div>
    );
}

export default BuyAndSell;