import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

const EMAIL_TEMPLATES = {
  vi: {
    formal: `Kính gửi [Tên người nhận / Phòng Nhân sự],

Tôi viết thư này để ứng tuyển vào vị trí [Tên vị trí] tại [Tên công ty] theo thông tin tuyển dụng mà tôi được biết.

Với [X năm] kinh nghiệm trong lĩnh vực [lĩnh vực], tôi tự tin rằng năng lực chuyên môn và kinh nghiệm thực tiễn của tôi sẽ đóng góp tích cực cho đội ngũ của quý công ty.

[Đoạn trình bày kỹ năng phù hợp với JD]

Tôi rất mong có cơ hội được trao đổi thêm về cách tôi có thể đóng góp cho [Tên công ty]. Xin vui lòng liên hệ với tôi qua email [email] hoặc số điện thoại [SĐT].

Trân trọng,
[Họ tên]`,
    modern: `Chào anh/chị [Tên],

Tôi rất hào hứng khi thấy vị trí [Tên vị trí] tại [Tên công ty] — đây chính xác là cơ hội mà tôi đang tìm kiếm!

[Mở đầu ấn tượng liên quan đến thành tựu nổi bật]

Trong [X năm] làm việc, tôi đã:
• [Thành tựu 1 với con số cụ thể]
• [Thành tựu 2 liên quan đến JD]
• [Kỹ năng đặc biệt phù hợp]

Tôi tin rằng sự kết hợp giữa [kỹ năng A] và [kỹ năng B] sẽ mang lại giá trị thực cho team.

Rất mong được trao đổi thêm!

Thân,
[Họ tên]`,
    creative: `Xin chào [Tên công ty]! 👋

Khi đọc JD cho vị trí [Tên vị trí], tôi nghĩ: "Đây là công việc dành cho mình!"

Tại sao? Vì:
🎯 [Điểm match #1 với JD]
💡 [Kinh nghiệm/thành tựu nổi bật]
🚀 [Giá trị tôi mang lại]

[Câu chuyện ngắn về passion/project liên quan]

Tôi sẵn sàng cho cuộc trò chuyện bất cứ lúc nào. Let's connect!

[Họ tên]
[Email] | [SĐT]`,
  },
  en: {
    formal: `Dear [Hiring Manager / HR Department],

I am writing to express my interest in the [Position] role at [Company Name] as advertised.

With [X years] of experience in [field], I am confident that my professional expertise and practical experience will contribute positively to your team.

[Paragraph highlighting skills matching the JD]

I look forward to the opportunity to discuss how I can contribute to [Company Name]. Please feel free to contact me at [email] or [phone].

Sincerely,
[Full Name]`,
    modern: `Hi [Name],

I was excited to see the [Position] opening at [Company Name] — this is exactly the opportunity I've been looking for!

[Impressive opening related to a key achievement]

Over the past [X years], I have:
• [Achievement 1 with specific metrics]
• [Achievement 2 relevant to JD]
• [Unique skill that fits]

I believe the combination of [skill A] and [skill B] will bring real value to the team.

Looking forward to connecting!

Best,
[Full Name]`,
    creative: `Hello [Company Name]! 👋

When I read the JD for [Position], I thought: "This role was made for me!"

Here's why:
🎯 [Match point #1 with JD]
💡 [Notable experience/achievement]
🚀 [Value I bring]

[Short story about a relevant passion/project]

I'm ready to chat anytime. Let's connect!

[Full Name]
[Email] | [Phone]`,
  },
};

const COVER_LETTER_TEMPLATES = {
  vi: {
    formal: `[Họ tên]
[Địa chỉ]
[Email] | [SĐT]
[Ngày tháng]

Kính gửi: [Tên người nhận / Phòng Nhân sự]
[Tên công ty]
[Địa chỉ công ty]

RE: Ứng tuyển vị trí [Tên vị trí]

Kính gửi Quý Anh/Chị,

Tôi viết thư này để bày tỏ sự quan tâm của mình đối với vị trí [Tên vị trí] tại [Tên công ty]. Với nền tảng chuyên môn vững chắc trong [lĩnh vực] cùng [X năm] kinh nghiệm, tôi tin rằng mình là ứng viên phù hợp cho vị trí này.

[Đoạn 1: Giới thiệu kinh nghiệm chính và thành tựu nổi bật]

[Đoạn 2: Phân tích cụ thể cách kỹ năng của bạn đáp ứng yêu cầu JD]

[Đoạn 3: Thể hiện sự hiểu biết về công ty và cam kết đóng góp]

Tôi rất mong có cơ hội được phỏng vấn và trình bày chi tiết hơn về cách tôi có thể đóng góp cho sự phát triển của [Tên công ty].

Trân trọng,
[Họ tên]`,
    modern: `## [Họ tên] — Ứng tuyển [Tên vị trí]

📧 [Email] | 📱 [SĐT] | 🔗 [LinkedIn]

---

### Tại sao tôi phù hợp?

[Mở đầu mạnh mẽ: 2-3 câu tóm tắt giá trị cốt lõi]

### Kinh nghiệm & Thành tựu

**[Công ty/Dự án gần nhất]** — [Vai trò]
• [Thành tựu định lượng #1]
• [Thành tựu định lượng #2]

**Kỹ năng phù hợp với JD:**
✅ [Kỹ năng 1]
✅ [Kỹ năng 2]
✅ [Kỹ năng 3]

### Tại sao [Tên công ty]?

[1-2 câu thể hiện sự am hiểu về công ty và động lực ứng tuyển]

---

Sẵn sàng trao đổi chi tiết hơn. Rất mong được kết nối!

[Họ tên]`,
    creative: `# Xin chào, tôi là [Họ tên]! 🙋

> "[Quote ngắn thể hiện triết lý làm việc]"

## Câu chuyện của tôi

[Đoạn mở đầu cuốn hút — tại sao bạn đam mê lĩnh vực này]

## Tôi mang đến điều gì?

🏆 **[Thành tựu lớn nhất]** — [Mô tả ngắn]
📊 **[Con số ấn tượng]** — [Context]
🎯 **[Kỹ năng đặc biệt]** — [Áp dụng thế nào]

## Tại sao [Tên công ty]?

[Câu chuyện cá nhân hoặc lý do cụ thể]

## Let's talk! 🚀

📧 [Email]
📱 [SĐT]
🔗 [LinkedIn/Portfolio]`,
  },
  en: {
    formal: `[Full Name]
[Address]
[Email] | [Phone]
[Date]

To: [Hiring Manager / HR Department]
[Company Name]
[Company Address]

RE: Application for [Position]

Dear Sir/Madam,

I am writing to express my keen interest in the [Position] role at [Company Name]. With a strong foundation in [field] and [X years] of experience, I believe I am a well-suited candidate for this position.

[Paragraph 1: Key experience and notable achievements]

[Paragraph 2: Specific analysis of how your skills meet JD requirements]

[Paragraph 3: Demonstrate understanding of the company and commitment]

I look forward to the opportunity to interview and elaborate on how I can contribute to [Company Name]'s growth.

Sincerely,
[Full Name]`,
    modern: `## [Full Name] — Applying for [Position]

📧 [Email] | 📱 [Phone] | 🔗 [LinkedIn]

---

### Why I'm a Great Fit

[Strong opening: 2-3 sentences summarizing core value proposition]

### Experience & Achievements

**[Most Recent Company/Project]** — [Role]
• [Quantified achievement #1]
• [Quantified achievement #2]

**Skills Matching JD:**
✅ [Skill 1]
✅ [Skill 2]
✅ [Skill 3]

### Why [Company Name]?

[1-2 sentences showing company knowledge and motivation]

---

Ready to discuss further. Looking forward to connecting!

[Full Name]`,
    creative: `# Hello, I'm [Full Name]! 🙋

> "[Short quote reflecting work philosophy]"

## My Story

[Engaging opening paragraph — why you're passionate about this field]

## What I Bring to the Table

🏆 **[Biggest achievement]** — [Brief description]
📊 **[Impressive metric]** — [Context]
🎯 **[Unique skill]** — [How it applies]

## Why [Company Name]?

[Personal story or specific reason]

## Let's talk! 🚀

📧 [Email]
📱 [Phone]
🔗 [LinkedIn/Portfolio]`,
  },
};

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

  try {
    const { cvText, jdText, language, templateStyle, mode } = await req.json();
    const analysisMode = mode || "full";

    // Edge case: missing inputs
    if (!cvText || !jdText) {
      return new Response(JSON.stringify({ error: "CV text and JD text are required" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Edge case: JD too short
    if (jdText.trim().length < 20) {
      return new Response(JSON.stringify({ error: language === "en" ? "Job description is too short. Please provide more details." : "Mô tả công việc quá ngắn. Vui lòng cung cấp thêm chi tiết." }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Edge case: CV text too short (likely binary/unreadable)
    if (cvText.trim().length < 30) {
      return new Response(JSON.stringify({ error: language === "en" ? "Could not read CV content. Please use a text-based PDF or TXT file." : "Không thể đọc nội dung CV. Vui lòng sử dụng file PDF dạng text hoặc file TXT." }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");
    if (!LOVABLE_API_KEY) throw new Error("LOVABLE_API_KEY is not configured");

    const lang = language === "en" ? "English" : "Vietnamese";
    const style = templateStyle || "formal";
    
    const emailTemplate = EMAIL_TEMPLATES[language as "vi" | "en"]?.[style as "formal" | "modern" | "creative"] || EMAIL_TEMPLATES.vi.formal;
    const coverTemplate = COVER_LETTER_TEMPLATES[language as "vi" | "en"]?.[style as "formal" | "modern" | "creative"] || COVER_LETTER_TEMPLATES.vi.formal;

    const systemPrompt = `You are an expert career consultant, professional resume writer, and application letter specialist. You have deep expertise in crafting compelling cover letters and application emails that get responses.

Your task is to analyze the candidate's CV against the job description, then generate professional application materials.

IMPORTANT RULES:
1. ALL output text must be in ${lang}.
2. Use the template style "${style}" as reference for tone and structure.
3. Replace ALL placeholder brackets [like this] with actual information extracted from the CV and JD.
4. If the CV doesn't contain certain info (name, email, phone), use reasonable placeholders like "[Your Name]" in ${lang}.
5. Quantify achievements whenever possible (numbers, percentages, metrics).
6. Reference SPECIFIC skills from the CV that match the JD requirements.
7. The cover letter and email must feel authentic and personalized, not generic.
8. For "formal" style: Professional, traditional business format.
9. For "modern" style: Clean, structured with bullet points and sections.
10. For "creative" style: Engaging, personality-driven with emojis and storytelling.`;

    const userPrompt = `## CV Content:
${cvText}

## Job Description:
${jdText}

## Email Template Reference (${style} style, ${lang}):
${emailTemplate}

## Cover Letter Template Reference (${style} style, ${lang}):
${coverTemplate}

---

INSTRUCTIONS:
1. Analyze the CV against the JD thoroughly.
2. Score the match (0-100) based on: skills match, experience relevance, education fit, keyword alignment.
3. Identify 3-5 specific strengths where the CV matches the JD.
4. Identify 3-5 specific areas where the CV falls short of JD requirements.
5. Provide 3-5 actionable improvement tips.
6. Write a complete application email following the ${style} template style above. Replace all placeholders with actual data from the CV. The email must reference specific matching skills.
7. Write a complete cover letter following the ${style} template style above. Replace all placeholders with actual data from the CV. The cover letter must be detailed, professional, and tailored to this specific JD.

CRITICAL: Do NOT leave any [placeholder brackets] in the final output. Extract real information from the CV to fill them in. If info is unavailable, write "${language === "en" ? "[Your Name]" : "[Họ tên của bạn]"}" etc.

All text must be in ${lang}.`;

    const response = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${LOVABLE_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "google/gemini-3-flash-preview",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
        tools: [
          {
            type: "function",
            function: {
              name: "analyze_cv",
              description: "Return structured CV analysis with professional email and cover letter",
              parameters: {
                type: "object",
                properties: {
                  score: { type: "number", description: "Match score 0-100" },
                  strengths: { type: "array", items: { type: "string" }, description: "3-5 specific strengths" },
                  weaknesses: { type: "array", items: { type: "string" }, description: "3-5 areas to improve" },
                  improvement_tips: { type: "array", items: { type: "string" }, description: "3-5 actionable tips" },
                  email_subject: { type: "string", description: "Professional email subject line" },
                  email_body: { type: "string", description: "Complete application email body following the template style" },
                  cover_letter: { type: "string", description: "Complete professional cover letter following the template style" },
                },
                required: ["score", "strengths", "weaknesses", "improvement_tips", "email_subject", "email_body", "cover_letter"],
                additionalProperties: false,
              },
            },
          },
        ],
        tool_choice: { type: "function", function: { name: "analyze_cv" } },
      }),
    });

    if (!response.ok) {
      if (response.status === 429) {
        return new Response(JSON.stringify({ error: language === "en" ? "Rate limit exceeded, please try again later." : "Đã vượt quá giới hạn yêu cầu, vui lòng thử lại sau." }), {
          status: 429,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      if (response.status === 402) {
        return new Response(JSON.stringify({ error: language === "en" ? "AI credits exhausted. Please add credits." : "Hết credit AI. Vui lòng nạp thêm." }), {
          status: 402,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      const t = await response.text();
      console.error("AI gateway error:", response.status, t);
      return new Response(JSON.stringify({ error: language === "en" ? "AI analysis failed. Please try again." : "Phân tích AI thất bại. Vui lòng thử lại." }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const data = await response.json();
    const toolCall = data.choices?.[0]?.message?.tool_calls?.[0];
    
    if (!toolCall) {
      console.error("No tool call in response:", JSON.stringify(data));
      return new Response(JSON.stringify({ error: language === "en" ? "AI did not return structured data. Please try again." : "AI không trả về dữ liệu có cấu trúc. Vui lòng thử lại." }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const result = JSON.parse(toolCall.function.arguments);

    // Edge case: validate result structure
    if (typeof result.score !== "number" || result.score < 0 || result.score > 100) {
      result.score = Math.max(0, Math.min(100, result.score || 50));
    }
    if (!Array.isArray(result.strengths)) result.strengths = [];
    if (!Array.isArray(result.weaknesses)) result.weaknesses = [];
    if (!Array.isArray(result.improvement_tips)) result.improvement_tips = [];
    if (!result.email_subject) result.email_subject = language === "en" ? "Application for the position" : "Thư ứng tuyển vị trí";
    if (!result.email_body) result.email_body = "";
    if (!result.cover_letter) result.cover_letter = "";

    return new Response(JSON.stringify(result), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (e) {
    console.error("analyze-cv error:", e);
    return new Response(JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
