import { createContext, useEffect, useState } from "react";
import { getMe, login as loginApi, signup as signupApi } from "../api/authApi";
import { getToken, removeToken, setToken } from "../utils/token";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setAuthToken] = useState(getToken());
  const [loading, setLoading] = useState(true);

  const login = async ({ email, password }) => {
    try {
      console.log("1. Calling /login");

      const data = await loginApi({ email, password });
      console.log("2. Login response:", data);

      setToken(data.access_token);
      setAuthToken(data.access_token);

      console.log("3. Calling /me");

      const currentUser = await getMe(data.access_token);
      console.log("4. Current user:", currentUser);

      setUser(currentUser);

      console.log("5. Login completed");

      return currentUser;
    } catch (error) {
      console.error("LOGIN ERROR:", error);
      throw error;
    }
};

  const signup = async ({ username, email, password }) => {
    await signupApi({ username, email, password });
    return login({ email, password });
  };

  const logout = () => {
    removeToken();
    setAuthToken(null);
    setUser(null);
  };

  useEffect(() => {
    const initializeAuth = async () => {
      const savedToken = getToken();

      if (!savedToken) {
        setLoading(false);
        return;
      }

      try {
        const currentUser = await getMe(savedToken);
        setAuthToken(savedToken);
        setUser(currentUser);
      } catch (error) {
        removeToken();
        setAuthToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContext;