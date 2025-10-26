// app/layout.js
import { ClerkProvider } from "@clerk/nextjs";
import { Inter } from "next/font/google"; // <-- IMPORT THIS
import './globals.css';

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "AI-Wildlife Monitoring",
  description: "Next.js App with Clerk",
};

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html lang="en" className={inter.className}>
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
