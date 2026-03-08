import { motion } from "framer-motion";
import { CheckCircle, AlertTriangle, Lightbulb } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

interface ScoreDisplayProps {
  score: number;
  strengths: string[];
  weaknesses: string[];
  tips: string[];
}

const ScoreDisplay = ({ score, strengths, weaknesses, tips }: ScoreDisplayProps) => {
  const { t } = useLanguage();
  const scoreColor = score >= 80 ? "text-score-high" : score >= 60 ? "text-score-mid" : "text-score-low";
  const scoreRingColor = score >= 80 ? "stroke-score-high" : score >= 60 ? "stroke-score-mid" : "stroke-score-low";
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="space-y-6">
      {/* Score Ring */}
      <div className="glass-card rounded-xl p-8 flex flex-col items-center">
        <div className="relative w-36 h-36">
          <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="54" fill="none" strokeWidth="8" className="stroke-muted" />
            <motion.circle
              cx="60" cy="60" r="54" fill="none" strokeWidth="8"
              strokeLinecap="round"
              className={scoreRingColor}
              strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ duration: 1.5, ease: "easeOut" }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <motion.span
              className={`text-4xl font-display font-bold ${scoreColor}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              {score}
            </motion.span>
            <span className="text-xs text-muted-foreground">/ 100</span>
          </div>
        </div>
        <p className="text-muted-foreground mt-3 font-medium">{t("score.match")}</p>
      </div>

      {/* Strengths */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="font-display font-semibold text-foreground mb-4 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-success" /> {t("score.strengths")}
        </h3>
        <ul className="space-y-3">
          {strengths.map((s, i) => (
            <motion.li
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + i * 0.1 }}
              className="flex items-start gap-3 text-sm text-foreground"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-success mt-1.5 shrink-0" />
              {s}
            </motion.li>
          ))}
        </ul>
      </div>

      {/* Weaknesses */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="font-display font-semibold text-foreground mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-score-mid" /> {t("score.weaknesses")}
        </h3>
        <ul className="space-y-3">
          {weaknesses.map((w, i) => (
            <motion.li
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + i * 0.1 }}
              className="flex items-start gap-3 text-sm text-foreground"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-score-mid mt-1.5 shrink-0" />
              {w}
            </motion.li>
          ))}
        </ul>
      </div>

      {/* Tips */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="font-display font-semibold text-foreground mb-4 flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-accent" /> {t("score.tips")}
        </h3>
        <ul className="space-y-3">
          {tips.map((tip, i) => (
            <motion.li
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 + i * 0.1 }}
              className="flex items-start gap-3 text-sm text-foreground"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-accent mt-1.5 shrink-0" />
              {tip}
            </motion.li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ScoreDisplay;
