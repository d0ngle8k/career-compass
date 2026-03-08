import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, BarChart3, Mail, Sparkles, X, Globe } from "lucide-react";
import ScoreDisplay from "@/components/solution/ScoreDisplay";
import CoverLetterDisplay from "@/components/solution/CoverLetterDisplay";
import ChatbotWidget from "@/components/ChatbotWidget";

const SolutionPage = () => {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [language, setLanguage] = useState<"vi" | "en">("vi");
  const [activeTab, setActiveTab] = useState<"score" | "letter">("score");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<null | {
    score: number;
    strengths: string[];
    weaknesses: string[];
    improvement_tips: string[];
    email_subject: string;
    email_body: string;
    cover_letter: string;
  }>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert("File quá lớn. Vui lòng chọn file dưới 5MB.");
        return;
      }
      setCvFile(file);
    }
  };

  const handleAnalyze = async () => {
    if (!cvFile || !jdText.trim()) return;
    setIsAnalyzing(true);
    // Mock analysis - will be replaced with real AI backend
    setTimeout(() => {
      setResults({
        score: 78,
        strengths: [
          "Kinh nghiệm 3+ năm trong lĩnh vực IT Support phù hợp với yêu cầu",
          "Kỹ năng troubleshooting hardware/software được thể hiện rõ",
          "Có chứng chỉ CompTIA A+ liên quan trực tiếp đến vị trí",
        ],
        weaknesses: [
          "Thiếu kinh nghiệm với hệ thống ticketing (Jira/ServiceNow)",
          "Chưa đề cập kỹ năng networking (TCP/IP, DNS, DHCP)",
          "Cần bổ sung kinh nghiệm làm việc nhóm và giao tiếp khách hàng",
        ],
        improvement_tips: [
          "Thêm các số liệu cụ thể vào bullet points (VD: 'Hỗ trợ 50+ user/ngày')",
          "Bổ sung kỹ năng networking vào phần Skills",
          "Thêm project hoặc achievement nổi bật liên quan đến JD",
        ],
        email_subject: "Ứng tuyển vị trí IT Helpdesk/Support - [Tên bạn]",
        email_body: `Kính gửi Quý Anh/Chị,\n\nTôi viết email này để bày tỏ sự quan tâm đến vị trí IT Helpdesk/Support tại Quý Công ty. Với hơn 3 năm kinh nghiệm trong lĩnh vực hỗ trợ kỹ thuật và chứng chỉ CompTIA A+, tôi tin rằng mình có thể đóng góp hiệu quả cho đội ngũ IT của Quý Công ty.\n\nXin vui lòng tham khảo CV đính kèm để biết thêm chi tiết. Tôi rất mong có cơ hội trao đổi thêm.\n\nTrân trọng,\n[Tên bạn]`,
        cover_letter: `Kính gửi Quý Phòng Nhân sự,\n\nTôi hân hạnh được ứng tuyển vào vị trí IT Helpdesk/Support tại Quý Công ty. Qua hơn 3 năm kinh nghiệm làm việc trong môi trường IT Support, tôi đã tích lũy được nền tảng kỹ thuật vững chắc và kỹ năng xử lý sự cố hiệu quả.\n\nĐiểm nổi bật:\n• Hỗ trợ kỹ thuật cho 200+ nhân viên, đạt tỷ lệ giải quyết lần đầu 85%\n• Triển khai hệ thống backup tự động, giảm 40% thời gian downtime\n• Sở hữu chứng chỉ CompTIA A+ và kinh nghiệm với Windows/Linux\n\nTôi rất mong được đóng góp cho sự phát triển của Quý Công ty và sẵn sàng trao đổi thêm khi thuận tiện.\n\nTrân trọng,\n[Tên bạn]`,
      });
      setIsAnalyzing(false);
    }, 2500);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <section className="pt-28 pb-6 bg-muted/30">
        <div className="section-container text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-2">
              Phân tích CV thông minh
            </h1>
            <p className="text-muted-foreground text-lg">Upload CV và nhập JD để bắt đầu</p>
          </motion.div>
        </div>
      </section>

      <section className="py-8 bg-background flex-1">
        <div className="section-container">
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
            {/* Input Panel */}
            <div className="lg:col-span-2 space-y-6">
              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="glass-card rounded-xl p-6">
                <h2 className="font-display font-semibold text-lg text-foreground mb-4 flex items-center gap-2">
                  <Upload className="w-5 h-5 text-accent" /> Upload CV
                </h2>

                {/* File upload */}
                <div className="relative">
                  <input
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                  />
                  <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-accent/50 transition-colors">
                    {cvFile ? (
                      <div className="flex items-center justify-center gap-2">
                        <FileText className="w-5 h-5 text-accent" />
                        <span className="font-medium text-foreground">{cvFile.name}</span>
                        <button onClick={(e) => { e.stopPropagation(); setCvFile(null); }} className="text-muted-foreground hover:text-destructive">
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ) : (
                      <>
                        <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                        <p className="text-sm text-muted-foreground">Kéo thả hoặc click để chọn file</p>
                        <p className="text-xs text-muted-foreground mt-1">PDF, DOCX (tối đa 5MB)</p>
                      </>
                    )}
                  </div>
                </div>
              </motion.div>

              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1 }} className="glass-card rounded-xl p-6">
                <h2 className="font-display font-semibold text-lg text-foreground mb-4 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-accent" /> Job Description
                </h2>
                <Textarea
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
                  placeholder="Dán mô tả công việc bạn muốn ứng tuyển tại đây...&#10;&#10;VD: IT Helpdesk/Support, yêu cầu 2+ năm kinh nghiệm..."
                  rows={8}
                  className="resize-none"
                />
              </motion.div>

              <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.15 }} className="glass-card rounded-xl p-6">
                <Label className="font-display font-semibold text-lg text-foreground mb-3 flex items-center gap-2">
                  <Globe className="w-5 h-5 text-accent" /> Ngôn ngữ đầu ra
                </Label>
                <div className="flex gap-3 mt-3">
                  <Button
                    variant={language === "vi" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setLanguage("vi")}
                  >
                    🇻🇳 Tiếng Việt
                  </Button>
                  <Button
                    variant={language === "en" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setLanguage("en")}
                  >
                    🇬🇧 English
                  </Button>
                </div>
              </motion.div>

              <Button
                variant="cta"
                size="lg"
                className="w-full gap-2"
                disabled={!cvFile || !jdText.trim() || isAnalyzing}
                onClick={handleAnalyze}
              >
                <Sparkles className="w-5 h-5" />
                {isAnalyzing ? "Đang phân tích..." : "Phân tích CV"}
              </Button>
            </div>

            {/* Results Panel */}
            <div className="lg:col-span-3">
              <AnimatePresence mode="wait">
                {isAnalyzing ? (
                  <motion.div
                    key="loading"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="glass-card rounded-xl p-12 flex flex-col items-center justify-center min-h-[400px]"
                  >
                    <div className="w-16 h-16 border-4 border-accent/30 border-t-accent rounded-full animate-spin mb-6" />
                    <p className="text-muted-foreground font-medium">AI đang phân tích CV của bạn...</p>
                    <p className="text-sm text-muted-foreground mt-1">Quá trình này có thể mất 10-30 giây</p>
                  </motion.div>
                ) : results ? (
                  <motion.div key="results" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                    {/* Tabs */}
                    <div className="flex gap-2 mb-6">
                      <Button
                        variant={activeTab === "score" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setActiveTab("score")}
                        className="gap-2"
                      >
                        <BarChart3 className="w-4 h-4" /> CV Scoring
                      </Button>
                      <Button
                        variant={activeTab === "letter" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setActiveTab("letter")}
                        className="gap-2"
                      >
                        <Mail className="w-4 h-4" /> Cover Letter & Email
                      </Button>
                    </div>

                    {activeTab === "score" ? (
                      <ScoreDisplay
                        score={results.score}
                        strengths={results.strengths}
                        weaknesses={results.weaknesses}
                        tips={results.improvement_tips}
                      />
                    ) : (
                      <CoverLetterDisplay
                        emailSubject={results.email_subject}
                        emailBody={results.email_body}
                        coverLetter={results.cover_letter}
                      />
                    )}
                  </motion.div>
                ) : (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="glass-card rounded-xl p-12 flex flex-col items-center justify-center min-h-[400px] text-center"
                  >
                    <div className="w-20 h-20 bg-muted rounded-full flex items-center justify-center mb-6">
                      <Sparkles className="w-10 h-10 text-muted-foreground" />
                    </div>
                    <h3 className="font-display text-xl font-semibold text-foreground mb-2">Chưa có kết quả</h3>
                    <p className="text-muted-foreground max-w-sm">
                      Upload CV và nhập Job Description ở bên trái, sau đó nhấn "Phân tích CV" để bắt đầu.
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
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
