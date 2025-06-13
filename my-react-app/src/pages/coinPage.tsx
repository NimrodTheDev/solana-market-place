 import React, { useEffect, useState, ChangeEvent } from "react";
 // import HoldersAnalytics from "../components/coin/coinHolder";
import axios from "axios";
import CoinFilter, { CoinData, FilterOptions } from "../components/coin/CoinFilter"; // Adjust path as needed
import CoinProfile from "../components/coin/coinProfile";
// import CoinComments from "../components/coin/comment";
// import CryptoTradingWidget from "../components/coin/tradingWidget";
import CryptoTokenDetails from "../components/coin/cryptoTokenDetail";
import SimilarCoins from "../components/coin/similiarCoin";
import BuyAndSell from "../components/coin/BuyAndSell";
import { useParams } from "react-router-dom";

const CoinPage: React.FC = () => {
  const [allCoins, setAllCoins] = useState<CoinData[]>([]); // fetch all
  const [filteredCoins, setFilteredCoins] = useState<CoinData[]>([]); // client filtered
  const [coinData, setCoinData] = useState<CoinData | null>(null);
  const [filter, setFilter] = useState<FilterOptions["filter"]>("all");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [loadingList, setLoadingList] = useState<boolean>(true);
  const [loadingCoin, setLoadingCoin] = useState<boolean>(true);
  const [errorList, setErrorList] = useState<string | null>(null);
  const [errorCoin, setErrorCoin] = useState<string | null>(null);
  const { id } = useParams();

  // Determine limit based on window width
  const limit = typeof window !== "undefined" && window.innerWidth < 768 ? 5 : 10;

  // Fetch all coins once without filter params (server returns all)
  useEffect(() => {
    const fetchAllCoins = async () => {
      setLoadingList(true);
      setErrorList(null);
      try {
        const response = await axios.get<CoinData[]>(
          `https://solana-market-place-backend.onrender.com/api/coins/topcoins?limit=${limit}`
        );
        if (response.status === 200) {
          setAllCoins(response.data);
          setFilteredCoins(response.data); // init filtered with all
        } else {
          setErrorList(`Unexpected status code: ${response.status}`);
          setAllCoins([]);
          setFilteredCoins([]);
        }
      } catch (err: any) {
        setErrorList(err.message || "Failed to fetch coins.");
        setAllCoins([]);
        setFilteredCoins([]);
      } finally {
        setLoadingList(false);
      }
    };
    fetchAllCoins();
  }, [limit]);

  // Client-side filtering logic applied when filter or searchTerm changes
  useEffect(() => {
    let filtered = allCoins;

    // Filter by drcscore or name or all
    if (filter === "drcscore") {
      filtered = filtered.filter((coin) => coin.score > 0);
    } else if (filter === "name") {
      filtered = filtered.slice().sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    }

    // Then filter by search term (case insensitive substring match)
    if (searchTerm.trim() !== "") {
      const lowerSearch = searchTerm.toLowerCase();
      filtered = filtered.filter(
        (coin) =>
          coin.name.toLowerCase().includes(lowerSearch) ||
          coin.address.toLowerCase().includes(lowerSearch)
      );
    }

    setFilteredCoins(filtered);
  }, [allCoins, filter, searchTerm]);

  // Fetch individual coin data by ID
  useEffect(() => {
    const fetchCoinData = async () => {
      if (!id) {
        setCoinData(null);
        setLoadingCoin(false);
        return;
      }
      setLoadingCoin(true);
      setErrorCoin(null);
      try {
        const response = await axios.get<CoinData>(
          `https://solana-market-place-backend.onrender.com/api/coins/${id}`
        );
        setCoinData(response.data);
      } catch (err) {
        setErrorCoin("Failed to fetch coin data");
      } finally {
        setLoadingCoin(false);
      }
    };
    fetchCoinData();
  }, [id]);

  const handleSearchChange = (e: ChangeEvent<HTMLInputElement>) =>
    setSearchTerm(e.target.value);

  const handleFilterChange = (newFilter: FilterOptions["filter"]) => {
    setFilter(newFilter);
    setSearchTerm("");
  };

  if (loadingList || loadingCoin) {
    return <div className="bg-gray-900 text-white min-h-screen p-4">Loading...</div>;
  }

  if (errorList) {
    return <div className="bg-gray-900 text-white min-h-screen p-4">{errorList}</div>;
  }

  return (
    <div className="bg-custom-dark-blue w-full items-center">
      {/* Filtering & Searching of Coins */}
      <CoinFilter
        coins={filteredCoins}
        filter={filter}
        searchTerm={searchTerm}
        onSearchChange={handleSearchChange}
        onFilterChange={handleFilterChange}
      />

      {/* Detailed view of single coin */}
      {errorCoin ? (
        <p className="text-red-500 text-center mt-4">{errorCoin}</p>
      ) : coinData ? (
        <div className="bg-custom-dark-blue flex flex-col gap-2 mx-auto text-white max-w-7xl p-4">
          <div className="flex flex-col sm:flex-row">
            <div className="flex flex-col gap-2 w-full">
              <CoinProfile coinData={coinData} />
              <CryptoTokenDetails coinData={coinData} />
			  {/* <CoinComments coinData={coinData} /> */}
            </div>
            <div className="flex flex-col gap-2">
              <BuyAndSell coinData={coinData} />
			  {/* <CryptoTradingWidget coinData={coinData} /> */}
				{/* <HoldersAnalytics coinData={coinData} /> */}
            </div>
          </div>
          <SimilarCoins coinData={coinData} />
        </div>
      ) : null}
    </div>
  );
};

export default CoinPage;
