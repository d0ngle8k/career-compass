import { useEffect, useRef } from "react";
import { useTheme } from "@/contexts/ThemeContext";
import { motion, AnimatePresence } from "framer-motion";

interface Star {
  x: number;
  y: number;
  size: number;
  opacity: number;
  twinkleSpeed: number;
  twinklePhase: number;
}

interface ShootingStar {
  x: number;
  y: number;
  length: number;
  speed: number;
  angle: number;
  opacity: number;
  life: number;
  maxLife: number;
}

const StarryBackground = () => {
  const { theme } = useTheme();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const starsRef = useRef<Star[]>([]);
  const shootingStarsRef = useRef<ShootingStar[]>([]);
  const animRef = useRef<number>(0);

  useEffect(() => {
    if (theme !== "dark") {
      cancelAnimationFrame(animRef.current);
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Generate stars
    starsRef.current = Array.from({ length: 150 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random(),
      twinkleSpeed: Math.random() * 0.02 + 0.005,
      twinklePhase: Math.random() * Math.PI * 2,
    }));

    const spawnShootingStar = () => {
      if (shootingStarsRef.current.length >= 3) return;
      const side = Math.random();
      let x: number, y: number, angle: number;
      if (side < 0.5) {
        x = Math.random() * canvas.width;
        y = -10;
        angle = Math.PI / 4 + Math.random() * (Math.PI / 4);
      } else {
        x = canvas.width + 10;
        y = Math.random() * canvas.height * 0.5;
        angle = Math.PI * 0.6 + Math.random() * 0.4;
      }
      shootingStarsRef.current.push({
        x, y, angle,
        length: 60 + Math.random() * 80,
        speed: 6 + Math.random() * 8,
        opacity: 1,
        life: 0,
        maxLife: 80 + Math.random() * 60,
      });
    };

    let frame = 0;
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      frame++;

      // Draw stars with twinkling
      starsRef.current.forEach((star) => {
        star.twinklePhase += star.twinkleSpeed;
        const flicker = Math.sin(star.twinklePhase) * 0.5 + 0.5;
        const alpha = star.opacity * flicker;

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200, 220, 255, ${alpha})`;
        ctx.fill();

        // Glow effect for brighter stars
        if (star.size > 1.2) {
          ctx.beginPath();
          ctx.arc(star.x, star.y, star.size * 3, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(180, 200, 255, ${alpha * 0.1})`;
          ctx.fill();
        }
      });

      // Spawn shooting stars periodically
      if (frame % 90 === 0 && Math.random() < 0.6) {
        spawnShootingStar();
      }

      // Draw shooting stars
      shootingStarsRef.current = shootingStarsRef.current.filter((ss) => {
        ss.life++;
        ss.x += Math.cos(ss.angle) * ss.speed;
        ss.y += Math.sin(ss.angle) * ss.speed;

        const fadeIn = Math.min(ss.life / 10, 1);
        const fadeOut = Math.max(1 - (ss.life - ss.maxLife * 0.7) / (ss.maxLife * 0.3), 0);
        ss.opacity = fadeIn * fadeOut;

        if (ss.opacity <= 0) return false;

        const tailX = ss.x - Math.cos(ss.angle) * ss.length;
        const tailY = ss.y - Math.sin(ss.angle) * ss.length;

        const gradient = ctx.createLinearGradient(ss.x, ss.y, tailX, tailY);
        gradient.addColorStop(0, `rgba(255, 255, 255, ${ss.opacity})`);
        gradient.addColorStop(0.3, `rgba(180, 200, 255, ${ss.opacity * 0.6})`);
        gradient.addColorStop(1, `rgba(100, 150, 255, 0)`);

        ctx.beginPath();
        ctx.moveTo(ss.x, ss.y);
        ctx.lineTo(tailX, tailY);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 2;
        ctx.stroke();

        // Head glow
        ctx.beginPath();
        ctx.arc(ss.x, ss.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${ss.opacity * 0.8})`;
        ctx.fill();

        return ss.life < ss.maxLife;
      });

      animRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      cancelAnimationFrame(animRef.current);
      window.removeEventListener("resize", resize);
    };
  }, [theme]);

  return (
    <AnimatePresence>
      {theme === "dark" && (
        <motion.canvas
          ref={canvasRef}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.8 }}
          className="fixed inset-0 z-0 pointer-events-none"
          style={{ background: "transparent" }}
        />
      )}
    </AnimatePresence>
  );
};

export default StarryBackground;
