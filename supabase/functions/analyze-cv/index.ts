import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

  try {
    const { cvText, jdText, language } = await req.json();

    if (!cvText || !jdText) {
      return new Response(JSON.stringify({ error: "CV text and JD text are required" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");
    if (!LOVABLE_API_KEY) throw new Error("LOVABLE_API_KEY is not configured");

    const lang = language === "en" ? "English" : "Vietnamese";

    const systemPrompt = `You are an expert career consultant and CV analyst. Analyze the candidate's CV against the job description provided. Return your analysis as a JSON object by calling the analyze_cv function. All text content must be in ${lang}.`;

    const userPrompt = `## CV Content:
${cvText}

## Job Description:
${jdText}

Analyze this CV against the JD. Provide:
1. A match score (0-100)
2. 3-5 specific strengths
3. 3-5 areas for improvement  
4. 3-5 actionable tips
5. A professional application email (subject + body)
6. A professional cover letter

Use professional cover letter and email templates. The email and cover letter should reference specific skills from the CV that match the JD. Write in ${lang}.`;

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
              description: "Return structured CV analysis results",
              parameters: {
                type: "object",
                properties: {
                  score: { type: "number", description: "Match score 0-100" },
                  strengths: { type: "array", items: { type: "string" }, description: "List of strengths" },
                  weaknesses: { type: "array", items: { type: "string" }, description: "Areas to improve" },
                  improvement_tips: { type: "array", items: { type: "string" }, description: "Actionable tips" },
                  email_subject: { type: "string", description: "Application email subject" },
                  email_body: { type: "string", description: "Application email body" },
                  cover_letter: { type: "string", description: "Professional cover letter" },
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
        return new Response(JSON.stringify({ error: "Rate limit exceeded, please try again later." }), {
          status: 429,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      if (response.status === 402) {
        return new Response(JSON.stringify({ error: "AI credits exhausted. Please add credits." }), {
          status: 402,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      const t = await response.text();
      console.error("AI gateway error:", response.status, t);
      return new Response(JSON.stringify({ error: "AI analysis failed" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const data = await response.json();
    const toolCall = data.choices?.[0]?.message?.tool_calls?.[0];
    
    if (!toolCall) {
      console.error("No tool call in response:", JSON.stringify(data));
      return new Response(JSON.stringify({ error: "AI did not return structured data" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const result = JSON.parse(toolCall.function.arguments);

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
