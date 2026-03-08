import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { motion } from "framer-motion";
import { Upload, FileText, Sparkles, X } from "lucide-react";
import ScoreDisplay from "@/components/solution/ScoreDisplay";
import ChatbotWidget from "@/components/ChatbotWidget";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

const SolutionPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<null | {
    score: number;
    strengths: string[];
    weaknesses: string[];
    improvement_tips: string[];
  }>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast.error(t("solution.file.too.large"));
        return;
      }
      setCvFile(file);
    }
  };

  const extractTextFromFile = async (file: File): Promise<string> => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve((e.target?.result as string) || `[File: ${file.name}]`);
      reader.onerror = () => resolve(`[File: ${file.name}]`);
      reader.readAsText(file);
    });
  };

  const handleAnalyze = async () => {
    if (!cvFile || !jdText.trim()) return;
    if (!user) { toast.error(t("solution.login.required")); navigate("/auth"); return; }
    if (jdText.trim().length < 20) { toast.error(t("solution.jd.too.short")); return; }

    setIsAnalyzing(true);
    try {
      const cvText = await extractTextFromFile(cvFile);
      if (cvText.trim().length < 30) { toast.error(t("solution.cv.unreadable")); setIsAnalyzing(false); return; }

      const { data, error } = await supabase.functions.invoke("analyze-cv", {
        body: { cvText, jdText: jdText.trim(), mode: "score_only" },
      });

      if (error) throw new Error(error.message || "Analysis failed");
      if (data?.error) throw new Error(data.error);
      setResults(data);
    } catch (err: any) {
      console.error("Analysis error:", err);
      toast.error(err.message || t("solution.analyze.error"));
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <section className="pt-28 pb-6 bg-muted/30">
        <div className="section-container text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-2">{t("solution.title")}</h1>
            <p className="text-muted-foreground text-lg">{t("solution.desc")}</p>
          </motion.div>
        </div>
      </section>

      <section className="py-8 bg-background flex-1">
        <div className="section-container">
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="glass-card rounded-xl p-6">
                <h2 className="font-display font-semibold text-lg text-foreground mb-4 flex items-center gap-2">
                  <Upload className="w-5 h-5 text-accent" /> {t("solution.upload")}
                </h2>
                <div className="relative">
                  <input type="file" accept=".pdf,.docx,.txt" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" />
                  <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-accent/50 transition-colors">
                    {cvFile ? (
                      <div className="flex items-center justify-center gap-2">
                        <FileText className="w-5 h-5 text-accent" />
                        <span className="font-medium text-foreground">{cvFile.name}</span>
                        <button onClick={(e) => { e.stopPropagation(); setCvFile(null); }} className="text-muted-foreground hover:text-destructive"><X className="w-4 h-4" /></button>
                      </div>
                    ) : (
                      <>
                        <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                        <p className="text-sm text-muted-foreground">{t("solution.drag")}</p>
                        <p className="text-xs text-muted-foreground mt-1">{t("solution.maxsize")}</p>
                      </>
                    )}
                  </div>
                </div>
              </motion.div>

              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1 }} className="glass-card rounded-xl p-6">
                <h2 className="font-display font-semibold text-lg text-foreground mb-4 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-accent" /> {t("solution.jd")}
                </h2>
                <Textarea value={jdText} onChange={(e) => setJdText(e.target.value)} placeholder={t("solution.jd.placeholder")} rows={8} className="resize-none" />
              </motion.div>

              <Button variant="cta" size="lg" className="w-full gap-2" disabled={!cvFile || !jdText.trim() || isAnalyzing} onClick={handleAnalyze}>
                <Sparkles className="w-5 h-5" />
                {isAnalyzing ? t("solution.analyzing") : t("solution.analyze")}
              </Button>
            </div>

            <div className="lg:col-span-3">
              {isAnalyzing ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card rounded-xl p-12 flex flex-col items-center justify-center min-h-[400px]">
                  <div className="w-16 h-16 border-4 border-accent/30 border-t-accent rounded-full animate-spin mb-6" />
                  <p className="text-muted-foreground font-medium">{t("solution.ai.loading")}</p>
                  <p className="text-sm text-muted-foreground mt-1">{t("solution.ai.wait")}</p>
                </motion.div>
              ) : results ? (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                  <ScoreDisplay score={results.score} strengths={results.strengths} weaknesses={results.weaknesses} tips={results.improvement_tips} />
                </motion.div>
              ) : (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card rounded-xl p-12 flex flex-col items-center justify-center min-h-[400px] text-center">
                  <div className="w-20 h-20 bg-muted rounded-full flex items-center justify-center mb-6">
                    <Sparkles className="w-10 h-10 text-muted-foreground" />
                  </div>
                  <h3 className="font-display text-xl font-semibold text-foreground mb-2">{t("solution.noresult.title")}</h3>
                  <p className="text-muted-foreground max-w-sm">{t("solution.noresult.desc")}</p>
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </section>

      <ChatbotWidget jdText={jdText} cvFileName={cvFile?.name} />
      <Footer />
    </div>
  );
};

export default SolutionPage;
