import { Button } from "@/components/ui/button";
import { Chrome, Github } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:9000";

export const OAuthButtons = () => {
  const [loading, setLoading] = useState<"google" | "github" | null>(null);

  const handleGoogleLogin = async () => {
    setLoading("google");
    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/auth/google/login`);
      const data = await response.json();
      
      if (data.success && data.data.authorization_url) {
        // Redirect user to Google OAuth consent screen
        window.location.href = data.data.authorization_url;
      } else {
        throw new Error("Failed to initiate Google OAuth");
      }
    } catch (error) {
      console.error("Google OAuth error:", error);
      toast.error("Không thể đăng nhập bằng Google. Vui lòng thử lại.");
      setLoading(null);
    }
  };

  const handleGitHubLogin = async () => {
    setLoading("github");
    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/auth/github/login`);
      const data = await response.json();
      
      if (data.success && data.data.authorization_url) {
        // Redirect user to GitHub OAuth consent screen
        window.location.href = data.data.authorization_url;
      } else {
        throw new Error("Failed to initiate GitHub OAuth");
      }
    } catch (error) {
      console.error("GitHub OAuth error:", error);
      toast.error("Không thể đăng nhập bằng GitHub. Vui lòng thử lại.");
      setLoading(null);
    }
  };

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Hoặc tiếp tục với
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Button
          type="button"
          variant="outline"
          onClick={handleGoogleLogin}
          disabled={loading !== null}
          className="gap-2"
        >
          <Chrome className="w-4 h-4" />
          {loading === "google" ? "Đang xử lý..." : "Google"}
        </Button>

        <Button
          type="button"
          variant="outline"
          onClick={handleGitHubLogin}
          disabled={loading !== null}
          className="gap-2"
        >
          <Github className="w-4 h-4" />
          {loading === "github" ? "Đang xử lý..." : "GitHub"}
        </Button>
      </div>
    </div>
  );
};
