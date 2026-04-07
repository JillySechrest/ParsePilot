'use client'

import {useState, useEffect, useRef} from 'react';
import styles from './ChatWindow.module.css';

type Message = {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
};

type Props = {
    documentId: string;
};

export default function ChatWindow({documentId}: Props) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const bottomeRef = useRef<HTMLDivElement>(null);

    // --- LOAD CHAT HISTORY --
    // On mount, fetch chat history for the document
    useEffect(() => {
        async function loadHistory() {
            const res = await fetch(`api/chat/${documentId}/history`);
            if (res.ok) {
                const data = await res.json();
                setMessages(data.messages);
            }
        }
        loadHistory();
    }, [documentId]);

    // --- AUTO-SCROLL ---
    // When a new message is added, scroll to bottomg of chat view
    
}