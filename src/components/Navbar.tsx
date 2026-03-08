import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Menu, X, Sun, Moon, Globe } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useTheme } from "@/contexts/ThemeContext";
import { useLanguage } from "@/contexts/LanguageContext";

const Navbar = () => {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const { language, setLanguage, t } = useLanguage();

  const navItems = [
    { label: t("nav.home"), path: "/" },
    { label: t("nav.solution"), path: "/solution" },
    { label: t("nav.about"), path: "/about" },
    { label: t("nav.contact"), path: "/contact" },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-card/80 backdrop-blur-lg border-b border-border/50">
      <div className="section-container flex items-center justify-between h-16">
        <Link to="/" className="font-display font-bold text-xl text-primary">
          CV<span className="text-accent">Genius</span>
        </Link>

        {/* Desktop */}
        <div className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <Link key={item.path} to={item.path}>
              <Button
                variant={location.pathname === item.path ? "secondary" : "ghost"}
                size="sm"
                className="font-medium"
              >
                {item.label}
              </Button>
            </Link>
          ))}

          {/* Language Toggle */}
          <div className="ml-2 flex items-center bg-secondary rounded-lg p-0.5">
            <button
              onClick={() => setLanguage("vi")}
              className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all duration-200 ${
                language === "vi"
                  ? "bg-card text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              🇻🇳 VI
            </button>
            <button
              onClick={() => setLanguage("en")}
              className={`px-2.5 py-1 rounded-md text-xs font-semibold transition-all duration-200 ${
                language === "en"
                  ? "bg-card text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              🇬🇧 EN
            </button>
          </div>

          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="ml-1 relative overflow-hidden"
            aria-label="Toggle theme"
          >
            <AnimatePresence mode="wait">
              {theme === "light" ? (
                <motion.div
                  key="sun"
                  initial={{ rotate: -90, scale: 0 }}
                  animate={{ rotate: 0, scale: 1 }}
                  exit={{ rotate: 90, scale: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Sun className="w-4 h-4" />
                </motion.div>
              ) : (
                <motion.div
                  key="moon"
                  initial={{ rotate: 90, scale: 0 }}
                  animate={{ rotate: 0, scale: 1 }}
                  exit={{ rotate: -90, scale: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Moon className="w-4 h-4" />
                </motion.div>
              )}
            </AnimatePresence>
          </Button>

          <Link to="/solution" className="ml-2">
            <Button variant="cta" size="sm">{t("nav.cta")}</Button>
          </Link>
        </div>

        {/* Mobile controls */}
        <div className="flex items-center gap-1 md:hidden">
          {/* Language - mobile */}
          <div className="flex items-center bg-secondary rounded-lg p-0.5">
            <button
              onClick={() => setLanguage("vi")}
              className={`px-2 py-1 rounded-md text-xs font-semibold transition-all ${
                language === "vi" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground"
              }`}
            >
              VI
            </button>
            <button
              onClick={() => setLanguage("en")}
              className={`px-2 py-1 rounded-md text-xs font-semibold transition-all ${
                language === "en" ? "bg-card text-foreground shadow-sm" : "text-muted-foreground"
              }`}
            >
              EN
            </button>
          </div>

          <Button variant="ghost" size="icon" onClick={toggleTheme}>
            {theme === "light" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </Button>

          <Button variant="ghost" size="icon" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X /> : <Menu />}
          </Button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-card border-b border-border"
          >
            <div className="section-container py-4 flex flex-col gap-2">
              {navItems.map((item) => (
                <Link key={item.path} to={item.path} onClick={() => setMobileOpen(false)}>
                  <Button
                    variant={location.pathname === item.path ? "secondary" : "ghost"}
                    className="w-full justify-start"
                  >
                    {item.label}
                  </Button>
                </Link>
              ))}
              <Link to="/solution" onClick={() => setMobileOpen(false)}>
                <Button variant="cta" className="w-full mt-2">{t("nav.cta")}</Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;
