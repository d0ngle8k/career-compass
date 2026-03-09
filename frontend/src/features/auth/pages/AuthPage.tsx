import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Eye, EyeOff, Loader2, LogIn } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { OAuthButtons } from "../components/OAuthButtons";

const AuthPage = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { user, login, loading } = useAuth();
  const { t } = useLanguage();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (user) navigate("/solution", { replace: true });
  }, [user, navigate]);

  useEffect(() => {
    const oauthError = searchParams.get("error");
    if (!oauthError) return;

    toast.error(`OAuth error: ${decodeURIComponent(oauthError)}`);
    searchParams.delete("error");
    setSearchParams(searchParams, { replace: true });
  }, [searchParams, setSearchParams]);

  const handleLogin = async () => {
    if (!email.trim() || !password) return;
    try {
      await login(email.trim(), password);
      toast.success(t("auth.login.success"));
      navigate("/solution");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : t("solution.analyze.error"));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="glass-card rounded-2xl p-8 space-y-6">
          <div className="text-center">
            <h1 className="font-display text-2xl font-bold text-foreground">
              CV<span className="text-accent">Genius</span>
            </h1>
            <p className="text-muted-foreground mt-2 text-sm">{t("auth.subtitle")}</p>
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">{t("auth.email")}</Label>
              <Input
                id="email"
                type="email"
                placeholder="admin@careercompass.local"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">{t("signup.password")}</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleLogin()}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <Button variant="cta" className="w-full gap-2" onClick={handleLogin} disabled={loading || !email.trim() || !password}>
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <LogIn className="w-4 h-4" />}
              {t("auth.login.button")}
            </Button>
          </div>

          {/* OAuth Buttons */}
          <OAuthButtons />

          <p className="text-center text-sm text-muted-foreground">
            {t("auth.no.account")}{" "}
            <Link to="/signup" className="text-accent hover:underline font-medium">
              {t("auth.signup.link")}
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default AuthPage;
