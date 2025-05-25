import { useState, ReactNode, isValidElement } from 'react'
import {  ArrowRight, X, Copy, Check } from 'lucide-react';
import { useSolana } from '../solanaClient/index';
import { uploadFile } from '../solanaClient/usePinta';
import DragAndDropFileInput from '../components/general/dragNdrop';
import { Link } from 'react-router-dom';
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
}

interface ToastProps {
    message: ReactNode;
    type: 'success' | 'error';
    onClose: () => void;
}

function Toast({ message, type, onClose }: ToastProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        // If message is a React element (Link), extract the href
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
        <div className={`fixed top-4 z-4 left-1/2 transform -translate-x-1/2 flex items-center gap-2 px-4 py-3 rounded-full shadow-lg transition-all duration-300 animate-slide-up ${
            type === 'success' ? 'bg-green-500' : 'bg-red-500'
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
    // const [preview, setPreview] = useState<string | null>(null);
    const [tokenName, settTokenName] = useState("");
    const [tokenSymbol, settTokenSymbol] = useState("");
    const [loading, setLoading] = useState({
        bool: false,
        msg: ""
    })
    // const [tokenUri, setTokenUri] = useState("");
    const [tokenDescription, setTokenDescription] = useState("");
    const [tokenImage, setTokenImage] = useState<File | null>(null);
    const [tokenWebsite, setTokenWebsite] = useState("");
    const [tokenTwitter, setTokenTwitter] = useState("");
    const [tokenDiscord, setTokenDiscord] = useState("");
    const {CreateTokenMint} = useSolana()
    const [error, setError] = useState<string | null>(null);
    const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});
    // const handleImageChange = (e: any) => {
    //     const file = e.target.files[0];
    //     if (file && file.type.startsWith('image/')) {
    //         setPreview(URL.createObjectURL(file));
    //     }
    // };
    const [result, setResult] = useState<string | null>(null);
    const [showToast, setShowToast] = useState(false);
    const [toastMessage, setToastMessage] = useState<ReactNode>('');
    const [toastType, setToastType] = useState<'success' | 'error'>('success');

    const validateForm = (): boolean => {
        const errors: ValidationErrors = {};
        
        // Token Name validation
        if (!tokenName.trim()) {
            errors.tokenName = "Token name is required";
        } else if (tokenName.length > 50) {
            errors.tokenName = "Token name must be less than 50 characters";
        }

        // Token Symbol validation
        if (!tokenSymbol.trim()) {
            errors.tokenSymbol = "Token symbol is required";
        } else if (!/^[A-Z0-9]{2,10}$/.test(tokenSymbol)) {
            errors.tokenSymbol = "Token symbol must be 2-10 uppercase letters or numbers";
        }

        // Description validation
        if (!tokenDescription.trim()) {
            errors.tokenDescription = "Description is required";
        } else if (tokenDescription.length > 1000) {
            errors.tokenDescription = "Description must be less than 1000 characters";
        }

        // Website validation
        if (!tokenWebsite.trim()) {
            errors.tokenWebsite = "Website is required";
        } else if (!/^https?:\/\/.+/.test(tokenWebsite)) {
            errors.tokenWebsite = "Please enter a valid URL starting with http:// or https://";
        }

        // Twitter validation
        if (!tokenTwitter.trim()) {
            errors.tokenTwitter = "Twitter handle is required";
        } else if (!/^@?[A-Za-z0-9_]{1,15}$/.test(tokenTwitter)) {
            errors.tokenTwitter = "Please enter a valid Twitter handle";
        }

        // Discord validation
        if (!tokenDiscord.trim()) {
            errors.tokenDiscord = "Discord channel is required";
        } else if (!/^https?:\/\/discord\/+/.test(tokenDiscord)) {
            errors.tokenDiscord = "Please enter a valid Discord invite link";
        }

        // Image validation
        if (!tokenImage) {
            errors.tokenImage = "Project image is required";
        }

        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const showToastMessage = (message: ReactNode, type: 'success' | 'error') => {
        setToastMessage(message);
        setToastType(type);
        setShowToast(true);
        // Auto-hide after 5 seconds
        setTimeout(() => setShowToast(false), 5000);
    };

    return (
        <div className='relative'>
            <style>{styles}</style>
            <div className="h-64 z-10 crtGradient background-container  top-10 left-10  ...">
                <div className="h-40  justify-center...">
                    <div className="flex flex-col items-center justify-center h-full">
                        <h1 className="text-5xl font-bold text-custom-dark-blue mb-4 text-center">Launch a new Project</h1>
                        <p className="text-gray-800 max-w-lg mx-auto text-center">
                        Build your reputation in the Web3 ecosystem as you bring your vision to life on Notty Terminal.
                        </p>
                    </div>
                </div>
            </div>

            <div className="h-[calc(100vh+10rem)] bg-custom-dark-blue "></div>
            <div className="flex justify-center items-center mt-10 flex-col  absolute left-16 right-16 border-gray-600 border  top-36 h-218 bg-custom-dark-blue z-10 p-4 text-white rounded p-10">
                {/* <article className="flex  justify-self-end self-start">lwa</article> */}
                <form method='POST' className="flex flex-col justify-center w-full max-w-[500px] mx-auto mb-10 mt=10">
                    <div className="mb-8">
                        <h1 className="text-2xl font-bold mb-2">Project details</h1>
                        <p className="text-gray-400">Provide important details about your project</p>
                    </div>
                    <div className="space-y-6">
                        <div>
                            <label htmlFor="projectName" className='block text-sm font-medium mb-2'>Project name</label>
                            <input 
                                type="text" 
                                name="" 
                                id="projectName" 
                                className={`w-full bg-gray-800 border ${validationErrors.tokenName ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`} 
                                placeholder="Enter your project name" 
                                onChange={(e)=>settTokenName(e.target.value)} 
                            />
                            {validationErrors.tokenName && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenName}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2" htmlFor="projectDesc">Project description</label>
                            <textarea 
                                name="" 
                                id="projectDesc" 
                                className={`w-full h-[200px] bg-gray-800 border ${validationErrors.tokenDescription ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background resize-none`} 
                                placeholder="Describe your projects" 
                                onChange={(e)=>setTokenDescription(e.target.value)} 
                            />
                            {validationErrors.tokenDescription && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenDescription}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2" htmlFor="projectSymb">Project symbol</label>
                            <input 
                                type="text" 
                                name="" 
                                id="projectSymb" 
                                className={`w-full bg-gray-800 border ${validationErrors.tokenSymbol ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`} 
                                placeholder="Set token symbol" 
                                onChange={(e)=>settTokenSymbol(e.target.value.toUpperCase())} 
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
                                name="" 
                                id="webAddress" 
                                className={`w-full bg-gray-800 border ${validationErrors.tokenWebsite ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`} 
                                placeholder="https://your-website.com" 
                                onChange={(e)=>setTokenWebsite(e.target.value)} 
                            />
                            {validationErrors.tokenWebsite && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenWebsite}</p>}
                        </div>
                        <div>
                            <label htmlFor="twithand" className="block text-sm font-medium mb-2">Twitter Handle</label>
                            <input 
                                type="text" 
                                name="" 
                                id="twithand" 
                                className={`w-full bg-gray-800 border ${validationErrors.tokenTwitter ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`} 
                                placeholder="@yourhandle" 
                                onChange={(e)=>setTokenTwitter(e.target.value)} 
                            />
                            {validationErrors.tokenTwitter && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenTwitter}</p>}
                        </div>
                        <div>
                            <label htmlFor="discord" className="block text-sm font-medium mb-2">Discord Channel</label>
                            <input 
                                type="url" 
                                name="" 
                                id="discord" 
                                className={`w-full bg-gray-800 border ${validationErrors.tokenDiscord ? 'border-red-500' : 'border-gray-700'} rounded px-4 py-2 text-white no-background`} 
                                placeholder="https://discord.gg/your-channel" 
                                onChange={(e)=>setTokenDiscord(e.target.value)} 
                            />
                            {validationErrors.tokenDiscord && <p className="text-red-500 text-sm mt-1">{validationErrors.tokenDiscord}</p>}
                        </div>
                    </div>
                    <div className="flex justify-start mt-8">
                        <button
                            type="button"
                            disabled={loading.bool}
                            className="flex items-center justify-center bg-custom-light-purple hover:bg-indigo-600 text-white px-6 py-2 rounded transition-colors"
                            onClick={async ()=>{
                                setError("")
                                setResult("")
                                setLoading({bool: true, msg: "loading"})
                                
                                if (!validateForm()) {
                                    setLoading({bool: false, msg: ""})
                                    return;
                                }

                                try {
                                    // First upload the image and metadata to IPFS
                                    if (!tokenImage) {
                                        setLoading({bool: false, msg:''})
                                        return
                                    }
                                    const metadataUrl = await uploadFile(tokenImage, {
                                        name: tokenName,
                                        symbol: tokenSymbol,
                                        description: tokenDescription,
                                        website: tokenWebsite,
                                        twitter: tokenTwitter,
                                        discord: tokenDiscord
                                    });
                                    console.log('called')
                                    if (metadataUrl.length === 0) {
                                        setLoading({bool: false, msg:''})
                                        showToastMessage("Failed to upload token", "error");
                                        return
                                    }
                                    setLoading({bool: true, msg: "uploading MetaData"})
                                    // Then create the token with the metadata URL
                                    if (CreateTokenMint) {
                                        console.log('called')
                                        const txHash = await CreateTokenMint(tokenName, tokenSymbol, metadataUrl);

                                        if (txHash) {
                                            setResult(txHash);
                                            showToastMessage(
                                                <Link to={`https://explorer.solana.com/tx/${txHash}?cluster=devnet`} className='underline'>
                                                    Transaction successful! View on Explorer
                                                </Link>,
                                                "success"
                                            );
                                        } else {
                                            showToastMessage("Please ensure you have Phantom extension installed", "error");
                                        }
                                    }
                                } catch (e: any) {
                                    console.error(e)
                                    showToastMessage(e.message, "error");
                                }
                                finally{
                                    setLoading({bool: false, msg:''})
                                }
                            }}
                        >
                            {loading.bool ? loading.msg + "..." : "Mint"}
                            <ArrowRight className="ml-2 h-4 w-4" />
                        </button>
                    </div>
                </form>
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
    )
}

export default CreateCoin