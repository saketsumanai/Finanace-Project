/**
 * Firebase Authentication Service
 */
import {
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  updateProfile,
  User,
  UserCredential,
} from 'firebase/auth';
import { auth, googleProvider } from '@/config/firebase';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
    full_name: string;
    role: string;
  };
}

class FirebaseAuthService {
  /**
   * Sign in with Google
   */
  async signInWithGoogle(): Promise<AuthResponse> {
    try {
      // Sign in with Google popup
      const result: UserCredential = await signInWithPopup(auth, googleProvider);
      const user = result.user;

      // Get Firebase ID token
      const idToken = await user.getIdToken();

      // Send to backend for verification and JWT creation
      const response = await axios.post<AuthResponse>(
        `${API_URL}/auth/google`,
        {
          id_token: idToken,
          email: user.email,
          full_name: user.displayName,
          profile_picture: user.photoURL,
        }
      );

      // Store JWT token
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      return response.data;
    } catch (error: any) {
      console.error('Google sign-in error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to sign in with Google');
    }
  }

  /**
   * Sign in with email and password
   */
  async signInWithEmail(email: string, password: string): Promise<AuthResponse> {
    try {
      // Sign in with Firebase
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // Get Firebase ID token
      const idToken = await user.getIdToken();

      // Send to backend for JWT creation
      const response = await axios.post<AuthResponse>(
        `${API_URL}/auth/firebase-login`,
        {
          id_token: idToken,
          email: user.email,
        }
      );

      // Store JWT token
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      return response.data;
    } catch (error: any) {
      console.error('Email sign-in error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to sign in');
    }
  }

  /**
   * Register with email and password
   */
  async registerWithEmail(
    email: string,
    password: string,
    fullName: string
  ): Promise<AuthResponse> {
    try {
      // Create user in Firebase
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // Update profile with full name
      await updateProfile(user, {
        displayName: fullName,
      });

      // Get Firebase ID token
      const idToken = await user.getIdToken();

      // Send to backend for user creation and JWT
      const response = await axios.post<AuthResponse>(
        `${API_URL}/auth/firebase-register`,
        {
          id_token: idToken,
          email: user.email,
          full_name: fullName,
        }
      );

      // Store JWT token
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      return response.data;
    } catch (error: any) {
      console.error('Registration error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to register');
    }
  }

  /**
   * Sign out
   */
  async signOut(): Promise<void> {
    try {
      await signOut(auth);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    } catch (error) {
      console.error('Sign out error:', error);
      throw new Error('Failed to sign out');
    }
  }

  /**
   * Get current Firebase user
   */
  getCurrentUser(): User | null {
    return auth.currentUser;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  /**
   * Get stored user data
   */
  getStoredUser(): any {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
}

export const firebaseAuthService = new FirebaseAuthService();
