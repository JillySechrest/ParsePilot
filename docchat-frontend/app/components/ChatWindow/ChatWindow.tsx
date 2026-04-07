'use client'

import {useState, useEffect, useRef} from 'react';
import styles from './ChatWindow.module.css';
import { authedFetch } from '@/lib/api';
import { matchesGlob } from 'path';

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
            const res = await authedFetch(`/chat/${documentId}/history`);
            if (res.ok) {
                const data = await res.json();
                setMessages(data.messages);
            }
        }
        loadHistory();
    }, [documentId]);

    // --- AUTO-SCROLL ---
    // When a new message is added, scroll to bottomg of chat view
    useEffect(() => {
        bottomeRef.current?.scrollIntoView({behavior: 'smooth'});
    }, [messages]);

    // --- SEND MESSAGE ---
    async function handleSend() {
        const trimmed = input.trim();
        if (!trimmed || loading) return; // Do not send empty/duplicate reqs

        // STEP 1: Create user message
        const userMessage: Message = {
            id: crypto.randomUUID(), // Generate temp ID for UI
            role: 'user',
            content: trimmed,
            timestamp: new Date().toISOString(),
        };

        // STEP 2: Optimistic update - show message immediately
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
        // STEP 3: Send to backend
        const res = await authedFetch(`/chat/${documentId}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({question: trimmed}),
        });

        if(!res.ok) throw new Error('Failed to get a response');

        const data = await res.json();

        // STEP 4: Append agent's response
        const assignmentMessage: Message = {
            id: data.messageId,
            role: 'assistant',
            content: data.answer,
            timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assignmentMessage]);
        } catch {
            setMessages((prev) => [
                ...prev,
                {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    content: 'Sorry, something went wrong. Please try again.',
                    timestamp: new Date().toISOString(),
                }
            ]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.container}>
            {/* MESSAGE LIST */}
            <div className={styles.messageList}>
                {messages.map((msg) => (
                <div 
                    key={msg.id} 
                    className={
                        msg.role === 'user' ? styles.userMessage : styles.aiMessage
                    }
                >
                    <p>{msg.content}</p>
                </div>
                ))}
                {loading && <div className={styles.typing}>Thinking...</div>}
                <div ref ={bottomeRef} /> {/*Invisible anchor for auto-scroll*/}           
            </div>

            {/*INPUT AREA*/}
            <div className={styles.inputArea}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Send document query..."
                    disabled={loading}
                />
                <button onClick={handleSend} disabled={loading || !input.trim()}>
                    Send
                </button>
            </div>
        </div>
    );
}
