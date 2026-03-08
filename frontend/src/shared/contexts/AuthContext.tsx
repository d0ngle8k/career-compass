import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import { backendApi } from "@/shared/lib/backend-api";

type AuthUser = {
  email: string;
};

type AuthContextType = {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  loading: false,
  login: async () => {},
  signOut: async () => {},
});

const TOKEN_KEY = "career-compass-token";
const EMAIL_KEY = "career-compass-email";

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState<AuthUser | null>(() => {
    const email = localStorage.getItem(EMAIL_KEY);
    return email ? { email } : null;
  });
  const [loading, setLoading] = useState(false);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await backendApi.login(email, password);
      const nextToken = response.data.access_token;
      localStorage.setItem(TOKEN_KEY, nextToken);
      localStorage.setItem(EMAIL_KEY, email);
      setToken(nextToken);
      setUser({ email });
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    if (token) {
      try {
        await backendApi.logout(token);
      } catch {
        // Ignore logout API failures and clear local state anyway.
      }
    }

    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(EMAIL_KEY);
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, token, loading, login, signOut }),
    [user, token, loading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
