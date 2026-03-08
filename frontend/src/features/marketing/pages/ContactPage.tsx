import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { motion } from "framer-motion";
import { Mail, MapPin, Send } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { useLanguage } from "@/contexts/LanguageContext";

const ContactPage = () => {
  const [loading, setLoading] = useState(false);
  const { t } = useLanguage();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      toast.success(t("contact.success"));
      (e.target as HTMLFormElement).reset();
    }, 1000);
  };

  return (
    <div className="min-h-screen flex flex-col relative z-10">
      <Navbar />

      <section className="pt-28 pb-16 bg-muted/30">
        <div className="section-container text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-4">{t("contact.title")}</h1>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto">{t("contact.desc")}</p>
          </motion.div>
        </div>
      </section>

      <section className="py-16 bg-background flex-1">
        <div className="section-container">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-4xl mx-auto">
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1 }}>
              <h2 className="font-display text-2xl font-bold text-foreground mb-6">{t("contact.send.title")}</h2>
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <Label htmlFor="name">{t("contact.name")}</Label>
                  <Input id="name" placeholder="Nguyễn Văn A" required className="mt-1.5" />
                </div>
                <div>
                  <Label htmlFor="email">{t("contact.email")}</Label>
                  <Input id="email" type="email" placeholder="email@example.com" required className="mt-1.5" />
                </div>
                <div>
                  <Label htmlFor="message">{t("contact.message")}</Label>
                  <Textarea id="message" placeholder={t("contact.message.placeholder")} rows={5} required className="mt-1.5" />
                </div>
                <Button type="submit" variant="cta" size="lg" className="gap-2" disabled={loading}>
                  <Send className="w-4 h-4" /> {loading ? t("contact.sending") : t("contact.submit")}
                </Button>
              </form>
            </motion.div>

            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
              <h2 className="font-display text-2xl font-bold text-foreground mb-6">{t("contact.support")}</h2>
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-accent/10 rounded-lg flex items-center justify-center shrink-0">
                    <Mail className="w-5 h-5 text-accent" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">{t("contact.email")}</h3>
                    <p className="text-muted-foreground">support@cvgenius.vn</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 bg-accent/10 rounded-lg flex items-center justify-center shrink-0">
                    <MapPin className="w-5 h-5 text-accent" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">{t("contact.address")}</h3>
                    <p className="text-muted-foreground">TP. Hồ Chí Minh, Việt Nam</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default ContactPage;
