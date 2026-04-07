
type Props = {
    params: {docId: string};
};

export default function ChatPage({ params }: Props) {
    // params.docId --> gives doc ID from URL
    return <div><b>Chat about document</b>: {params.docId}</div>;
}