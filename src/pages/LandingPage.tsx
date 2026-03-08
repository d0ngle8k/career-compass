import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { BarChart3, Mail, MessageCircle, ArrowRight } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useLanguage } from "@/contexts/LanguageContext";

const LandingPage = () => {
  const { t } = useLanguage();

  const features = [
    {
      icon: BarChart3,
      title: t("features.scoring.title"),
      desc: t("features.scoring.desc"),
      color: "text-accent",
      bg: "bg-accent/10",
    },
    {
      icon: Mail,
      title: t("features.letter.title"),
      desc: t("features.letter.desc"),
      color: "text-cta",
      bg: "bg-cta/10",
    },
    {
      icon: MessageCircle,
      title: t("features.chatbot.title"),
      desc: t("features.chatbot.desc"),
      color: "text-primary",
      bg: "bg-primary/10",
    },
  ];

  const steps = [
    { num: "01", title: t("howit.step1.title"), desc: t("howit.step1.desc") },
    { num: "02", title: t("howit.step2.title"), desc: t("howit.step2.desc") },
    { num: "03", title: t("howit.step3.title"), desc: t("howit.step3.desc") },
  ];

  return (
    <div className="min-h-screen flex flex-col relative z-10">
      <Navbar />

      {/* Hero */}
      <section className="gradient-hero pt-28 pb-20 lg:pt-36 lg:pb-28 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-accent/30 rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-20 w-96 h-96 bg-cta/20 rounded-full blur-3xl" />
        </div>
        <div className="section-container relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <span className="inline-block px-4 py-1.5 rounded-full bg-accent/20 text-accent text-sm font-medium mb-6">
                {t("hero.badge")}
              </span>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-primary-foreground leading-tight mb-6">
                {t("hero.title1")}{" "}
                <span className="text-accent">{t("hero.title2")}</span>
              </h1>
              <p className="text-lg md:text-xl text-primary-foreground/80 mb-8 leading-relaxed max-w-2xl mx-auto">
                {t("hero.desc")}
              </p>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.2 }} className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/solution">
                <Button variant="cta" size="xl" className="gap-2">
                  {t("hero.cta")} <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
              <Link to="/about">
                <Button variant="hero-outline" size="xl" className="border-primary-foreground/30 text-primary-foreground hover:bg-primary-foreground/10">
                  {t("hero.learn")}
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
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">{t("features.title")}</h2>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto">{t("features.desc")}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div key={f.title} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.1 }} className="glass-card rounded-xl p-8 hover:shadow-elevated transition-shadow duration-300">
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
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">{t("howit.title")}</h2>
            <p className="text-muted-foreground text-lg">{t("howit.desc")}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((s, i) => (
              <motion.div key={s.num} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.15 }} className="text-center">
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
              <h2 className="font-display text-3xl md:text-4xl font-bold text-primary-foreground mb-4">{t("cta.title")}</h2>
              <p className="text-primary-foreground/80 text-lg mb-8 max-w-lg mx-auto">{t("cta.desc")}</p>
              <Link to="/solution">
                <Button variant="cta" size="xl" className="gap-2">
                  {t("cta.button")} <ArrowRight className="w-5 h-5" />
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
