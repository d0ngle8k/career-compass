import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { motion } from "framer-motion";
import { Upload, FileText, Sparkles, X, Globe, Palette, Copy, Check, Download } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import { Document, Packer, Paragraph, TextRun } from "docx";
import { saveAs } from "file-saver";

type TemplateStyle = "formal" | "modern" | "creative";

const WriteCoverLetterPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { t } = useLanguage();
  const contentRef = useRef<HTMLDivElement>(null);
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [language, setLanguage] = useState<"vi" | "en">("vi");
  const [templateStyle, setTemplateStyle] = useState<TemplateStyle>("formal");
  const [isGenerating, setIsGenerating] = useState(false);
  const [copiedField, setCopiedField] = useState<string | null>(null);
  const [result, setResult] = useState<null | { cover_letter: string }>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { toast.error(t("solution.file.too.large")); return; }
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

  const copyToClipboard = (text: string, field: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(field);
    toast.success(t("letter.copied"));
    setTimeout(() => setCopiedField(null), 2000);
  };

  const handleGenerate = async () => {
    if (!cvFile || !jdText.trim()) return;
    if (!user) { toast.error(t("solution.login.required")); navigate("/auth"); return; }
    if (jdText.trim().length < 20) { toast.error(t("solution.jd.too.short")); return; }

    setIsGenerating(true);
    try {
      const cvText = await extractTextFromFile(cvFile);
      if (cvText.trim().length < 30) { toast.error(t("solution.cv.unreadable")); setIsGenerating(false); return; }

      const { data, error } = await supabase.functions.invoke("analyze-cv", {
        body: { cvText, jdText: jdText.trim(), language, templateStyle, mode: "cover_letter_only" },
      });

      if (error) throw new Error(error.message);
      if (data?.error) throw new Error(data.error);
      setResult(data);
    } catch (err: any) {
      console.error("Generate error:", err);
      toast.error(err.message || t("solution.analyze.error"));
    } finally {
      setIsGenerating(false);
    }
  };

  const exportPDF = async () => {
    if (!contentRef.current || !result) return;
    const html2pdf = (await import("html2pdf.js")).default;
    html2pdf()
      .set({
        margin: [15, 15, 15, 15],
        filename: "cover-letter.pdf",
        html2canvas: { scale: 2 },
        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      })
      .from(contentRef.current)
      .save();
    toast.success(t("export.pdf.success"));
  };

  const exportDOCX = async () => {
    if (!result) return;
    const lines = result.cover_letter.split("\n");
    const paragraphs = lines.map((line) => {
      const isHeading = line.startsWith("#");
      const cleanLine = line.replace(/^#+\s*/, "").replace(/\*\*/g, "");
      return new Paragraph({
        children: [new TextRun({ text: cleanLine, bold: isHeading, size: isHeading ? 28 : 22 })],
        spacing: { after: 200 },
      });
    });

    const doc = new Document({ sections: [{ properties: {}, children: paragraphs }] });
    const blob = await Packer.toBlob(doc);
    saveAs(blob, "cover-letter.docx");
    toast.success(t("export.docx.success"));
  };

  const templateStyles: { value: TemplateStyle; labelKey: string; descKey: string; icon: string }[] = [
    { value: "formal", labelKey: "template.formal", descKey: "template.formal.desc", icon: "📄" },
    { value: "modern", labelKey: "template.modern", descKey: "template.modern.desc", icon: "✨" },
    { value: "creative", labelKey: "template.creative", descKey: "template.creative.desc", icon: "🎨" },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <section className="pt-28 pb-6 bg-muted/30">
        <div className="section-container text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-2">{t("coverletter.title")}</h1>
            <p className="text-muted-foreground text-lg">{t("coverletter.desc")}</p>
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
                <Textarea value={jdText} onChange={(e) => setJdText(e.target.value)} placeholder={t("solution.jd.placeholder")} rows={6} className="resize-none" />
              </motion.div>

              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.15 }} className="glass-card rounded-xl p-6">
                <Label className="font-display font-semibold text-lg text-foreground mb-3 flex items-center gap-2">
                  <Globe className="w-5 h-5 text-accent" /> {t("solution.language")}
                </Label>
                <div className="flex gap-3 mt-3">
                  <Button variant={language === "vi" ? "default" : "outline"} size="sm" onClick={() => setLanguage("vi")}>🇻🇳 Tiếng Việt</Button>
                  <Button variant={language === "en" ? "default" : "outline"} size="sm" onClick={() => setLanguage("en")}>🇬🇧 English</Button>
                </div>
              </motion.div>

              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="glass-card rounded-xl p-6">
                <Label className="font-display font-semibold text-lg text-foreground mb-3 flex items-center gap-2">
                  <Palette className="w-5 h-5 text-accent" /> {t("solution.template.style")}
                </Label>
                <div className="grid grid-cols-1 gap-3 mt-3">
                  {templateStyles.map((ts) => (
                    <button key={ts.value} onClick={() => setTemplateStyle(ts.value)}
                      className={`flex items-start gap-3 p-3 rounded-lg border-2 text-left transition-all ${templateStyle === ts.value ? "border-accent bg-accent/5" : "border-border hover:border-accent/30"}`}>
                      <span className="text-xl mt-0.5">{ts.icon}</span>
                      <div>
                        <p className="font-medium text-sm text-foreground">{t(ts.labelKey)}</p>
                        <p className="text-xs text-muted-foreground mt-0.5">{t(ts.descKey)}</p>
                      </div>
                    </button>
                  ))}
                </div>
              </motion.div>

              <Button variant="cta" size="lg" className="w-full gap-2" disabled={!cvFile || !jdText.trim() || isGenerating} onClick={handleGenerate}>
                <Sparkles className="w-5 h-5" />
                {isGenerating ? t("solution.analyzing") : t("coverletter.generate")}
              </Button>
            </div>

            <div className="lg:col-span-3">
              {isGenerating ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card rounded-xl p-12 flex flex-col items-center justify-center min-h-[400px]">
                  <div className="w-16 h-16 border-4 border-accent/30 border-t-accent rounded-full animate-spin mb-6" />
                  <p className="text-muted-foreground font-medium">{t("solution.ai.loading")}</p>
                </motion.div>
              ) : result ? (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-display font-semibold text-foreground flex items-center gap-2">
                      <FileText className="w-5 h-5 text-accent" /> {t("letter.cover")}
                    </h3>
                    <div className="flex gap-2">
                      <Button variant="ghost" size="sm" onClick={() => copyToClipboard(result.cover_letter, "cover")} className="gap-1.5">
                        {copiedField === "cover" ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                        {copiedField === "cover" ? t("letter.copied") : t("letter.copy")}
                      </Button>
                      <Button variant="outline" size="sm" onClick={exportPDF} className="gap-1.5">
                        <Download className="w-4 h-4" /> PDF
                      </Button>
                      <Button variant="outline" size="sm" onClick={exportDOCX} className="gap-1.5">
                        <Download className="w-4 h-4" /> DOCX
                      </Button>
                    </div>
                  </div>
                  <div ref={contentRef} className="bg-muted/50 rounded-lg p-6">
                    <div className="text-sm text-foreground leading-relaxed prose prose-sm max-w-none">
                      <ReactMarkdown>{result.cover_letter}</ReactMarkdown>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card rounded-xl p-12 flex flex-col items-center justify-center min-h-[400px] text-center">
                  <div className="w-20 h-20 bg-muted rounded-full flex items-center justify-center mb-6">
                    <FileText className="w-10 h-10 text-muted-foreground" />
                  </div>
                  <h3 className="font-display text-xl font-semibold text-foreground mb-2">{t("coverletter.empty.title")}</h3>
                  <p className="text-muted-foreground max-w-sm">{t("coverletter.empty.desc")}</p>
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
};

export default WriteCoverLetterPage;
