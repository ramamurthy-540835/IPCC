import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = { title: "IPCC Climate AI", description: "Explore climate science with evidence-backed AI." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
