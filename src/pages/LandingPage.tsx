import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { FileText, BarChart3, Mail, MessageCircle, ArrowRight, CheckCircle } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const features = [
  {
    icon: BarChart3,
    title: "CV Scoring",
    desc: "Chấm điểm CV (0-100) dựa trên JD. Phân tích điểm mạnh, điểm yếu và đưa ra lời khuyên cải thiện.",
    color: "text-accent",
    bg: "bg-accent/10",
  },
  {
    icon: Mail,
    title: "Cover Letter & Email",
    desc: "Tự động sinh thư xin việc và email ứng tuyển chuyên nghiệp dựa trên CV và JD của bạn.",
    color: "text-cta",
    bg: "bg-cta/10",
  },
  {
    icon: MessageCircle,
    title: "AI Chatbot Assistant",
    desc: "Trợ lý AI giúp viết lại bullet point kinh nghiệm, thêm action verbs và định lượng kết quả.",
    color: "text-primary",
    bg: "bg-primary/10",
  },
];

const steps = [
  { num: "01", title: "Upload CV", desc: "Tải lên file PDF hoặc DOCX" },
  { num: "02", title: "Nhập Job Description", desc: "Dán mô tả công việc bạn muốn ứng tuyển" },
  { num: "03", title: "Nhận phân tích AI", desc: "Điểm số, cover letter và lời khuyên tức thì" },
];

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      {/* Hero */}
      <section className="gradient-hero pt-28 pb-20 lg:pt-36 lg:pb-28 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-accent/30 rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-20 w-96 h-96 bg-cta/20 rounded-full blur-3xl" />
        </div>
        <div className="section-container relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <span className="inline-block px-4 py-1.5 rounded-full bg-accent/20 text-accent text-sm font-medium mb-6">
                Powered by Gemini AI
              </span>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-primary-foreground leading-tight mb-6">
                Tối ưu CV của bạn với{" "}
                <span className="text-accent">trí tuệ nhân tạo</span>
              </h1>
              <p className="text-lg md:text-xl text-primary-foreground/80 mb-8 leading-relaxed max-w-2xl mx-auto">
                Chấm điểm CV, sinh Cover Letter và nhận lời khuyên cải thiện chỉ trong vài giây. Giúp bạn nổi bật trong mắt nhà tuyển dụng.
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link to="/solution">
                <Button variant="cta" size="xl" className="gap-2">
                  Bắt đầu phân tích <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
              <Link to="/about">
                <Button variant="hero-outline" size="xl" className="border-primary-foreground/30 text-primary-foreground hover:bg-primary-foreground/10">
                  Tìm hiểu thêm
                </Button>
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-background">
        <div className="section-container">
          <div className="text-center mb-14">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
              Tính năng nổi bật
            </h2>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto">
              Ba công cụ mạnh mẽ giúp bạn sẵn sàng cho mọi cơ hội nghề nghiệp
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="glass-card rounded-xl p-8 hover:shadow-elevated transition-shadow duration-300"
              >
                <div className={`w-12 h-12 ${f.bg} rounded-lg flex items-center justify-center mb-5`}>
                  <f.icon className={`w-6 h-6 ${f.color}`} />
                </div>
                <h3 className="font-display font-semibold text-xl mb-3 text-foreground">{f.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 bg-muted/50">
        <div className="section-container">
          <div className="text-center mb-14">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
              Cách hoạt động
            </h2>
            <p className="text-muted-foreground text-lg">Chỉ 3 bước đơn giản</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((s, i) => (
              <motion.div
                key={s.num}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
                className="text-center"
              >
                <div className="text-5xl font-display font-bold text-accent/20 mb-4">{s.num}</div>
                <h3 className="font-display font-semibold text-xl mb-2 text-foreground">{s.title}</h3>
                <p className="text-muted-foreground">{s.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-background">
        <div className="section-container">
          <div className="gradient-hero rounded-2xl p-10 md:p-16 text-center relative overflow-hidden">
            <div className="absolute inset-0 opacity-10">
              <div className="absolute top-0 right-0 w-64 h-64 bg-accent/30 rounded-full blur-3xl" />
            </div>
            <div className="relative z-10">
              <h2 className="font-display text-3xl md:text-4xl font-bold text-primary-foreground mb-4">
                Sẵn sàng nâng cấp CV?
              </h2>
              <p className="text-primary-foreground/80 text-lg mb-8 max-w-lg mx-auto">
                Hàng nghìn ứng viên đã cải thiện hồ sơ của họ. Đến lượt bạn.
              </p>
              <Link to="/solution">
                <Button variant="cta" size="xl" className="gap-2">
                  Phân tích CV miễn phí <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;
