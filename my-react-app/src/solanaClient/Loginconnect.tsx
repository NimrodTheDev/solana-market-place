import { useState } from 'react';
import { useWallet } from '@solana/wallet-adapter-react';

const loginUrl = "https://solana-market-place-backend.onrender.com/api/login/";
const registerUrl = "https://solana-market-place-backend.onrender.com/api/register/";

type TokenResponse = {
  token: string;
};

type UserData = {
  id: number;
  wallet_address: string;
};

export default function Loginconnect() {
  const { connect, connected, publicKey } = useWallet();
  const [token, setToken] = useState<string>("");
  const [userData, setUserData] = useState<UserData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [account, setAccount] = useState<string>("");

  // Connect wallet function
  const handleConnectWallet = async () => {
    try {
      await connect();
      if (publicKey) {
        setAccount(publicKey.toString());
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to connect wallet");
      console.error("Wallet connection error:", err);
    }
  };

  // Login function
  const handleLogin = async () => {
    setIsLoading(true);
    setError(null);

    try {
      if (!account) {
        throw new Error("Please connect your wallet first");
      }

      const response = await fetch(loginUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          wallet_address: account
        })
      });

      if (!response.ok) {
        if (response.status === 404) {
          setError("User  not found. Please register first.");
          setIsRegistering(true);
          return;
        } else {
          throw new Error(`Login failed: ${response.status}`);
        }
      }

      const data: TokenResponse = await response.json();
      setToken(data.token);

      const userDataResponse = await fetch("https://solana-market-place-backend.onrender.com/api/me/", {
        headers: {
          "Authorization": `Token ${data.token}`
        }
      });

      if (!userDataResponse.ok) {
        throw new Error(`Failed to fetch user data: ${userDataResponse.status}`);
      }

      const userData: UserData = await userDataResponse.json();
      setUserData(userData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  // Register function
  const handleRegister = async () => {
    setIsLoading(true);
    setError(null);

    try {
      if (!account) {
        await handleConnectWallet();
      }

      const registerResponse = await fetch(registerUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          wallet_address: account
        })
      });

      if (!registerResponse.ok) {
        throw new Error(`Registration failed: ${registerResponse.status}`);
      }

      await handleLogin();
    } catch (err) {
 setError(err instanceof Error ? err.message : "An unexpected error occurred during registration");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      {!connected && (
        <button 
          onClick={handleConnectWallet}
          style={{ marginBottom: '10px' }}
        >
          Connect Wallet
        </button>
      )}
      
      <button 
        onClick={handleLogin}
        disabled={isLoading || !connected}
      >
        {isLoading ? "Loading..." : "Login"}
      </button>
      
      {error && <p style={{ color: "red" }}>{error}</p>}
      
      {isRegistering && (
        <div>
          <p>Please register first to continue.</p>
          <button 
            onClick={handleRegister}
            disabled={isLoading}
          >
            Register
          </button>
        </div>
      )}
      
      {userData && (
        <div>
          <h2>User Data:</h2>
          <p>ID: {userData.id}</p>
          <p>Wallet Address: {userData.wallet_address}</p>
          <p>Token: {token}</p>
        </div>
      )}
    </div>
  );
}
