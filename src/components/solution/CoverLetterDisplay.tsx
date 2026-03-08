import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Copy, Check, Mail, FileText } from "lucide-react";
import { toast } from "sonner";

interface CoverLetterDisplayProps {
  emailSubject: string;
  emailBody: string;
  coverLetter: string;
}

const CoverLetterDisplay = ({ emailSubject, emailBody, coverLetter }: CoverLetterDisplayProps) => {
  const [copiedField, setCopiedField] = useState<string | null>(null);

  const copyToClipboard = (text: string, field: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(field);
    toast.success("Đã sao chép!");
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
      {copiedField === field ? "Đã sao chép" : "Sao chép"}
    </Button>
  );

  return (
    <div className="space-y-6">
      {/* Email */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-semibold text-foreground flex items-center gap-2">
            <Mail className="w-5 h-5 text-cta" /> Email ứng tuyển
          </h3>
          <CopyBtn text={`Subject: ${emailSubject}\n\n${emailBody}`} field="email" />
        </div>
        <div className="bg-muted/50 rounded-lg p-4 space-y-3">
          <div>
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Tiêu đề</span>
            <p className="text-sm text-foreground font-medium mt-1">{emailSubject}</p>
          </div>
          <div className="border-t border-border pt-3">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Nội dung</span>
            <p className="text-sm text-foreground mt-1 whitespace-pre-line leading-relaxed">{emailBody}</p>
          </div>
        </div>
      </div>

      {/* Cover Letter */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-display font-semibold text-foreground flex items-center gap-2">
            <FileText className="w-5 h-5 text-accent" /> Cover Letter
          </h3>
          <CopyBtn text={coverLetter} field="cover" />
        </div>
        <div className="bg-muted/50 rounded-lg p-4">
          <p className="text-sm text-foreground whitespace-pre-line leading-relaxed">{coverLetter}</p>
        </div>
      </div>
    </div>
  );
};

export default CoverLetterDisplay;
