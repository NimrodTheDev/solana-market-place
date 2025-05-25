import { Wallet } from 'lucide-react';
import { Component, ErrorInfo, ReactNode } from 'react';


interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  isPhantomInstalled: boolean;
}

class PhantomError extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      isPhantomInstalled: true
    };
  }

  static getDerivedStateFromError(_: Error): State {
    return { hasError: true, isPhantomInstalled: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by PhantomError:', error, errorInfo);
  }

  componentDidMount() {
    // Check if Phantom wallet is installed
    const checkPhantomWallet = () => {
      // @ts-ignore
      const isInstalled = window.solana 
      this.setState({ isPhantomInstalled: isInstalled });
    };

    checkPhantomWallet();
  }

  render() {
    if (!this.state.isPhantomInstalled) {
      return (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-90 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-8 rounded-lg max-w-md w-full mx-4">
            <div className="flex flex-col items-center text-center">
              <div className="bg-indigo-900 bg-opacity-50 p-4 rounded-full mb-6">
                <Wallet size={48} className="text-indigo-300" />
              </div>
              
              <h2 className="text-2xl font-bold text-white mb-4">
                Phantom Wallet Required
              </h2>
              
              <p className="text-gray-400 mb-6">
                To use this application, you need to install the Phantom wallet browser extension or any solana browser extension.
                Phantom is a secure wallet for Solana that allows you to manage your digital assets.
              </p>

              <div className="space-y-4 w-full">
                <a
                  href="https://phantom.app/download"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full bg-indigo-500 hover:bg-indigo-600 text-white font-medium py-3 px-6 rounded-lg transition-colors"
                >
                  Download Phantom Wallet
                </a>
                
                <button
                  onClick={() => window.location.reload()}
                  className="block w-full bg-gray-700 hover:bg-gray-600 text-white font-medium py-3 px-6 rounded-lg transition-colors"
                >
                  Reload Page After Installation
                </button>
              </div>

              <div className="mt-6 text-sm text-gray-500">
                <p>Don't have a Solana wallet yet?</p>
                <a
                  href="https://phantom.app/help/getting-started/creating-a-new-wallet"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-400 hover:text-indigo-300"
                >
                  Learn how to create one →
                </a>
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (this.state.hasError) {
      return (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-90 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-8 rounded-lg max-w-md w-full mx-4">
            <div className="flex flex-col items-center text-center">
              <div className="bg-red-900 bg-opacity-50 p-4 rounded-full mb-6">
                <svg className="w-12 h-12 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              
              <h2 className="text-2xl font-bold text-white mb-4">
                Something went wrong
              </h2>
              
              <p className="text-gray-400 mb-6">
                An error occurred while rendering this page. Please try refreshing the page or contact support if the problem persists.
              </p>

              <button
                onClick={() => window.location.reload()}
                className="block w-full bg-red-500 hover:bg-red-600 text-white font-medium py-3 px-6 rounded-lg transition-colors"
              >
                Refresh Page
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default PhantomError; 