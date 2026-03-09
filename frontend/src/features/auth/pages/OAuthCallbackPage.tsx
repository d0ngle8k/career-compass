import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

const OAuthCallbackPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("token");
    const email = searchParams.get("email");

    if (token && email) {
      // Save token and email to localStorage
      localStorage.setItem("career-compass-token", token);
      localStorage.setItem("career-compass-email", decodeURIComponent(email));
      
      toast.success("Đăng nhập thành công!");
      
      // Navigate to home/dashboard and trigger a page reload to update auth state
      window.location.href = "/solution";
    } else {
      toast.error("Đăng nhập thất bại. Vui lòng thử lại.");
      navigate("/auth", { replace: true });
    }
  }, [searchParams, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center space-y-4">
        <Loader2 className="w-12 h-12 animate-spin mx-auto text-accent" />
        <p className="text-muted-foreground">Đang xử lý đăng nhập...</p>
      </div>
    </div>
  );
};

export default OAuthCallbackPage;
