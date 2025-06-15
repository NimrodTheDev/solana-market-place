import { useState, ReactNode, isValidElement } from 'react'
import { ArrowRight, X, Copy, Check } from 'lucide-react';
import { useSolana } from '../solanaClient/index';
import { uploadFile } from '../solanaClient/usePinta';
import DragAndDropFileInput from '../components/general/dragNdrop';
import { Link } from 'react-router-dom';
import { web3 } from '@project-serum/anchor';
// import Hero from '../components/landingPage/hero'

// Add animation keyframes
const styles = `
@keyframes slide-up {
    from {
        transform: translate(-50%, 100%);
        opacity: 0;
    }
    to {
        transform: translate(-50%, 0);
        opacity: 1;
    }
}

.animate-slide-up {
    animation: slide-up 0.3s ease-out forwards;
}
`;

interface ValidationErrors {
    tokenName?: string;
    tokenSymbol?: string;
    tokenDescription?: string;
    tokenWebsite?: string;
    tokenTwitter?: string;
    tokenDiscord?: string;
    tokenImage?: string;
    initialSupply?: string;
    pricePerToken?: string;
}

interface ToastProps {
    message: ReactNode;
    type: 'success' | 'error';
    onClose: () => void;
}

function Toast({ message, type, onClose }: ToastProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        let textToCopy = '';
        if (isValidElement(message) && typeof message.props === 'object' && message.props !== null && 'to' in message.props) {
            const to = message.props.to as string;
            textToCopy = to.split('/tx/')[1].split('?')[0];
        } else if (message) {
            textToCopy = message.toString();
        }

        try {
            await navigator.clipboard.writeText(textToCopy);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    };

    return (
        <div className={`fixed top-4 z-4 left-1/2 transform -translate-x-1/2 flex items-center gap-2 px-4 py-3 rounded-full shadow-lg transition-all duration-300 animate-slide-up ${type === 'success' ? 'bg-green-500' : 'bg-red-500'
            } text-white`}>
            <span>{message}</span>
            <div className="flex items-center gap-1">
                <button
                    onClick={handleCopy}
                    className="hover:bg-white/10 rounded-full p-1 transition-colors"
                    title="Copy to clipboard"
                >
                    {copied ? <Check size={16} /> : <Copy size={16} />}
                </button>
                <button
                    onClick={onClose}
                    className="hover:bg-white/10 rounded-full p-1 transition-colors"
                >
                    <X size={16} />
                </button>
            </div>
        </div>
    );
}

function CreateCoin() {
    const [currentStep, setCurrentStep] = useState(1);
    const [tokenName, settTokenName] = useState("");
    const [tokenSymbol, settTokenSymbol] = useState("");
    const [loading, setLoading] = useState({
        bool: false,
        msg: ""
    });
    const [tokenDescription, setTokenDescription] = useState("");
    const [tokenImage, setTokenImage] = useState<File | null>(null);
    const [tokenWebsite, setTokenWebsite] = useState("");
    const [tokenTwitter, setTokenTwitter] = useState("");
    const [tokenDiscord, setTokenDiscord] = useState("");
    const [initialSupply, setInitialSupply] = useState("");
    const [pricePerToken, setPricePerToken] = useState("");
    const { CreateTokenMint,InitTokenVault } = useSolana();
    const [error, setError] = useState<string | null>(null);
    const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});
    const [result, setResult] = useState<string | null>(null);
    const [showToast, setShowToast] = useState(false);
    const [toastMessage, setToastMessage] = useState<ReactNode>('');
    const [toastType, setToastType] = useState<'success' | 'error'>('success');
    const [mint, setMint]= useState<web3.Keypair|undefined>()
    const validateStep1 = (): boolean => {
        const errors: ValidationErrors = {};

        if (!tokenName.trim()) {
            errors.tokenName = "Token name is required";
        } else if (tokenName.length > 50) {
            errors.tokenName = "Token name must be less than 50 characters";
        }

        if (!tokenSymbol.trim()) {
            errors.tokenSymbol = "Token symbol is required";
        } else if (!/^[A-Z0-9]{2,10}$/.test(tokenSymbol)) {
            errors.tokenSymbol = "Token symbol must be 2-10 uppercase letters or numbers";
        }

        if (!tokenDescription.trim()) {
            errors.tokenDescription = "Description is required";
        } else if (tokenDescription.length > 1000) {
            errors.tokenDescription = "Description must be less than 1000 characters";
        }

        if (!tokenWebsite.trim()) {
            errors.tokenWebsite = "Website is required";
        } else if (!/^https?:\/\/.+/.test(tokenWebsite)) {
            errors.tokenWebsite = "Please enter a valid URL starting with http:// or https://";
        }

        if (!tokenTwitter.trim()) {
            errors.tokenTwitter = "Twitter handle is required";
        } else if (!/^@?[A-Za-z0-9_]{1,15}$/.test(tokenTwitter)) {
            errors.tokenTwitter = "Please enter a valid Twitter handle";
        }

        if (!tokenDiscord.trim()) {
            errors.tokenDiscord = "Discord channel is required";
        } else if (!/^https?:\/\/discord\/+/.test(tokenDiscord)) {
            errors.tokenDiscord = "Please enter a valid Discord invite link";
        }

        if (!tokenImage) {
            errors.tokenImage = "Project image is required";
        }

        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const validateStep2 = (): boolean => {
        const errors: ValidationErrors = {};

        if (!initialSupply.trim()) {
            errors.initialSupply = "Initial supply is required";
        } else if (isNaN(Number(initialSupply)) || Number(initialSupply) <= 0) {
            errors.initialSupply = "Initial supply must be a positive number";
        }

        if (!pricePerToken.trim()) {
            errors.pricePerToken = "Price per token is required";
        } else if (isNaN(Number(pricePerToken)) || Number(pricePerToken) <= 0) {
            errors.pricePerToken = "Price per token must be a positive number";
        }

        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const showToastMessage = (message: ReactNode, type: 'success' | 'error') => {
        setToastMessage(message);
        setToastType(type);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 5000);
    };

    const handleStep1Submit = async () => {
        if (!validateStep1()) {
            return;
        }
        try {
            if (!tokenImage) {
                setLoading({ bool: false, msg: '' });
                return;
            }

            const metadataUrl = await uploadFile(tokenImage, {
                name: tokenName,
                symbol: tokenSymbol,
                description: tokenDescription,
                website: tokenWebsite,
                twitter: tokenTwitter,
                discord: tokenDiscord
            });

            if (metadataUrl.length === 0) {
                setLoading({ bool: false, msg: '' });
                showToastMessage("Failed to upload token", "error");
                return;
            }

            setLoading({ bool: true, msg: "Creating token" });

            if (CreateTokenMint) {
                const txHash = await CreateTokenMint(tokenName, tokenSymbol, metadataUrl);

                if (txHash) {
                    setResult(txHash.tx);
                    showToastMessage(
                        <Link to={`https://explorer.solana.com/tx/${txHash.tx}?cluster=devnet`} className='underline'>
                            Token created successfully! View on Explorer
                        </Link>,
                        "success"
                    );
                    setMint(txHash.mintAccount)
                    setCurrentStep(2);
                } else {
                    showToastMessage("Please ensure you have Phantom extension installed", "error");
                }
            }
        } catch (e: any) {
            console.error(e);
            showToastMessage(e.message, "error");
        } finally {
            setLoading({ bool: false, msg: '' });
        }
    };

    const handleStep2Submit = async () => {
        if (!validateStep2()) {
            return;
        }

        setError("");
        setResult("");
        setLoading({ bool: true, msg: "Creating token" });

        try {
            if (mint && InitTokenVault) {
                let resp = await InitTokenVault(Number(pricePerToken), Number(initialSupply), mint )   
                console.log(resp)
                setResult(resp.tx)
                showToastMessage(
                    <Link to={`https://explorer.solana.com/tx/${resp.tx}?cluster=devnet`} className='underline'>
                            Token created successfully! View on Explorer
                        </Link>,
                        "success"
                )
            }
        } catch (e: any) {
            setError(e.message)
            console.error(e)
        } finally {
           setLoading({bool:false, msg:""})
        }
    };

    return (
        <div className='relative sm:min-h-[180vh] xl:min-h-[124vh]'>
            <style>{styles}</style>
            <div className="h-64 z-10 crtGradient background-container top-10 left-10">
                <div className="h-40 justify-center">
                    <div className="flex flex-col items-center justify-center h-full">
                        <h1 className="text-5xl font-bold text-custom-dark-blue mb-4 mt-8 text-center">Launch a new Project</h1>
                        <p className="text-gray-800 max-w-lg mx-auto text-center">
                            Build your reputation in the Web3 ecosystem as you bring your vision to life on Notty Terminal.
                        </p>
                    </div>
                </div>
            </div>

            <div className="max-[400px] h-[1200px] mx-auto bg-custom-dark-blue relative flex items-center justify-center">
                <div className="flex justify-center items-center absolute mt-10 flex-col border-gray-600 border max-w-[600px] w-full top-[-150px] mx-auto bg-custom-dark-blue z-10 p-4 text-white rounded">
                    <div className="mb-8">
                        <h1 className="text-2xl font-bold text-center mb-2">{currentStep===1 ? "Project details" : "Vault"}</h1>
                        <p className="text-gray-400">
                            {currentStep === 1 ? "Provide important details about your project" : "Set initial supply and price"}
                        </p>
                    </div>

                    {currentStep === 1 ? (
                        <form className="flex flex-col justify-center w-full max-w-[500px] mx-auto mb-10 mt=10">
                            <div className="space-y-6">
                                <div>
                                    <label htmlFor="projectName" className='block text-sm font-medium mb-2'>Project name</label>
                                    <input
                                        type="text"
                                        id="projectName"
                                        className={`w-full bg-gray-800 border ${validationErrors.tokenName ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="Enter your project name"
                                        onChange={(e) => settTokenName(e.target.value)}
                                    />
                                    {validationErrors.tokenName && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenName}</p>}
                                </div>

                                <div>
                                    <label className="block text-sm font-medium mb-2" htmlFor="projectDesc">Project description</label>
                                    <textarea
                                        id="projectDesc"
                                        className={`w-full h-[200px] bg-gray-800 border ${validationErrors.tokenDescription ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background resize-none`}
                                        placeholder="Describe your projects"
                                        onChange={(e) => setTokenDescription(e.target.value)}
                                    />
                                    {validationErrors.tokenDescription && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenDescription}</p>}
                                </div>

                                <div>
                                    <label className="block text-sm font-medium mb-2" htmlFor="projectSymb">Project symbol</label>
                                    <input
                                        type="text"
                                        id="projectSymb"
                                        className={`w-full bg-gray-800 border ${validationErrors.tokenSymbol ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="Set token symbol"
                                        onChange={(e) => settTokenSymbol(e.target.value.toUpperCase())}
                                    />
                                    {validationErrors.tokenSymbol && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenSymbol}</p>}
                                </div>

                                <div>
                                    <label className="block text-sm font-medium mb-2" htmlFor="projectImage">Project Image</label>
                                    <DragAndDropFileInput
                                        singleFile={true}
                                        onFileSelect={function (files: File[]): void {
                                            setTokenImage(files[0]);
                                        }}
                                        id={'file'}
                                    />
                                    {validationErrors.tokenImage && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenImage}</p>}
                                </div>

                                <div>
                                    <label htmlFor="webAddress" className="block text-sm font-medium mb-2">Website Address</label>
                                    <input
                                        type="url"
                                        id="webAddress"
                                        className={`w-full bg-gray-800 border ${validationErrors.tokenWebsite ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="https://your-website.com"
                                        onChange={(e) => setTokenWebsite(e.target.value)}
                                    />
                                    {validationErrors.tokenWebsite && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenWebsite}</p>}
                                </div>

                                <div>
                                    <label htmlFor="twithand" className="block text-sm font-medium mb-2">Twitter Handle</label>
                                    <input
                                        type="text"
                                        id="twithand"
                                        className={`w-full bg-gray-800 border ${validationErrors.tokenTwitter ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="@yourhandle"
                                        onChange={(e) => setTokenTwitter(e.target.value)}
                                    />
                                    {validationErrors.tokenTwitter && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenTwitter}</p>}
                                </div>

                                <div>
                                    <label htmlFor="discord" className="block text-sm font-medium mb-2">Discord Channel</label>
                                    <input
                                        type="url"
                                        id="discord"
                                        className={`w-full bg-gray-800 border ${validationErrors.tokenDiscord ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="https://discord.gg/your-channel"
                                        onChange={(e) => setTokenDiscord(e.target.value)}
                                    />
                                    {validationErrors.tokenDiscord && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenDiscord}</p>}
                                </div>
                            </div>

                            <div className="flex justify-end mt-8">
                                <button
                                    type="button"
                                    className="flex items-center justify-center bg-custom-light-purple hover:bg-indigo-600 text-white px-6 py-2 rounded transition-colors"
                                    onClick={handleStep1Submit}
                                >
                                    Next Step
                                    <ArrowRight className="ml-2 h-4 w-4" />
                                </button>
                            </div>
                        </form>
                    ) : (
                        <form className="flex flex-col justify-center w-full max-w-[500px] mx-auto mb-10 mt=10">
                            <div className="space-y-6">
                                <div>
                                    <label htmlFor="initialSupply" className="block text-sm font-medium mb-2">Initial Supply</label>
                                    <input
                                        type="number"
                                        id="initialSupply"
                                        className={`w-full bg-gray-800 border ${validationErrors.initialSupply ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="Enter initial token supply"
                                        onChange={(e) => setInitialSupply(e.target.value)}
                                    />
                                    {validationErrors.initialSupply && <p className="text-red-500 text-sm mt-1">{validationErrors.initialSupply}</p>}
                                </div>

                                <div>
                                    <label htmlFor="pricePerToken" className="block text-sm font-medium mb-2">Price per Token (SOL)</label>
                                    <input
                                        type="number"
                                        id="pricePerToken"
                                        step="0.000000001"
                                        className={`w-full bg-gray-800 border ${validationErrors.pricePerToken ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`}
                                        placeholder="Enter price per token in SOL"
                                        onChange={(e) => setPricePerToken(e.target.value)}
                                    />
                                    {validationErrors.pricePerToken && <p className="text-red-500 text-sm mt-1">{validationErrors.pricePerToken}</p>}
                                </div>
                            </div>

                            <div className="flex justify-between mt-8">
                                {/* <button
                                    type="button"
                                    className="flex items-center justify-center bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded transition-colors"
                                    onClick={() => setCurrentStep(1)}
                                >
                                    Back
                                </button> */}
                                <button
                                    type="button"
                                    disabled={loading.bool}
                                    className="flex items-center justify-center bg-custom-light-purple hover:bg-indigo-600 text-white px-6 py-2 rounded transition-colors"
                                    onClick={handleStep2Submit}
                                >
                                    {loading.bool ? loading.msg + "..." : "Initialize Vault"}
                                    <ArrowRight className="ml-2 h-4 w-4" />
                                </button>
                            </div>
                        </form>
                    )}
                </div>

                <div className='flex flex-col items-center justify-center overflow-hidden w-full'>
                    {result && <Link to={`https://explorer.solana.com/tx/${result}?cluster=devnet`} className='text-green-500 underline'>link to TX hash</Link>}
                    {error && <p className='text-red-500'>{error}</p>}
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

export default CreateCoin;