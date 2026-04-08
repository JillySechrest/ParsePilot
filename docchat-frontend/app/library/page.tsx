'use client';

import {useState, useEffect} from 'react';
import Link from 'next/link';
import styles from './Library.module.css';
import { authedFetch } from '@/lib/api';

type Document = {
    id: string,
    filename: string,
    uploadedAt: string,
    status: 'processing' | 'ready' | 'error';
};

export default function LibraryPage() {
    const [docs, setDocs] = useState<Document[]>([]);

    useEffect(() => {
        async function fetchDocs() {
            const res = await authedFetch('/documents');
            if (res.ok) {
                const data = await res.json();
                setDocs(data.documents);
            }
        }
        fetchDocs();
    }, []);

    return(
        <div className={styles.container}>
            <h1>User Documents</h1>
            {docs.length === 0 ? (
                <p>No documents uploaded, yet. <Link href="/upload">Upload Document</Link></p>
            ) : (
                <ul className={styles.list}>
                    {docs.map((doc) => (
                        <li key={doc.id} className={styles.item}>
                            <span>{doc.filename}</span>
                            <span className={styles.status}>{doc.status}
                            </span>
                            {doc.status  === 'ready' ? (
                                <Link href={`/chat/${doc.id}`}> Chat</Link>
                            ) : (
                                <span className={styles.disabled}>Processing...</span>
                            )}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}