import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ThemeProvider } from "@/components/providers/theme-provider";
import { Toaster } from "@/components/ui/sonner";
import "./globals.css";

// Sans — Geist as the working default. Design target is Google Sans;
// to switch, add the licensed font files and load via next/font/local
// (see .claude/skills/shadcn-ui-design/assets/fonts.ts).
const fontSans = Geist({
  variable: "--font-sans",
  subsets: ["latin"],
});

// Mono — Geist Mono (matches the design token font/family/mono).
const fontMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Create Skill Design",
  description: "Next.js + Tailwind v4 + shadcn/ui, driven by a Figma design system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${fontSans.variable} ${fontMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-background text-foreground font-sans">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
