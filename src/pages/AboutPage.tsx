import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Target, Users, Lightbulb } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

const team = [
  { name: "Trương Gia Thành", role: "Project Lead", avatar: "TT" },
  { name: "Đoàn Văn Khoan", role: "Backend Developer", avatar: "DK" },
  { name: "Nguyễn Hoàng Anh Kha", role: "UX/UI Designer", avatar: "NK" },
];

const AboutPage = () => {
  const { t } = useLanguage();

  const values = [
    { icon: Target, title: t("about.mission.title"), desc: t("about.mission.desc") },
    { icon: Users, title: t("about.team.title"), desc: t("about.team.desc") },
    { icon: Lightbulb, title: t("about.vision.title"), desc: t("about.vision.desc") },
  ];

  return (
    <div className="min-h-screen flex flex-col relative z-10">
      <Navbar />

      <section className="pt-28 pb-16 bg-muted/30">
        <div className="section-container text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-4">{t("about.title")}</h1>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">{t("about.desc")}</p>
          </motion.div>
        </div>
      </section>

      <section className="py-16 bg-background">
        <div className="section-container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {values.map((v, i) => (
              <motion.div key={v.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }} className="glass-card rounded-xl p-8 text-center">
                <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <v.icon className="w-6 h-6 text-accent" />
                </div>
                <h3 className="font-display font-semibold text-xl mb-2 text-foreground">{v.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{v.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-muted/30">
        <div className="section-container">
          <h2 className="font-display text-3xl font-bold text-foreground text-center mb-10">{t("about.devteam")}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto">
            {team.map((m, i) => (
              <motion.div key={m.name} initial={{ opacity: 0, scale: 0.9 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }} className="glass-card rounded-xl p-6 text-center">
                <div className="w-16 h-16 rounded-full bg-primary flex items-center justify-center mx-auto mb-4">
                  <span className="text-primary-foreground font-display font-bold text-lg">{m.avatar}</span>
                </div>
                <h3 className="font-display font-semibold text-foreground">{m.name}</h3>
                <p className="text-sm text-muted-foreground mt-1">{m.role}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default AboutPage;
