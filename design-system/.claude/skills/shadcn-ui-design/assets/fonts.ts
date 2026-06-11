import localFont from "next/font/local"

// Sans — Google Sans (design token: font/family/sans)
// Google Sans is NOT on Google Fonts, so it cannot use next/font/google.
// Place the font files in /public/fonts/ and load them with next/font/local.
// If you don't have the licensed files, swap to a Google Fonts alternative:
//   import { Inter as googleSans } from "next/font/google"  // closest open fallback
export const googleSans = localFont({
  src: [
    { path: "../public/fonts/GoogleSans-Regular.woff2",  weight: "400", style: "normal" },
    { path: "../public/fonts/GoogleSans-Medium.woff2",   weight: "500", style: "normal" },
    { path: "../public/fonts/GoogleSans-SemiBold.woff2", weight: "600", style: "normal" },
    { path: "../public/fonts/GoogleSans-Bold.woff2",     weight: "700", style: "normal" },
  ],
  variable: "--font-google-sans",
  display: "swap",
})

// Mono — Geist Mono (design token: font/family/mono)
export const geistMono = localFont({
  src: "../public/fonts/GeistMono-Variable.woff2",
  variable: "--font-geist-mono",
  display: "swap",
})
