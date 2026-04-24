// app/layout.js
import { Inter } from "next/font/google"; 
import './globals.css';

// Temporarily commenting out Clerk until API keys are provided
// import { ClerkProvider } from "@clerk/nextjs";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "AI-Wildlife Monitoring",
  description: "Next.js App with Clerk",
};

export default function RootLayout({ children }) {
  return (
    // <ClerkProvider>
      <html lang="en" className={inter.className}>
        <body>{children}</body>
      </html>
    // </ClerkProvider>
  );
}
