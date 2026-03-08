import { Link } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";

const Footer = () => {
  const { t } = useLanguage();

  return (
    <footer className="bg-primary text-primary-foreground py-12 relative z-10">
      <div className="section-container">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="font-display font-bold text-xl mb-3">
              CV<span className="text-accent">Genius</span>
            </h3>
            <p className="text-primary-foreground/70 text-sm leading-relaxed">{t("footer.desc")}</p>
          </div>
          <div>
            <h4 className="font-display font-semibold mb-3">{t("footer.nav")}</h4>
            <div className="flex flex-col gap-2 text-sm text-primary-foreground/70">
              <Link to="/" className="hover:text-primary-foreground transition-colors">{t("nav.home")}</Link>
              <Link to="/solution" className="hover:text-primary-foreground transition-colors">{t("nav.solution")}</Link>
              <Link to="/about" className="hover:text-primary-foreground transition-colors">{t("nav.about")}</Link>
              <Link to="/contact" className="hover:text-primary-foreground transition-colors">{t("nav.contact")}</Link>
            </div>
          </div>
          <div>
            <h4 className="font-display font-semibold mb-3">{t("footer.contact")}</h4>
            <div className="flex flex-col gap-2 text-sm text-primary-foreground/70">
              <span>support@cvgenius.vn</span>
              <span>TP. Hồ Chí Minh, Việt Nam</span>
            </div>
          </div>
        </div>
        <div className="border-t border-primary-foreground/20 mt-8 pt-6 text-center text-sm text-primary-foreground/50">
          © 2026 CVGenius. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
