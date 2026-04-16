/**
 * Firebase Configuration for ProVerBs Legal AI
 *
 * Get your config from Firebase Console:
 * https://console.firebase.google.com/project/YOUR_PROJECT/settings/general
 */

// Replace these with your actual Firebase config from the console
export const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "",
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "",
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "",
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || "",
};

// Backend API configuration
export const apiConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080",
  conversationPath: "/api/conversation",
  audioPath: "/api/audio",
};

// App configuration
export const appConfig = {
  appName: "ProVerBs Legal AI",
  appVersion: "1.0.0",
  maxMessageLength: 2000,
  audioVoice: "en-US-AriaNeural",
};
