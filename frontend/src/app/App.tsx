import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LanguageProvider } from "@/contexts/LanguageContext";
import { AuthProvider } from "@/contexts/AuthContext";
import LandingPage from "@/features/marketing/pages/LandingPage";
import SolutionPage from "@/features/cv-analysis/pages/SolutionPage";
import WriteMailPage from "@/features/content-generation/pages/WriteMailPage";
import WriteCoverLetterPage from "@/features/content-generation/pages/WriteCoverLetterPage";
import AboutPage from "@/features/marketing/pages/AboutPage";
import ContactPage from "@/features/marketing/pages/ContactPage";
import AuthPage from "@/features/auth/pages/AuthPage";
import SignUpPage from "@/features/auth/pages/SignUpPage";
import OAuthCallbackPage from "@/features/auth/pages/OAuthCallbackPage";
import NotFound from "@/pages/NotFound";
import ChatbotWidget from "@/components/ChatbotWidget";
import ProtectedRoute from "@/shared/components/auth/ProtectedRoute";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <LanguageProvider>
      <AuthProvider>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/auth" element={<AuthPage />} />
              <Route path="/signup" element={<SignUpPage />} />
              <Route path="/auth/callback" element={<OAuthCallbackPage />} />
              <Route element={<ProtectedRoute />}>
                <Route path="/solution" element={<SolutionPage />} />
                <Route path="/write-mail" element={<WriteMailPage />} />
                <Route path="/write-cover-letter" element={<WriteCoverLetterPage />} />
              </Route>
              <Route path="/about" element={<AboutPage />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
            <ChatbotWidget />
          </BrowserRouter>
        </TooltipProvider>
      </AuthProvider>
    </LanguageProvider>
  </QueryClientProvider>
);

export default App;
