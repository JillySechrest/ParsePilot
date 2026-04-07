'use client';

import {useState, useCallback} from 'react';
import {useRouter} from 'next/navigation';
import styles from './FileUpload.module.css';

// Only supported file extensions for upload & max file size (10MB)
const ALLOWED_TYPES = [
    'application/pdf',
    'text/csv',
    'text/markdown'
];
const MAX_SIZE_MB = 10;

export default function FileUpload() {
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    const handleUpload = useCallback(async (file: File) => {
        // VALIDATION
        // Check file type --> if file is not in ALLOWED_TYPES array - reject file
        if(ALLOWED_TYPES.includes(file.type)) {
            setError('Only PDF, CSV, and MD files are allowed.');
            return;
        }
        // VALIDATION
        // Check file size --> if file is > MAX_SIZE_MB - reject file
        if(file.size > MAX_SIZE_MB * 1024 * 1024) {
            setError(`File must be under ${MAX_SIZE_MB}MB.`);
            return;
        } 
        setError(null);
        setUploading(true);
        
        try {
            // --- BUILD REQUEST ---
            // FormData sets correct Content-Type (multi-part/form-data) automatically
            const formData = new FormData();
            formData.append('file', file);

            // --- SEND REQUEST TO BACKEND ---
            // Content-Type header is set via FormData
            const response = await fetch('api/documents/upload', {
                method: 'POST',
                body: formData,
            });

            if(!response.ok) {
                throw new Error('Upload failed. Please try again.');
            }

            const data = await response.json();
            // data.documentID --> passed from backend after file store
            router.push(`/chat/${data.documentId}`);
        } catch (err) {
            setError(err instanceof Error ? err.message: 'An unexpected error occurred.');
        } finally {
            setUploading(false);
        }
    }, [router]);

    return (
        <div className={styles.dropZone}>
            <input
                type="file"
                accept=".pdf,.csv,.md"
                onChange={(e) => {
                    const file = e.target.files?.[0];
                    if(file) handleUpload(file);
                }}
                disabled={uploading}
            />
            {uploading && <p>Uploading...</p>}
            {error && <p className={styles.error}>{error}</p>}
        </div>
    );
}