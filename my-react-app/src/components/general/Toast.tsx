import { useState, ReactNode } from 'react';
import { Copy, Check, X } from 'lucide-react';

interface ToastProps {
    message: ReactNode;
    type: 'success' | 'error';
    onClose: () => void;
}

export function Toast({ message, type, onClose }: ToastProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        let textToCopy = '';
        if (typeof message === 'string') {
            textToCopy = message;
        } else if (message && typeof message === 'object' && 'props' in message) {
            const props = message.props as { to?: string };
            if (props.to) {
                textToCopy = props.to.split('/tx/')[1]?.split('?')[0] || '';
            }
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
        <div className={`fixed top-4 z-4 left-1/2 transform -translate-x-1/2 flex items-center gap-2 px-4 py-3 rounded-full shadow-lg transition-all duration-300 animate-slide-up ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white`}>
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

export const useToast = () => {
    const [showToast, setShowToast] = useState(false);
    const [toastMessage, setToastMessage] = useState<ReactNode>('');
    const [toastType, setToastType] = useState<'success' | 'error'>('success');

    const showToastMessage = (message: ReactNode, type: 'success' | 'error') => {
        setToastMessage(message);
        setToastType(type);
        setShowToast(true);
        setTimeout(() => setShowToast(false), 5000);
    };

    return {
        showToast,
        toastMessage,
        toastType,
        showToastMessage,
        setShowToast
    };
}; 