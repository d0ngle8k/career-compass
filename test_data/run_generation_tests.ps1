#!/usr/bin/env pwsh
<#
.SYNOPSIS
Test script to generate 100 emails and 100 cover letters (50 Vietnamese + 50 English each)
and verify information extraction accuracy and spelling.

.DESCRIPTION
This script:
1. Authenticates with backend
2. Generates 100 email pairs (50 VI, 50 EN)
3. Generates 100 cover letter pairs (50 VI, 50 EN)
4. Checks if metadata is extracted correctly
5. Validates spelling
6. Generates comprehensive report
#>

param(
    [string]$BackendUrl = "http://127.0.0.1:9000",
    [string]$OutputFile = "c:\Users\Thanh\Desktop\career-compass-ai\test_data\generation_test_results.json"
)

# Configuration
$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

# Test data with realistic variations
$TestData = @{
    Vietnamese = @(
        @{
            companies = @("Công ty Công nghệ ABC", "Tech Solutions Vietnam", "NextGen Technology", "CloudFirst Vietnam", "DataLake Corporation", "FPT Software", "Viettel Digital", "Momo", "Tiki", "Grab Vietnam")
            positions = @("Lập trình viên Backend", "QA Engineer", "Frontend Developer", "DevOps Engineer", "Data Engineer", "Full Stack Developer", "Mobile Developer", "Systems Engineer", "Senior Architect", "Tech Lead")
            names = @("Trần Minh Đức", "Lê Thị Hương", "Phạm Quốc Hùng", "Bùi Thị Lan Anh", "Ngô Văn Sơn", "Võ Minh Khoa", "Hoàng Thị Linh", "Đặng Văn Hùng", "Tô Thị Huỳnh", "Phan Quốc Bảo")
            emails = @("duc.tran@gmail.com", "huong.le@gmail.com", "hung.pham@gmail.com", "lananh@gmail.com", "vson@gmail.com", "khoa.vo@gmail.com", "linh.hoang@gmail.com", "hung.dang@gmail.com", "huynh.to@gmail.com", "bao.phan@gmail.com")
            phones = @("0912345678", "0987654321", "0911111111", "0898765432", "0901234567", "0923456789", "0934567890", "0945678901", "0956789012", "0967890123")
            recipients = @("Ông Phạm Văn An", "Ms. Nguyễn Thị Mai", "Ông Trần Minh Tuấn", "Bà Võ Thị Hoa", "Thầy Nguyễn Văn Sơn", "Chị Đặng Thị Hương", "Anh Lê Quốc Hùng", "Bà Trần Thị Liên", "Ông Phan Minh Đức", "Chị Hoàng Thị Thanh")
            skills = @("Python, Django, PostgreSQL", "Java, Spring Boot, Kubernetes", "React, TypeScript, Node.js", "Kubernetes, Docker, AWS", "Apache Spark, Kafka, SQL", "JavaScript, HTML/CSS, React", "Linux, Shell Script, Terraform", "Test Automation, Selenium", "Machine Learning, TensorFlow", "Data Analytics, Tableau")
            experiences = @(3, 4, 5, 6, 7, 8, 2, 4, 5, 3)
            skills_list = @("Python", "Java", "JavaScript", "Docker", "Kubernetes", "SQL", "PostgreSQL", "MongoDB", "AWS", "Git")
        }
    )
    English = @(
        @{
            companies = @("TechCorp Inc", "StartupXYZ", "CloudScale Solutions", "SoftwarePro Inc", "AI Innovations Ltd", "DataFlow Systems", "SecureWeb Solutions", "MobileFirst Apps", "CloudNative Labs", "DevOps Masters")
            positions = @("Senior Software Engineer", "Full Stack Developer", "DevOps Engineer", "QA Automation Engineer", "Machine Learning Engineer", "Backend Developer", "Frontend Engineer", "Systems Architect", "Tech Lead", "Solutions Architect")
            names = @("Michael Johnson", "Emily Rodriguez", "James Wilson", "Jessica Chen", "Christopher Lee", "Amanda White", "Robert Taylor", "Sarah Smith", "David Brown", "Lisa Anderson")
            emails = @("michael.j@gmail.com", "emily.r@gmail.com", "james.w@gmail.com", "jessica.c@gmail.com", "chris.l@gmail.com", "amanda.w@gmail.com", "robert.t@gmail.com", "sarah.s@gmail.com", "david.b@gmail.com", "lisa.a@gmail.com")
            phones = @("+1-555-0123", "+1-555-0456", "(555) 789-0123", "(555) 234-5678", "(555) 456-7890", "(555) 567-8901", "(555) 678-9012", "(555) 789-0123", "(555) 890-1234", "(555) 901-2345")
            recipients = @("Sarah Smith", "David Brown", "Lisa Anderson", "Robert Taylor", "Amanda White", "Michael Johnson", "Emily Rodriguez", "James Wilson", "Jessica Chen", "Christopher Lee")
            skills = @("Java, Spring Boot, Microservices", "React, Node.js, MongoDB", "Kubernetes, Docker, Terraform", "Selenium, Python, Pytest", "TensorFlow, Python, ML", "Python, Django, PostgreSQL", "JavaScript, TypeScript, React", "Linux, Cloud, Devops", "C++, System Design", "AWS, CI/CD, Architecture")
            experiences = @(5, 4, 3, 5, 4, 6, 3, 7, 8, 5)
            skills_list = @("Java", "Python", "JavaScript", "Docker", "Kubernetes", "AWS", "React", "Spring Boot", "Azure", "Git")
        }
    )
}

Write-Host "`n=== Career Compass AI - Content Generation Test Suite ===" -ForegroundColor Cyan
Write-Host "Backend URL: $BackendUrl" -ForegroundColor Yellow
Write-Host "Output File: $OutputFile`n" -ForegroundColor Yellow

# Step 1: Authentication
Write-Host "[1/6] Authenticating with backend..." -ForegroundColor Yellow
try {
    $loginBody = @{
        email = "admin@careercompass.local"
        password = "admin123"
    } | ConvertTo-Json

    $loginResponse = Invoke-WebRequest -Uri "$BackendUrl/api/v1/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body $loginBody `
        -UseBasicParsing

    $loginData = $loginResponse.Content | ConvertFrom-Json
    $token = $loginData.data.access_token
    Write-Host "✓ Authentication successful" -ForegroundColor Green
}
catch {
    Write-Host "✗ Authentication failed: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Generate diverse test data
Write-Host "`n[2/6] Generating diverse test data for 100 test cases..." -ForegroundColor Yellow

$testCases = @()
$caseId = 1

# Generate 50 Vietnamese test cases
$viData = $TestData.Vietnamese[0]
for ($i = 0; $i -lt 50; $i++) {
    $companyIdx = $i % $viData.companies.Count
    $posIdx = ($i + 1) % $viData.positions.Count
    $nameIdx = ($i + 2) % $viData.names.Count
    $emailIdx = ($i + 3) % $viData.emails.Count
    $phoneIdx = ($i + 4) % $viData.phones.Count
    $recipientIdx = ($i + 5) % $viData.recipients.Count
    $skillsIdx = ($i + 6) % $viData.skills.Count
    $expIdx = ($i + 7) % $viData.experiences.Count

    $cv = @"
HỒ SƠ ỨNG VIÊN

Họ và Tên: $($viData.names[$nameIdx])
Email: $($viData.emails[$emailIdx])
Điện thoại: $($viData.phones[$phoneIdx])
Địa chỉ: Hồ Chí Minh

KINH NGHIỆM
- $($viData.experiences[$expIdx]) năm kinh nghiệm với $($viData.skills[$skillsIdx])
- Phát triển ứng dụng, tối ưu hóa hệ thống
- Làm việc với các công ty lớn

KỸ NĂNG
$($viData.skills[$skillsIdx])
Git, Linux, Agile
"@

    $jd = @"
VỊ TRÍ: $($viData.positions[$posIdx])
CÔNG TY: $($viData.companies[$companyIdx])
Thư gửi: $($viData.recipients[$recipientIdx])

Chúng tôi tìm kiếm $($viData.positions[$posIdx]) có $($viData.experiences[$expIdx])+1 năm kinh nghiệm.
Ứng viên phải thành thạo $($viData.skills[$skillsIdx]).
"@

    $testCases += @{
        id = $caseId++
        language = "vi"
        cv = $cv
        jd = $jd
        expectedCompany = $viData.companies[$companyIdx]
        expectedPosition = $viData.positions[$posIdx]
        expectedName = $viData.names[$nameIdx]
        expectedEmail = $viData.emails[$emailIdx]
        expectedPhone = $viData.phones[$phoneIdx]
        expectedRecipient = $viData.recipients[$recipientIdx]
    }
}

# Generate 50 English test cases
$enData = $TestData.English[0]
for ($i = 0; $i -lt 50; $i++) {
    $companyIdx = $i % $enData.companies.Count
    $posIdx = ($i + 1) % $enData.positions.Count
    $nameIdx = ($i + 2) % $enData.names.Count
    $emailIdx = ($i + 3) % $enData.emails.Count
    $phoneIdx = ($i + 4) % $enData.phones.Count
    $recipientIdx = ($i + 5) % $enData.recipients.Count
    $skillsIdx = ($i + 6) % $enData.skills.Count
    $expIdx = ($i + 7) % $enData.experiences.Count

    $cv = @"
PROFESSIONAL RESUME

Name: $($enData.names[$nameIdx])
Email: $($enData.emails[$emailIdx])
Phone: $($enData.phones[$phoneIdx])
Location: United States

PROFESSIONAL EXPERIENCE
- $($enData.experiences[$expIdx]) years with $($enData.skills[$skillsIdx])
- System development and optimization
- Worked with Fortune 500 companies

TECHNICAL SKILLS
$($enData.skills[$skillsIdx])
Git, AWS, Agile Methodology
"@

    $jd = @"
Position: $($enData.positions[$posIdx])
Company: $($enData.companies[$companyIdx])
Hiring Manager: $($enData.recipients[$recipientIdx])

We are seeking a $($enData.positions[$posIdx]) with $($enData.experiences[$expIdx])+3 years of experience.
Must have expertise in $($enData.skills[$skillsIdx]).
"@

    $testCases += @{
        id = $caseId++
        language = "en"
        cv = $cv
        jd = $jd
        expectedCompany = $enData.companies[$companyIdx]
        expectedPosition = $enData.positions[$posIdx]
        expectedName = $enData.names[$nameIdx]
        expectedEmail = $enData.emails[$emailIdx]
        expectedPhone = $enData.phones[$phoneIdx]
        expectedRecipient = $enData.recipients[$recipientIdx]
    }
}

Write-Host "✓ Generated $($testCases.Count) test cases" -ForegroundColor Green

# Step 3: Generate emails
Write-Host "`n[3/6] Generating 100 emails (50 Vietnamese + 50 English)..." -ForegroundColor Yellow

$emailResults = @()
$emailSuccess = 0
$emailFailure = 0
$headers = @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
}

foreach ($testCase in $testCases) {
    try {
        $payload = @{
            cv_text = $testCase.cv
            jd_text = $testCase.jd
            language = $testCase.language
        } | ConvertTo-Json -Depth 10

        $response = Invoke-WebRequest -Uri "$BackendUrl/api/v1/ai/generate-email" `
            -Method POST `
            -Headers $headers `
            -Body $payload `
            -UseBasicParsing

        $data = $response.Content | ConvertFrom-Json
        $emailSuccess++

        # Validate extraction
        $metadata = $data.data.extracted_metadata
        $validations = @{
            nameMatch = $metadata.candidate_name -eq $testCase.expectedName
            emailMatch = $metadata.email -eq $testCase.expectedEmail
            phoneMatch = $metadata.phone -eq $testCase.expectedPhone
            companyMatch = $metadata.company_name -eq $testCase.expectedCompany
            positionMatch = $metadata.position -eq $testCase.expectedPosition
            recipientMatch = $metadata.recipient -eq $testCase.expectedRecipient
        }

        $emailResults += @{
            caseId = $testCase.id
            language = $testCase.language
            success = $true
            subjectLength = $data.data.email_subject.Length
            bodyLength = $data.data.email_body.Length
            metadata = $metadata
            validations = $validations
            extractionAccuracy = (($validations.Values | Where-Object {$_}).Count / $validations.Count) * 100
        }

        Write-Host -NoNewline "."
    }
    catch {
        $emailFailure++
        $emailResults += @{
            caseId = $testCase.id
            language = $testCase.language
            success = $false
            error = $_.Exception.Message
        }
        Write-Host -NoNewline "x"
    }
}

Write-Host "`n✓ Email generation: $emailSuccess successful, $emailFailure failed" -ForegroundColor Green

# Step 4: Generate cover letters
Write-Host "`n[4/6] Generating 100 cover letters (50 Vietnamese + 50 English)..." -ForegroundColor Yellow

$coverResults = @()
$coverSuccess = 0
$coverFailure = 0

foreach ($testCase in $testCases) {
    try {
        $payload = @{
            cv_text = $testCase.cv
            jd_text = $testCase.jd
            language = $testCase.language
        } | ConvertTo-Json -Depth 10

        $response = Invoke-WebRequest -Uri "$BackendUrl/api/v1/ai/generate-cover-letter" `
            -Method POST `
            -Headers $headers `
            -Body $payload `
            -UseBasicParsing

        $data = $response.Content | ConvertFrom-Json
        $coverSuccess++

        # Validate extraction
        $metadata = $data.data.extracted_metadata
        $validations = @{
            nameMatch = $metadata.candidate_name -eq $testCase.expectedName
            emailMatch = $metadata.email -eq $testCase.expectedEmail
            phoneMatch = $metadata.phone -eq $testCase.expectedPhone
            companyMatch = $metadata.company_name -eq $testCase.expectedCompany
            positionMatch = $metadata.position -eq $testCase.expectedPosition
            recipientMatch = $metadata.recipient -eq $testCase.expectedRecipient
        }

        $coverResults += @{
            caseId = $testCase.id
            language = $testCase.language
            success = $true
            letterLength = $data.data.cover_letter.Length
            metadata = $metadata
            validations = $validations
            extractionAccuracy = (($validations.Values | Where-Object {$_}).Count / $validations.Count) * 100
        }

        Write-Host -NoNewline "."
    }
    catch {
        $coverFailure++
        $coverResults += @{
            caseId = $testCase.id
            language = $testCase.language
            success = $false
            error = $_.Exception.Message
        }
        Write-Host -NoNewline "x"
    }
}

Write-Host "`n✓ Cover letter generation: $coverSuccess successful, $coverFailure failed" -ForegroundColor Green

# Step 5: Analyze results
Write-Host "`n[5/6] Analyzing results..." -ForegroundColor Yellow

# Email statistics
$emailStats = @{
    totalGenerated = ($emailResults | Where-Object { $_.success }).Count
    successRate = (($emailResults | Where-Object { $_.success }).Count / $emailResults.Count) * 100
    vietnameseSuccess = ($emailResults | Where-Object { $_.success -and $_.language -eq "vi" }).Count
    englishSuccess = ($emailResults | Where-Object { $_.success -and $_.language -eq "en" }).Count
    avgExtractionAccuracy = ($emailResults | Where-Object { $_.success } | Measure-Object -Property extractionAccuracy -Average).Average
    extractionBreakdown = @{
        nameAccuracy = (($emailResults | Where-Object { $_.success -and $_.validations.nameMatch } | Measure-Object).Count / ($emailResults | Where-Object { $_.success }).Count) * 100
        emailAccuracy = (($emailResults | Where-Object { $_.success -and $_.validations.emailMatch } | Measure-Object).Count / ($emailResults | Where-Object { $_.success }).Count) * 100
        phoneAccuracy = (($emailResults | Where-Object { $_.success -and $_.validations.phoneMatch } | Measure-Object).Count / ($emailResults | Where-Object { $_.success }).Count) * 100
        companyAccuracy = (($emailResults | Where-Object { $_.success -and $_.validations.companyMatch } | Measure-Object).Count / ($emailResults | Where-Object { $_.success }).Count) * 100
        positionAccuracy = (($emailResults | Where-Object { $_.success -and $_.validations.positionMatch } | Measure-Object).Count / ($emailResults | Where-Object { $_.success }).Count) * 100
        recipientAccuracy = (($emailResults | Where-Object { $_.success -and $_.validations.recipientMatch } | Measure-Object).Count / ($emailResults | Where-Object { $_.success }).Count) * 100
    }
}

# Cover letter statistics
$coverStats = @{
    totalGenerated = ($coverResults | Where-Object { $_.success }).Count
    successRate = (($coverResults | Where-Object { $_.success }).Count / $coverResults.Count) * 100
    vietnameseSuccess = ($coverResults | Where-Object { $_.success -and $_.language -eq "vi" }).Count
    englishSuccess = ($coverResults | Where-Object { $_.success -and $_.language -eq "en" }).Count
    avgExtractionAccuracy = ($coverResults | Where-Object { $_.success } | Measure-Object -Property extractionAccuracy -Average).Average
    extractionBreakdown = @{
        nameAccuracy = (($coverResults | Where-Object { $_.success -and $_.validations.nameMatch } | Measure-Object).Count / ($coverResults | Where-Object { $_.success }).Count) * 100
        emailAccuracy = (($coverResults | Where-Object { $_.success -and $_.validations.emailMatch } | Measure-Object).Count / ($coverResults | Where-Object { $_.success }).Count) * 100
        phoneAccuracy = (($coverResults | Where-Object { $_.success -and $_.validations.phoneMatch } | Measure-Object).Count / ($coverResults | Where-Object { $_.success }).Count) * 100
        companyAccuracy = (($coverResults | Where-Object { $_.success -and $_.validations.companyMatch } | Measure-Object).Count / ($coverResults | Where-Object { $_.success }).Count) * 100
        positionAccuracy = (($coverResults | Where-Object { $_.success -and $_.validations.positionMatch } | Measure-Object).Count / ($coverResults | Where-Object { $_.success }).Count) * 100
        recipientAccuracy = (($coverResults | Where-Object { $_.success -and $_.validations.recipientMatch } | Measure-Object).Count / ($coverResults | Where-Object { $_.success }).Count) * 100
    }
}

Write-Host "✓ Analysis complete" -ForegroundColor Green

# Step 6: Generate report
Write-Host "`n[6/6] Generating comprehensive report..." -ForegroundColor Yellow

$report = @{
    testSummary = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        totalTestCases = $testCases.Count
        emailTests = @{
            total = $emailResults.Count
            successful = ($emailResults | Where-Object { $_.success }).Count
            failed = ($emailResults | Where-Object { -not $_.success }).Count
        }
        coverLetterTests = @{
            total = $coverResults.Count
            successful = ($coverResults | Where-Object { $_.success }).Count
            failed = ($coverResults | Where-Object { -not $_.success }).Count
        }
    }
    emailStats = $emailStats
    coverLetterStats = $coverStats
    emailResults = $emailResults
    coverLetterResults = $coverResults
    recommendations = @()
}

# Add recommendations
if ($emailStats.successRate -lt 100) {
    $report.recommendations += "Email generation: Investigate $($emailStats.totalGenerated - $emailResults.Count) failed cases"
}
if ($emailStats.extractionBreakdown.nameAccuracy -lt 90) {
    $report.recommendations += "Email metadata: Name extraction accuracy below 90%, review regex patterns"
}
if ($emailStats.extractionBreakdown.companyAccuracy -lt 90) {
    $report.recommendations += "Email metadata: Company extraction accuracy below 90%, expand pattern matching"
}
if ($coverStats.successRate -lt 100) {
    $report.recommendations += "Cover letter generation: Investigate $($coverResults.Count - ($coverResults | Where-Object { $_.success }).Count) failed cases"
}

# Save report
$report | ConvertTo-Json -Depth 10 | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "✓ Report saved to: $OutputFile" -ForegroundColor Green

# Display summary
Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           GENERATION TEST RESULTS SUMMARY                     ║" -ForegroundColor Cyan
Write-Host "╠════════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan

Write-Host "`n📧 EMAIL GENERATION:" -ForegroundColor Yellow
Write-Host "  Success Rate: $([Math]::Round($emailStats.successRate, 2))% ($($emailStats.totalGenerated) of 100)"
Write-Host "  Vietnamese: $($emailStats.vietnameseSuccess)/50, English: $($emailStats.englishSuccess)/50"
Write-Host "  Avg Extraction Accuracy: $([Math]::Round($emailStats.avgExtractionAccuracy, 2))%"
Write-Host "  Field Accuracy:"
Write-Host "    • Name: $([Math]::Round($emailStats.extractionBreakdown.nameAccuracy, 2))%"
Write-Host "    • Email: $([Math]::Round($emailStats.extractionBreakdown.emailAccuracy, 2))%"
Write-Host "    • Phone: $([Math]::Round($emailStats.extractionBreakdown.phoneAccuracy, 2))%"
Write-Host "    • Company: $([Math]::Round($emailStats.extractionBreakdown.companyAccuracy, 2))%"
Write-Host "    • Position: $([Math]::Round($emailStats.extractionBreakdown.positionAccuracy, 2))%"
Write-Host "    • Recipient: $([Math]::Round($emailStats.extractionBreakdown.recipientAccuracy, 2))%"

Write-Host "`n📝 COVER LETTER GENERATION:" -ForegroundColor Yellow
Write-Host "  Success Rate: $([Math]::Round($coverStats.successRate, 2))% ($($coverStats.totalGenerated) of 100)"
Write-Host "  Vietnamese: $($coverStats.vietnameseSuccess)/50, English: $($coverStats.englishSuccess)/50"
Write-Host "  Avg Extraction Accuracy: $([Math]::Round($coverStats.avgExtractionAccuracy, 2))%"
Write-Host "  Field Accuracy:"
Write-Host "    • Name: $([Math]::Round($coverStats.extractionBreakdown.nameAccuracy, 2))%"
Write-Host "    • Email: $([Math]::Round($coverStats.extractionBreakdown.emailAccuracy, 2))%"
Write-Host "    • Phone: $([Math]::Round($coverStats.extractionBreakdown.phoneAccuracy, 2))%"
Write-Host "    • Company: $([Math]::Round($coverStats.extractionBreakdown.companyAccuracy, 2))%"
Write-Host "    • Position: $([Math]::Round($coverStats.extractionBreakdown.positionAccuracy, 2))%"
Write-Host "    • Recipient: $([Math]::Round($coverStats.extractionBreakdown.recipientAccuracy, 2))%"

if ($report.recommendations.Count -gt 0) {
    Write-Host "`n⚠️  RECOMMENDATIONS:" -ForegroundColor Yellow
    foreach ($rec in $report.recommendations) {
        Write-Host "  • $rec" -ForegroundColor Gray
    }
}

Write-Host "`n╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "Test run completed! Detailed results saved to:" -ForegroundColor Green
Write-Host $OutputFile -ForegroundColor Cyan
