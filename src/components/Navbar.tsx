import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const navItems = [
  { label: "Trang chủ", path: "/" },
  { label: "Giải pháp", path: "/solution" },
  { label: "Về chúng tôi", path: "/about" },
  { label: "Liên hệ", path: "/contact" },
];

const Navbar = () => {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

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
          <Link to="/solution" className="ml-3">
            <Button variant="cta" size="sm">Bắt đầu ngay</Button>
          </Link>
        </div>

        {/* Mobile toggle */}
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X /> : <Menu />}
        </Button>
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
                <Button variant="cta" className="w-full mt-2">Bắt đầu ngay</Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;
