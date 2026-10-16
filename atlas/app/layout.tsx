import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The Copper Scroll Atlas",
  description: "Trace Copper Scroll claims through manuscript readings, candidate features, observations and exact sources.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
