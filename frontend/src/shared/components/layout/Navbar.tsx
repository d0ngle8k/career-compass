import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Menu, X, LogIn, LogOut, User, ChevronDown, BarChart3, Mail, FileText } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";

const Navbar = () => {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [solutionOpen, setSolutionOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();
  const { user, signOut } = useAuth();

  const solutionItems = [
    { label: t("nav.cv.analysis"), path: "/solution", icon: BarChart3 },
    { label: t("nav.write.mail"), path: "/write-mail", icon: Mail },
    { label: t("nav.write.cover"), path: "/write-cover-letter", icon: FileText },
  ];

  const isSolutionActive = ["/solution", "/write-mail", "/write-cover-letter"].includes(location.pathname);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-card/80 backdrop-blur-lg border-b border-border/50">
      <div className="section-container flex items-center justify-between h-16">
        <Link to="/" className="font-display font-bold text-xl text-primary">
          CV<span className="text-accent">Genius</span>
        </Link>

        {/* Desktop */}
        <div className="hidden md:flex items-center gap-1">
          <Link to="/">
            <Button variant={location.pathname === "/" ? "secondary" : "ghost"} size="sm" className="font-medium">
              {t("nav.home")}
            </Button>
          </Link>

          {/* Solution dropdown */}
          <div className="relative" onMouseEnter={() => setSolutionOpen(true)} onMouseLeave={() => setSolutionOpen(false)}>
            <Button variant={isSolutionActive ? "secondary" : "ghost"} size="sm" className="font-medium gap-1">
              {t("nav.solution")} <ChevronDown className={`w-3.5 h-3.5 transition-transform ${solutionOpen ? "rotate-180" : ""}`} />
            </Button>
            <AnimatePresence>
              {solutionOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  transition={{ duration: 0.15 }}
                  className="absolute top-full left-0 mt-1 w-56 bg-card border border-border rounded-xl shadow-lg overflow-hidden z-50"
                >
                  {solutionItems.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Link key={item.path} to={item.path} onClick={() => setSolutionOpen(false)}>
                        <div className={`flex items-center gap-3 px-4 py-3 text-sm transition-colors hover:bg-muted ${location.pathname === item.path ? "bg-muted text-foreground font-medium" : "text-muted-foreground"}`}>
                          <Icon className="w-4 h-4 text-accent" />
                          {item.label}
                        </div>
                      </Link>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <Link to="/about">
            <Button variant={location.pathname === "/about" ? "secondary" : "ghost"} size="sm" className="font-medium">
              {t("nav.about")}
            </Button>
          </Link>
          <Link to="/contact">
            <Button variant={location.pathname === "/contact" ? "secondary" : "ghost"} size="sm" className="font-medium">
              {t("nav.contact")}
            </Button>
          </Link>

          {/* Language Toggle */}
          <div className="ml-2 flex items-center bg-secondary rounded-lg p-0.5">
            <button onClick={() => setLanguage("vi")} className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all duration-200 ${language === "vi" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"}`}>🇻🇳 VI</button>
            <button onClick={() => setLanguage("en")} className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all duration-200 ${language === "en" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"}`}>🇬🇧 EN</button>
          </div>

          {/* Auth */}
          {user ? (
            <div className="ml-2 flex items-center gap-2">
              <span className="text-sm text-muted-foreground flex items-center gap-1">
                <User className="w-4 h-4" /> {user.email?.split("@")[0]}
              </span>
              <Button variant="ghost" size="sm" onClick={signOut} className="gap-1"><LogOut className="w-4 h-4" /></Button>
            </div>
          ) : (
            <Link to="/auth" className="ml-2">
              <Button variant="cta" size="sm" className="gap-1"><LogIn className="w-4 h-4" /> {t("nav.login")}</Button>
            </Link>
          )}
        </div>

        {/* Mobile controls */}
        <div className="flex items-center gap-1 md:hidden">
          <div className="flex items-center bg-secondary rounded-lg p-0.5">
            <button onClick={() => setLanguage("vi")} className={`px-2 py-1 rounded-md text-xs font-semibold transition-all ${language === "vi" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground"}`}>VI</button>
            <button onClick={() => setLanguage("en")} className={`px-2 py-1 rounded-md text-xs font-semibold transition-all ${language === "en" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground"}`}>EN</button>
          </div>
          <Button variant="ghost" size="icon" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X /> : <Menu />}
          </Button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="md:hidden bg-card border-b border-border">
            <div className="section-container py-4 flex flex-col gap-2">
              <Link to="/" onClick={() => setMobileOpen(false)}>
                <Button variant={location.pathname === "/" ? "secondary" : "ghost"} className="w-full justify-start">{t("nav.home")}</Button>
              </Link>
              {/* Solution sub-items */}
              <div className="pl-2 space-y-1">
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider px-3 py-1">{t("nav.solution")}</p>
                {solutionItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <Link key={item.path} to={item.path} onClick={() => setMobileOpen(false)}>
                      <Button variant={location.pathname === item.path ? "secondary" : "ghost"} className="w-full justify-start gap-2">
                        <Icon className="w-4 h-4" /> {item.label}
                      </Button>
                    </Link>
                  );
                })}
              </div>
              <Link to="/about" onClick={() => setMobileOpen(false)}>
                <Button variant={location.pathname === "/about" ? "secondary" : "ghost"} className="w-full justify-start">{t("nav.about")}</Button>
              </Link>
              <Link to="/contact" onClick={() => setMobileOpen(false)}>
                <Button variant={location.pathname === "/contact" ? "secondary" : "ghost"} className="w-full justify-start">{t("nav.contact")}</Button>
              </Link>
              {user ? (
                <Button variant="outline" className="w-full mt-2 gap-2" onClick={() => { signOut(); setMobileOpen(false); }}>
                  <LogOut className="w-4 h-4" /> {t("nav.logout")}
                </Button>
              ) : (
                <Link to="/auth" onClick={() => setMobileOpen(false)}>
                  <Button variant="cta" className="w-full mt-2 gap-1"><LogIn className="w-4 h-4" /> {t("nav.login")}</Button>
                </Link>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;
