# ParsePilot Frontend

This is the frontend for ParsePilot, a document chat app built to make uploaded files feel a little less static. It handles the user-facing side of the flow: signing users in, sending authenticated API requests, uploading files, browsing a document library, and opening chat screens for individual documents.

The app is still taking shape, so this README is written around what is actually in the folder today. A few routes and components are wired up only as scaffolding for the next round of implementation.

## Stack

- Next.js 16 App Router
- React 19
- TypeScript
- Tailwind CSS 4
- AWS Amplify Auth for Cognito session handling

## What This App Does

- Configures Cognito authentication in the root layout
- Sends authenticated requests to the backend with a bearer token
- Provides a file upload component for PDF, CSV, and Markdown documents
- Lists uploaded documents and links ready documents into a chat route
- Includes a chat window component that loads history and sends new questions

## Current Route Status

| Route | Status | Notes |
| --- | --- | --- |
| `/` | Placeholder | Default create-next-app landing page is still present |
| `/upload` | Incomplete | Route file exists but is empty |
| `/library` | Partial | Fetches a document list and links ready items into chat |
| `/chat` | Placeholder | Layout shell only |
| `/chat/[docId]` | Placeholder | Displays the document id only |

## Environment Variables

Create a local environment file such as `.env.local` and define:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_COGNITO_USER_POOL_ID=your-user-pool-id
NEXT_PUBLIC_COGNITO_CLIENT_ID=your-user-pool-client-id
```

These values are used by:

- `NEXT_PUBLIC_API_URL`: base URL for backend requests made through `lib/api.ts`
- `NEXT_PUBLIC_COGNITO_USER_POOL_ID`: Cognito user pool configured in `app/layout.tsx`
- `NEXT_PUBLIC_COGNITO_CLIENT_ID`: Cognito app client configured in `app/layout.tsx`

## Getting Started

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open `http://localhost:3000` in your browser.

Other available scripts:

```bash
npm run build
npm run start
npm run lint
```

## Project Structure

```text
app/
	components/
		ChatWindow/     Reusable chat UI and backend messaging flow
		FileUpload/     Reusable upload UI and document submission flow
	chat/
		[docId]/        Document-specific chat route
		page.tsx        Chat placeholder route
	library/          Document list view
	upload/           Upload route stub
	layout.tsx        Global layout and Amplify auth configuration
	page.tsx          Current landing-page placeholder
lib/
	api.ts            Authenticated fetch helper
```

## Backend Expectations

The frontend currently expects a backend that exposes endpoints similar to:

- `POST /documents/upload`
- `GET /chat/:documentId/history`
- `POST /chat/:documentId/ask`
- A document listing endpoint for the library page

Requests sent through `authedFetch` include the current Cognito ID token as a bearer token.

## Implementation Notes

- The library page currently fetches from `api/documents`, which should be aligned with the backend base URL strategy used elsewhere.
- The upload route exists, but the page itself has not been wired to the `FileUpload` component yet.
- The `ChatWindow` and `FileUpload` components exist, but the route pages are not yet composed around them.
- The landing page metadata and content are still using default Next.js starter values.

## Next Recommended Steps

1. Replace the default home page with a product landing page or redirect.
2. Wire `app/upload/page.tsx` to render the upload component.
3. Connect `app/chat/[docId]/page.tsx` to the `ChatWindow` component.
4. Standardize document list fetching to use the authenticated API helper.
