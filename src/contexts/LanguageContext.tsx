import { createContext, useContext, useState, ReactNode } from "react";

type Language = "vi" | "en";

interface Translations {
  [key: string]: { vi: string; en: string };
}

const translations: Translations = {
  "nav.home": { vi: "Trang chủ", en: "Home" },
  "nav.solution": { vi: "Giải pháp", en: "Solution" },
  "nav.about": { vi: "Về chúng tôi", en: "About Us" },
  "nav.contact": { vi: "Liên hệ", en: "Contact" },
  "nav.cta": { vi: "Bắt đầu ngay", en: "Get Started" },
  "hero.badge": { vi: "Powered by Gemini AI", en: "Powered by Gemini AI" },
  "hero.title1": { vi: "Tối ưu CV của bạn với", en: "Optimize your CV with" },
  "hero.title2": { vi: "trí tuệ nhân tạo", en: "artificial intelligence" },
  "hero.desc": {
    vi: "Chấm điểm CV, sinh Cover Letter và nhận lời khuyên cải thiện chỉ trong vài giây. Giúp bạn nổi bật trong mắt nhà tuyển dụng.",
    en: "Score your CV, generate Cover Letters and get improvement tips in seconds. Stand out to recruiters.",
  },
  "hero.cta": { vi: "Bắt đầu phân tích", en: "Start Analysis" },
  "hero.learn": { vi: "Tìm hiểu thêm", en: "Learn More" },
  "features.title": { vi: "Tính năng nổi bật", en: "Key Features" },
  "features.desc": {
    vi: "Ba công cụ mạnh mẽ giúp bạn sẵn sàng cho mọi cơ hội nghề nghiệp",
    en: "Three powerful tools to prepare you for every career opportunity",
  },
  "features.scoring.title": { vi: "CV Scoring", en: "CV Scoring" },
  "features.scoring.desc": {
    vi: "Chấm điểm CV (0-100) dựa trên JD. Phân tích điểm mạnh, điểm yếu và đưa ra lời khuyên cải thiện.",
    en: "Score your CV (0-100) based on JD. Analyze strengths, weaknesses and provide improvement tips.",
  },
  "features.letter.title": { vi: "Cover Letter & Email", en: "Cover Letter & Email" },
  "features.letter.desc": {
    vi: "Tự động sinh thư xin việc và email ứng tuyển chuyên nghiệp dựa trên CV và JD của bạn.",
    en: "Auto-generate professional cover letters and application emails based on your CV and JD.",
  },
  "features.chatbot.title": { vi: "AI Chatbot Assistant", en: "AI Chatbot Assistant" },
  "features.chatbot.desc": {
    vi: "Trợ lý AI giúp viết lại bullet point kinh nghiệm, thêm action verbs và định lượng kết quả.",
    en: "AI assistant to rewrite experience bullet points, add action verbs and quantify results.",
  },
  "howit.title": { vi: "Cách hoạt động", en: "How It Works" },
  "howit.desc": { vi: "Chỉ 3 bước đơn giản", en: "Just 3 simple steps" },
  "howit.step1.title": { vi: "Upload CV", en: "Upload CV" },
  "howit.step1.desc": { vi: "Tải lên file PDF hoặc DOCX", en: "Upload PDF or DOCX file" },
  "howit.step2.title": { vi: "Nhập Job Description", en: "Enter Job Description" },
  "howit.step2.desc": { vi: "Dán mô tả công việc bạn muốn ứng tuyển", en: "Paste the job description you're applying for" },
  "howit.step3.title": { vi: "Nhận phân tích AI", en: "Get AI Analysis" },
  "howit.step3.desc": { vi: "Điểm số, cover letter và lời khuyên tức thì", en: "Scores, cover letter and instant tips" },
  "cta.title": { vi: "Sẵn sàng nâng cấp CV?", en: "Ready to upgrade your CV?" },
  "cta.desc": {
    vi: "Hàng nghìn ứng viên đã cải thiện hồ sơ của họ. Đến lượt bạn.",
    en: "Thousands of candidates have improved their profiles. It's your turn.",
  },
  "cta.button": { vi: "Phân tích CV miễn phí", en: "Analyze CV for Free" },
  "footer.desc": {
    vi: "Nền tảng phân tích CV thông minh, giúp bạn tối ưu hồ sơ ứng tuyển với sức mạnh AI.",
    en: "Smart CV analysis platform, helping you optimize your application with AI power.",
  },
  "footer.nav": { vi: "Điều hướng", en: "Navigation" },
  "footer.contact": { vi: "Liên hệ", en: "Contact" },
  // Solution page
  "solution.title": { vi: "Phân tích CV thông minh", en: "Smart CV Analysis" },
  "solution.desc": { vi: "Upload CV và nhập JD để bắt đầu", en: "Upload CV and enter JD to start" },
  "solution.upload": { vi: "Upload CV", en: "Upload CV" },
  "solution.drag": { vi: "Kéo thả hoặc click để chọn file", en: "Drag & drop or click to select" },
  "solution.maxsize": { vi: "PDF, DOCX (tối đa 5MB)", en: "PDF, DOCX (max 5MB)" },
  "solution.jd": { vi: "Job Description", en: "Job Description" },
  "solution.jd.placeholder": {
    vi: "Dán mô tả công việc bạn muốn ứng tuyển tại đây...\n\nVD: IT Helpdesk/Support, yêu cầu 2+ năm kinh nghiệm...",
    en: "Paste the job description here...\n\nE.g.: IT Helpdesk/Support, requires 2+ years experience...",
  },
  "solution.language": { vi: "Ngôn ngữ đầu ra", en: "Output Language" },
  "solution.analyze": { vi: "Phân tích CV", en: "Analyze CV" },
  "solution.analyzing": { vi: "Đang phân tích...", en: "Analyzing..." },
  "solution.ai.loading": { vi: "AI đang phân tích CV của bạn...", en: "AI is analyzing your CV..." },
  "solution.ai.wait": { vi: "Quá trình này có thể mất 10-30 giây", en: "This may take 10-30 seconds" },
  "solution.noresult.title": { vi: "Chưa có kết quả", en: "No results yet" },
  "solution.noresult.desc": {
    vi: 'Upload CV và nhập Job Description ở bên trái, sau đó nhấn "Phân tích CV" để bắt đầu.',
    en: 'Upload CV and enter Job Description on the left, then click "Analyze CV" to start.',
  },
  "solution.scoring": { vi: "CV Scoring", en: "CV Scoring" },
  "solution.coverletter": { vi: "Cover Letter & Email", en: "Cover Letter & Email" },
  "score.match": { vi: "Điểm phù hợp với JD", en: "JD Match Score" },
  "score.strengths": { vi: "Điểm mạnh", en: "Strengths" },
  "score.weaknesses": { vi: "Điểm cần cải thiện", en: "Areas to Improve" },
  "score.tips": { vi: "Lời khuyên", en: "Tips" },
  "letter.email": { vi: "Email ứng tuyển", en: "Application Email" },
  "letter.subject": { vi: "Tiêu đề", en: "Subject" },
  "letter.body": { vi: "Nội dung", en: "Content" },
  "letter.cover": { vi: "Cover Letter", en: "Cover Letter" },
  "letter.copy": { vi: "Sao chép", en: "Copy" },
  "letter.copied": { vi: "Đã sao chép", en: "Copied" },
  // About page
  "about.title": { vi: "Về chúng tôi", en: "About Us" },
  "about.desc": {
    vi: "CVGenius là dự án ứng dụng AI vào phân tích và tối ưu CV, được phát triển bởi nhóm sinh viên đầy nhiệt huyết.",
    en: "CVGenius is an AI-powered CV analysis project developed by a passionate student team.",
  },
  "about.mission.title": { vi: "Sứ mệnh", en: "Mission" },
  "about.mission.desc": {
    vi: "Giúp mọi ứng viên Việt Nam tự tin hơn trong hành trình tìm việc bằng công nghệ AI tiên tiến.",
    en: "Help every candidate feel confident in their job search journey with advanced AI technology.",
  },
  "about.team.title": { vi: "Đội ngũ", en: "Team" },
  "about.team.desc": {
    vi: "Nhóm sinh viên đam mê công nghệ, cam kết mang lại giải pháp thực tiễn cho người tìm việc.",
    en: "A passionate student team committed to delivering practical solutions for job seekers.",
  },
  "about.vision.title": { vi: "Tầm nhìn", en: "Vision" },
  "about.vision.desc": {
    vi: "Trở thành công cụ hỗ trợ nghề nghiệp #1 tại Đông Nam Á, ứng dụng AI vào tuyển dụng.",
    en: "Become the #1 career support tool in Southeast Asia, applying AI to recruitment.",
  },
  "about.devteam": { vi: "Đội ngũ phát triển", en: "Development Team" },
  // Contact page
  "contact.title": { vi: "Liên hệ", en: "Contact" },
  "contact.desc": {
    vi: "Bạn có câu hỏi hoặc góp ý? Hãy để lại thông tin, chúng tôi sẽ liên hệ lại ngay.",
    en: "Got questions or feedback? Leave your info and we'll get back to you.",
  },
  "contact.send.title": { vi: "Gửi tin nhắn", en: "Send a Message" },
  "contact.name": { vi: "Họ tên", en: "Full Name" },
  "contact.email": { vi: "Email", en: "Email" },
  "contact.message": { vi: "Nội dung", en: "Message" },
  "contact.message.placeholder": { vi: "Viết tin nhắn của bạn...", en: "Write your message..." },
  "contact.submit": { vi: "Gửi tin nhắn", en: "Send Message" },
  "contact.sending": { vi: "Đang gửi...", en: "Sending..." },
  "contact.success": { vi: "Cảm ơn bạn! Chúng tôi sẽ phản hồi sớm nhất.", en: "Thank you! We'll respond as soon as possible." },
  "contact.support": { vi: "Thông tin hỗ trợ", en: "Support Info" },
  "contact.address": { vi: "Địa chỉ", en: "Address" },
  // Chatbot
  "chatbot.greeting": {
    vi: "Xin chào! Tôi là trợ lý AI của CVGenius. Tôi có thể giúp bạn cải thiện CV, viết lại bullet points hoặc trả lời câu hỏi về hồ sơ ứng tuyển. Hãy hỏi tôi bất cứ điều gì! 🚀",
    en: "Hello! I'm CVGenius AI assistant. I can help you improve your CV, rewrite bullet points or answer questions about your application. Ask me anything! 🚀",
  },
  "chatbot.placeholder": { vi: "Hỏi về CV của bạn...", en: "Ask about your CV..." },
};

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType>({
  language: "vi",
  setLanguage: () => {},
  t: (key: string) => key,
});

export const useLanguage = () => useContext(LanguageContext);

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguage] = useState<Language>(() => {
    if (typeof window !== "undefined") {
      return (localStorage.getItem("cvgenius-lang") as Language) || "vi";
    }
    return "vi";
  });

  const handleSetLanguage = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem("cvgenius-lang", lang);
  };

  const t = (key: string): string => {
    return translations[key]?.[language] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};
