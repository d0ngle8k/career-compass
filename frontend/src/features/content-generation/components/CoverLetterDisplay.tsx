import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Copy, Check, Mail, FileText } from "lucide-react";
import { toast } from "sonner";
import { useLanguage } from "@/contexts/LanguageContext";
import ReactMarkdown from "react-markdown";

interface CoverLetterDisplayProps {
  emailSubject: string;
  emailBody: string;
  coverLetter: string;
}

const CoverLetterDisplay = ({ emailSubject, emailBody, coverLetter }: CoverLetterDisplayProps) => {
  const { t } = useLanguage();
  const [copiedField, setCopiedField] = useState<string | null>(null);

  const copyToClipboard = (text: string, field: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(field);
    toast.success(t("letter.copied"));
    setTimeout(() => setCopiedField(null), 2000);
  };

  const CopyBtn = ({ text, field }: { text: string; field: string }) => (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => copyToClipboard(text, field)}
      className="gap-1.5"
    >
      {copiedField === field ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
      {copiedField === field ? t("letter.copied") : t("letter.copy")}
    </Button>
  );

  return (
    <div className="space-y-6">
      {/* Email */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-semibold text-foreground flex items-center gap-2">
            <Mail className="w-5 h-5 text-cta" /> {t("letter.email")}
          </h3>
          <CopyBtn text={`Subject: ${emailSubject}\n\n${emailBody}`} field="email" />
        </div>
        <div className="bg-muted/50 rounded-lg p-4 space-y-3">
          <div>
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">{t("letter.subject")}</span>
            <p className="text-sm text-foreground font-medium mt-1">{emailSubject}</p>
          </div>
          <div className="border-t border-border pt-3">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">{t("letter.body")}</span>
            <div className="text-sm text-foreground mt-1 leading-relaxed prose prose-sm max-w-none">
              <ReactMarkdown>{emailBody}</ReactMarkdown>
            </div>
          </div>
        </div>
      </div>

      {/* Cover Letter */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-semibold text-foreground flex items-center gap-2">
            <FileText className="w-5 h-5 text-accent" /> {t("letter.cover")}
          </h3>
          <CopyBtn text={coverLetter} field="cover" />
        </div>
        <div className="bg-muted/50 rounded-lg p-4">
          <div className="text-sm text-foreground leading-relaxed prose prose-sm max-w-none">
            <ReactMarkdown>{coverLetter}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoverLetterDisplay;
