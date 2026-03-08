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
  // Auth
  "nav.login": { vi: "Đăng nhập", en: "Login" },
  "nav.logout": { vi: "Đăng xuất", en: "Logout" },
  "auth.subtitle": { vi: "Đăng nhập để bắt đầu phân tích CV", en: "Sign in to start analyzing your CV" },
  "auth.google": { vi: "Đăng nhập với Google", en: "Sign in with Google" },
  "auth.or": { vi: "hoặc", en: "or" },
  "auth.email": { vi: "Email", en: "Email" },
  "auth.send.otp": { vi: "Gửi mã xác thực", en: "Send verification code" },
  "auth.otp.sent": { vi: "Đã gửi mã xác thực! Kiểm tra email của bạn.", en: "Code sent! Check your email." },
  "auth.otp.check": { vi: "Nhập mã 6 số đã gửi đến", en: "Enter the 6-digit code sent to" },
  "auth.verify": { vi: "Xác thực", en: "Verify" },
  "auth.back": { vi: "← Quay lại", en: "← Go back" },
  "auth.login.success": { vi: "Đăng nhập thành công!", en: "Login successful!" },
  "solution.login.required": { vi: "Vui lòng đăng nhập để sử dụng tính năng này", en: "Please login to use this feature" },
  "solution.file.too.large": { vi: "File quá lớn. Vui lòng chọn file dưới 5MB.", en: "File too large. Please select a file under 5MB." },
  // Auth - login
  "auth.tab.password": { vi: "Mật khẩu", en: "Password" },
  "auth.tab.otp": { vi: "Mã OTP", en: "OTP Code" },
  "auth.login.button": { vi: "Đăng nhập", en: "Sign In" },
  "auth.no.account": { vi: "Chưa có tài khoản?", en: "Don't have an account?" },
  "auth.signup.link": { vi: "Đăng ký ngay", en: "Sign up now" },
  // Signup
  "nav.signup": { vi: "Đăng ký", en: "Sign Up" },
  "signup.subtitle": { vi: "Tạo tài khoản để bắt đầu phân tích CV", en: "Create an account to start analyzing your CV" },
  "signup.google": { vi: "Đăng ký với Google", en: "Sign up with Google" },
  "signup.name": { vi: "Tên hiển thị", en: "Display Name" },
  "signup.name.placeholder": { vi: "Nhập tên của bạn", en: "Enter your name" },
  "signup.password": { vi: "Mật khẩu", en: "Password" },
  "signup.confirm.password": { vi: "Xác nhận mật khẩu", en: "Confirm Password" },
  "signup.button": { vi: "Đăng ký", en: "Sign Up" },
  "signup.have.account": { vi: "Đã có tài khoản?", en: "Already have an account?" },
  "signup.login.link": { vi: "Đăng nhập", en: "Sign in" },
  "signup.fill.all": { vi: "Vui lòng điền đầy đủ thông tin", en: "Please fill in all fields" },
  "signup.password.min": { vi: "Mật khẩu phải có ít nhất 6 ký tự", en: "Password must be at least 6 characters" },
  "signup.password.mismatch": { vi: "Mật khẩu xác nhận không khớp", en: "Passwords do not match" },
  "signup.success": { vi: "Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.", en: "Sign up successful! Please check your email to verify your account." },
  // Template styles
  "solution.template.style": { vi: "Phong cách template", en: "Template Style" },
  "template.formal": { vi: "Trang trọng", en: "Formal" },
  "template.formal.desc": { vi: "Phong cách chuyên nghiệp, truyền thống — phù hợp ngân hàng, tập đoàn lớn", en: "Professional, traditional style — ideal for banks, large corporations" },
  "template.modern": { vi: "Hiện đại", en: "Modern" },
  "template.modern.desc": { vi: "Bố cục rõ ràng, bullet points — phù hợp công ty tech, startup", en: "Clean layout, bullet points — ideal for tech companies, startups" },
  "template.creative": { vi: "Sáng tạo", en: "Creative" },
  "template.creative.desc": { vi: "Phong cách cá tính, storytelling — phù hợp marketing, design", en: "Personality-driven, storytelling — ideal for marketing, design" },
  // Edge case messages
  "solution.jd.too.short": { vi: "Mô tả công việc quá ngắn. Vui lòng cung cấp thêm chi tiết.", en: "Job description is too short. Please provide more details." },
  "solution.cv.unreadable": { vi: "Không thể đọc nội dung CV. Vui lòng sử dụng file PDF dạng text hoặc file TXT.", en: "Could not read CV content. Please use a text-based PDF or TXT file." },
  "solution.analyze.error": { vi: "Phân tích thất bại. Vui lòng thử lại.", en: "Analysis failed. Please try again." },
  // Navbar dropdown
  "nav.cv.analysis": { vi: "Phân tích CV", en: "CV Analysis" },
  "nav.write.mail": { vi: "Viết Mail", en: "Write Mail" },
  "nav.write.cover": { vi: "Viết Cover Letter", en: "Write Cover Letter" },
  // Write Mail page
  "writemail.title": { vi: "Viết Email ứng tuyển", en: "Write Application Email" },
  "writemail.desc": { vi: "Tạo email ứng tuyển chuyên nghiệp dựa trên CV và JD", en: "Generate professional application emails based on CV and JD" },
  "writemail.generate": { vi: "Tạo Email", en: "Generate Email" },
  "writemail.empty.title": { vi: "Chưa có email", en: "No email yet" },
  "writemail.empty.desc": { vi: "Upload CV và nhập JD, sau đó nhấn \"Tạo Email\" để bắt đầu.", en: "Upload CV and enter JD, then click \"Generate Email\" to start." },
  "content.meta.title": { vi: "Thông tin nhận diện được", en: "Extracted Information" },
  "content.meta.candidate": { vi: "Ứng viên", en: "Candidate" },
  "content.meta.recipient": { vi: "Người nhận", en: "Recipient" },
  "content.meta.company": { vi: "Công ty", en: "Company" },
  "content.meta.position": { vi: "Vị trí", en: "Position" },
  "content.meta.experience": { vi: "Kinh nghiệm", en: "Experience" },
  "content.meta.years": { vi: "năm", en: "years" },
  "content.meta.phone": { vi: "Số điện thoại", en: "Phone" },
  "content.meta.address": { vi: "Địa chỉ", en: "Address" },
  "content.meta.skills": { vi: "Kỹ năng chính", en: "Key skills" },
  // Cover Letter page
  "coverletter.title": { vi: "Viết Cover Letter", en: "Write Cover Letter" },
  "coverletter.desc": { vi: "Tạo cover letter chuyên nghiệp dựa trên CV và JD", en: "Generate professional cover letters based on CV and JD" },
  "coverletter.generate": { vi: "Tạo Cover Letter", en: "Generate Cover Letter" },
  "coverletter.empty.title": { vi: "Chưa có cover letter", en: "No cover letter yet" },
  "coverletter.empty.desc": { vi: "Upload CV và nhập JD, sau đó nhấn \"Tạo Cover Letter\" để bắt đầu.", en: "Upload CV and enter JD, then click \"Generate Cover Letter\" to start." },
  // Export
  "export.pdf.success": { vi: "Đã xuất PDF thành công!", en: "PDF exported successfully!" },
  "export.docx.success": { vi: "Đã xuất DOCX thành công!", en: "DOCX exported successfully!" },
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
