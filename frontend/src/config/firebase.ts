/**
 * Firebase Configuration
 */
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getAnalytics } from 'firebase/analytics';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyD4HRsEuLFiWl3hjLHxgfC11ejETsUGZnA",
  authDomain: "oil-gas-f78c8.firebaseapp.com",
  projectId: "oil-gas-f78c8",
  storageBucket: "oil-gas-f78c8.firebasestorage.app",
  messagingSenderId: "116758914066",
  appId: "1:116758914066:web:60c33e8bc77bc8293964cb",
  measurementId: "G-96ZKZ1DC5H"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);

// Initialize Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

// Initialize Analytics (optional)
export const analytics = typeof window !== 'undefined' ? getAnalytics(app) : null;

export default app;
