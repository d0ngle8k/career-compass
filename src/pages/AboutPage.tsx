import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Target, Users, Lightbulb } from "lucide-react";

const team = [
  { name: "Nguyễn Văn A", role: "Project Lead / AI Engineer", avatar: "NA" },
  { name: "Trần Thị B", role: "Frontend Developer", avatar: "TB" },
  { name: "Lê Văn C", role: "Backend Developer", avatar: "LC" },
  { name: "Phạm Thị D", role: "UX Designer", avatar: "PD" },
];

const values = [
  { icon: Target, title: "Sứ mệnh", desc: "Giúp mọi ứng viên Việt Nam tự tin hơn trong hành trình tìm việc bằng công nghệ AI tiên tiến." },
  { icon: Users, title: "Đội ngũ", desc: "Nhóm sinh viên đam mê công nghệ, cam kết mang lại giải pháp thực tiễn cho người tìm việc." },
  { icon: Lightbulb, title: "Tầm nhìn", desc: "Trở thành công cụ hỗ trợ nghề nghiệp #1 tại Đông Nam Á, ứng dụng AI vào tuyển dụng." },
];

const AboutPage = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <section className="pt-28 pb-16 bg-muted/30">
        <div className="section-container text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-4">Về chúng tôi</h1>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              CVGenius là dự án ứng dụng AI vào phân tích và tối ưu CV, được phát triển bởi nhóm sinh viên đầy nhiệt huyết.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16 bg-background">
        <div className="section-container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {values.map((v, i) => (
              <motion.div
                key={v.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass-card rounded-xl p-8 text-center"
              >
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
          <h2 className="font-display text-3xl font-bold text-foreground text-center mb-10">Đội ngũ phát triển</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {team.map((m, i) => (
              <motion.div
                key={m.name}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass-card rounded-xl p-6 text-center"
              >
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
