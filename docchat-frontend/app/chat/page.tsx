import styles from './Chat.module.css';

export default function ChatPage() {

    return (
        <div className={styles.container}>
            <div className={styles.messageList}>
            {/* Render message here */}
            </div>
            <div className={styles.inputArea}>
            {/* Input + send button here */}
            </div>
        </div>
    );
}