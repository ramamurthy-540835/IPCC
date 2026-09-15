#!/usr/bin/env python3
"""Build the presenter-script PDF for IPCC_AI_GCP_Overview_v3.0_Final.pptx."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether,
)

TEAL = HexColor("#0F6E6B")
DARK = HexColor("#1A2E35")
AMBER = HexColor("#B7791F")
GREY = HexColor("#5A6B73")
LIGHT = HexColor("#EEF4F4")

styles = getSampleStyleSheet()

title_st = ParagraphStyle("TitleBig", parent=styles["Title"], fontName="Helvetica-Bold",
                          fontSize=24, leading=30, textColor=DARK, alignment=TA_CENTER, spaceAfter=6)
subtitle_st = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica",
                             fontSize=12.5, leading=17, textColor=GREY, alignment=TA_CENTER, spaceAfter=4)
slide_head = ParagraphStyle("SlideHead", parent=styles["Heading1"], fontName="Helvetica-Bold",
                            fontSize=15.5, leading=20, textColor=TEAL, spaceBefore=2, spaceAfter=2)
slide_sub = ParagraphStyle("SlideSub", parent=styles["Normal"], fontName="Helvetica-Oblique",
                           fontSize=10.5, leading=14, textColor=GREY, spaceAfter=8)
sec_head = ParagraphStyle("SecHead", parent=styles["Heading3"], fontName="Helvetica-Bold",
                          fontSize=11, leading=14, textColor=AMBER, spaceBefore=8, spaceAfter=3)
body = ParagraphStyle("BodyTxt", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10.5, leading=15.5, textColor=DARK, spaceAfter=6, alignment=TA_LEFT)
script_body = ParagraphStyle("ScriptTxt", parent=body, leftIndent=6, spaceAfter=7)
bullet = ParagraphStyle("BulletTxt", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=4)
jargon = ParagraphStyle("JargonTxt", parent=body, leftIndent=14, spaceAfter=5)
tip = ParagraphStyle("TipTxt", parent=styles["Normal"], fontName="Helvetica-Oblique",
                     fontSize=10, leading=14, textColor=TEAL, spaceBefore=4, spaceAfter=2,
                     leftIndent=6)

story = []

# ---------------------------------------------------------------- cover page
story.append(Spacer(1, 45*mm))
story.append(Paragraph("Presenter Script &amp; Speaker Guide", title_st))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("IPCC Climate AI Assistant — GCP Overview", subtitle_st))
story.append(Paragraph("For the deck: <b>IPCC_AI_GCP_Overview_v3.0_Final.pptx</b> (13 slides)", subtitle_st))
story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="60%", thickness=1.2, color=TEAL, hAlign="CENTER"))
story.append(Spacer(1, 8*mm))
story.append(Paragraph(
    "This guide gives you, the presenter, a plain-English walkthrough of every slide: "
    "what is on the slide, a suggested word-for-word script you can adapt, and simple "
    "explanations of every technical term so you can answer questions with confidence. "
    "No prior knowledge of cloud computing or artificial intelligence is assumed.",
    ParagraphStyle("CoverBody", parent=body, alignment=TA_CENTER, fontSize=11, leading=17,
                   leftIndent=18*mm, rightIndent=18*mm)))
story.append(Spacer(1, 20*mm))
story.append(Paragraph("Prepared 30 August 2026 · Project ai-ippc · Region us-central1", subtitle_st))
story.append(PageBreak())

# ------------------------------------------------------------- how-to page
story.append(Paragraph("How to use this guide", slide_head))
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "Each slide gets its own section with four parts:", body))
story.append(Paragraph("• <b>What's on the slide</b> — a quick reminder of the visual, so you know what the audience is looking at.", bullet))
story.append(Paragraph("• <b>Suggested script</b> — full sentences you can speak as-is or adapt to your own voice. Read them once or twice beforehand; they are written to sound natural when spoken.", bullet))
story.append(Paragraph("• <b>Plain-English jargon guide</b> — every technical word on the slide, explained with everyday comparisons.", bullet))
story.append(Paragraph("• <b>Presenter tip</b> — timing, emphasis, or a likely audience question.", bullet))
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "<b>The one-line story of the whole deck:</b> the IPCC publishes the world's most trusted "
    "climate reports, but they are thousands of pages long and hard to search. We built an AI "
    "assistant on Google Cloud that lets anyone ask a question in plain language and get an "
    "answer in minutes — and every answer shows exactly which pages of which report it came "
    "from, so it can always be checked. It is already live, and there is a clear roadmap to make "
    "it enterprise-grade.", body))
story.append(Paragraph(
    "Suggested total timing: about 20 minutes of speaking for 13 slides (roughly 90 seconds per "
    "slide), leaving 10 minutes for questions in a 30-minute meeting.", body))
story.append(PageBreak())


def slide(num, title, deck_line, whats_on, script_paras, jargon_items, tip_text):
    parts = []
    parts.append(Paragraph(f"Slide {num} — {title}", slide_head))
    parts.append(Paragraph(f"Slide headline on screen: “{deck_line}”", slide_sub))
    parts.append(Paragraph("What's on the slide", sec_head))
    for w in whats_on:
        parts.append(Paragraph("• " + w, bullet))
    parts.append(Paragraph("Suggested script (speak this)", sec_head))
    for s in script_paras:
        parts.append(Paragraph("“" + s + "”", script_body))
    if jargon_items:
        parts.append(Paragraph("Plain-English jargon guide", sec_head))
        for term, expl in jargon_items:
            parts.append(Paragraph(f"<b>{term}</b> — {expl}", jargon))
    parts.append(Paragraph("Presenter tip", sec_head))
    parts.append(Paragraph(tip_text, tip))
    story.append(parts[0])
    for p in parts[1:]:
        story.append(p)
    story.append(PageBreak())


# ================================================================ SLIDE 1
slide(1, "Title — IPCC Climate AI Assistant",
      "IPCC CLIMATE AI ASSISTANT — a grounded AI assistant for exploring IPCC city and climate reports",
      [
        "The project title and a one-line description.",
        "Four headline numbers: 8 IPCC reports, 10,184 indexed passages, 5 workflows, and a LIVE badge saying it runs on Cloud Run.",
        "A footer confirming this was prepared from the real, deployed system (project “ai-ippc”, region “us-central1”), by Ramamurthy &amp; Monisha.",
      ],
      [
        "Good morning everyone. Today I'm presenting the IPCC Climate AI Assistant — a working system, not a concept. In plain terms: we took eight of the world's most authoritative climate reports, broke them into just over ten thousand searchable passages, and put an AI assistant in front of them so anyone can ask a question and get an evidence-backed answer in minutes.",
        "Two things I want you to hold onto from this first slide. First, the word “grounded” — every answer the assistant gives is anchored to actual text in the reports, and it shows you exactly where the answer came from. Second, the word “LIVE” — this is already deployed and running on Google Cloud today. Every number you'll see in this deck was read from the running system, not from a plan.",
      ],
      [
        ("IPCC", "The Intergovernmental Panel on Climate Change — a United Nations body where the world's climate scientists assess all published research and produce the definitive reports governments rely on. Think of it as the world's official 'referee' for climate science."),
        ("AI assistant", "A computer program you can talk to in normal language, like ChatGPT, but here it is restricted to answering only from the IPCC reports."),
        ("Grounded", "The assistant is not allowed to 'make things up'. Its answers are anchored (grounded) in actual passages from the reports, and it shows those passages as receipts."),
        ("Indexed passages", "We cut the reports into 10,184 bite-sized chunks of text and catalogued each one so the system can find the right chunk instantly — like a librarian who has read every page and remembers where everything is."),
        ("Cloud Run", "A Google Cloud service that hosts our application on the internet. Google manages the servers; we just supply the program. 'LIVE on Cloud Run' means the assistant is up and reachable right now."),
        ("Project ai-ippc / region us-central1", "In Google Cloud, a 'project' is like a named account folder holding everything we built; the 'region' is the physical data-centre location (here, central USA) where it runs."),
      ],
      "Keep this slide short — 45 seconds. Point at the LIVE badge and say 'this is running today'; that single fact sets this apart from most AI presentations.")

# ================================================================ SLIDE 2
slide(2, "What is IPCC?",
      "What is IPCC? The global evidence institution behind the knowledge library",
      [
        "Three cards: (1) 'An evidence institution', (2) 'A decision reference', (3) 'Not a policy oracle'.",
        "A closing line: the assistant improves access to evidence; it does not replace expert judgment.",
      ],
      [
        "Before the technology, let's be clear about whose knowledge we're working with. The IPCC — the Intergovernmental Panel on Climate Change — is the United Nations body that reviews and summarises all the world's published climate science. It doesn't do its own experiments; instead, hundreds of scientists volunteer to read everything that has been published — on climate impacts, risks, how to adapt, and how to reduce emissions — and distil it into reports the whole world can trust.",
        "Governments, researchers, city planners and educators all use these reports as their shared, credible reference point. When a city justifies a flood-defence budget, the IPCC is often the evidence base behind it.",
        "One honest caveat, and it's on the slide deliberately: the IPCC is not a policy oracle. Its evidence is global and high-level. A real decision still needs local data, engineering work, legal review and community input. Our assistant follows the same philosophy — it makes the evidence dramatically easier to reach, but it never replaces expert judgment.",
      ],
      [
        ("Assess / synthesize", "The IPCC doesn't run new experiments; it reads thousands of already-published studies and combines them into one balanced summary — like a judge weighing all testimony rather than a witness giving new testimony."),
        ("Adaptation", "Adjusting to climate change that is already happening — e.g., building sea walls, planting heat-resistant trees, redesigning drainage."),
        ("Mitigation", "Reducing the cause of climate change — cutting greenhouse-gas emissions, e.g., switching to clean energy."),
        ("Policy oracle", "Our phrase for a magic box that tells you what decision to make. The IPCC (and our assistant) is explicitly NOT that — it informs decisions, it doesn't make them."),
      ],
      "The 'not a policy oracle' card is your credibility builder with executives — it shows the team understands the limits of AI. Slow down when you deliver that caveat.")

# ================================================================ SLIDE 3
slide(3, "Why cities? The pressure point",
      "Cities feel climate change first and decide under pressure",
      [
        "Three numbered 'realities': the city reality (compounding physical impacts), the information reality (evidence scattered in long reports), the leadership reality (different people need different depth).",
        "A strategic-opportunity strip: Question → Evidence → Informed action.",
      ],
      [
        "Why did we focus on cities? Because cities are where climate change gets real first. Heatwaves, flooding, water shortages, infrastructure failures and health impacts don't arrive one at a time — they pile on top of each other, and they don't hit everyone equally. City leaders have to make decisions under time pressure, in full public view.",
        "Now the second reality: the evidence those leaders need does exist — but it's scattered across reports that run to thousands of pages, written in dense scientific language, split across chapters and annexes. Every hour spent hunting for the right paragraph is an hour of decision delay.",
        "And the third reality: different people need different depth. An executive wants the two-sentence implication. A practitioner wants the technical detail. And everyone needs a way to trace the answer back to the original source when it's challenged.",
        "So the opportunity is simple to state: shrink the distance between a question, the evidence, and informed action. That path — question to evidence to action — is exactly what this platform compresses from weeks to minutes.",
      ],
      [
        ("Water stress", "When demand for water gets close to, or exceeds, the reliable supply — droughts, shrinking reservoirs, competition between homes, farms and industry."),
        ("Exposure is unequal", "Poorer neighbourhoods often sit in hotter, lower-lying, or more flood-prone areas with less protection — so the same storm hurts some communities far more than others."),
        ("Annexes", "The appendices at the back of a scientific report — glossaries, data tables, methods. Important details often hide there, which makes manual searching even harder."),
      ],
      "This is your 'why should anyone care' slide. The strongest line is in the speaker notes: the bottleneck is not evidence — it's the time between a question and a defensible answer. Say it verbatim.")

# ================================================================ SLIDE 4
slide(4, "The problem and the shift",
      "Authoritative evidence, locked in thousands of pages",
      [
        "A before/after comparison. Left (✕, today): weeks of searching, deep expertise needed just to find a passage, answers hard to trace.",
        "Right (✓, with the assistant): minutes to a plain-language answer, anyone can ask, every answer cites its passages and links the original PDF.",
        "Bottom strip — the operating principle: Retrieve evidence → Generate explanation → Show sources.",
      ],
      [
        "This slide is the heart of the business case. On the left is today's reality: getting an answer out of the IPCC library is manual research. It takes weeks of searching across chapters and working groups. You need deep domain expertise just to know where to look. And when you finally have an answer, it's hard to show your working — hard to trace it back to a defensible source.",
        "On the right is the same task with the assistant: minutes instead of weeks. A clear answer in plain language. And crucially — anyone can ask. A city planner, a student, a policy team. No PhD required to reach PhD-grade evidence.",
        "The third tick on the right is the one I'd underline for this audience: every answer cites the exact passages it used and links back to the original PDF. Speed without losing rigour.",
        "How does it stay honest? The operating principle at the bottom: the system first retrieves real evidence from the reports, then generates a plain-language explanation from that evidence, then shows its sources. Find first, explain second, prove always. That ordering is what makes this trustworthy.",
      ],
      [
        ("Working groups", "The IPCC splits its work into three big teams: Working Group I (the physical science — what's happening), Working Group II (impacts and adaptation — what it means for people), and Working Group III (mitigation — what we can do about it). Each produces its own enormous report."),
        ("Cites its passages", "Just like footnotes in an essay: the answer lists the exact text snippets it was based on, so anyone can verify it."),
        ("Retrieve → Generate → Show sources", "The three-step recipe: (1) fetch the most relevant real paragraphs from the reports, (2) have the AI write an answer using only those paragraphs, (3) display those paragraphs alongside the answer as proof."),
      ],
      "Physically gesture left ('weeks') then right ('minutes'). If you get one applause line in this deck, it's 'weeks to minutes — and rigour survives because every answer shows its sources.'")

# ================================================================ SLIDE 5
slide(5, "Why the IPCC itself needs AI",
      "Why the IPCC needs AI: evidence grows faster than any author team",
      [
        "Four big numbers from a single report cycle: 34,000+ papers assessed, 270 authors, 67 countries, 18 chapters.",
        "The 'AR7 twin challenge': more volume (literature growing faster than teams can read) and more blind spots (regions/topics with little published English literature).",
        "What AI must deliver, per the SIGIR/MANILA24 research agenda: traceable synthesis, multilingual and grey literature, bias mitigation, multi-modal retrieval.",
      ],
      [
        "You might ask: is AI here just because AI is fashionable? No — and this slide is the proof. Look at the scale of one single IPCC report: over thirty-four thousand scientific papers assessed by two hundred and seventy authors from sixty-seven countries, condensed into eighteen chapters. That is close to the limit of what human teams can do.",
        "And the next report cycle — called AR7 — faces a twin challenge. First, volume: climate research is being published faster than any author team can read it. Second, blind spots: some of the most climate-vulnerable regions publish little research in English, so their evidence risks being invisible.",
        "The international research community has already defined what AI must deliver here. At a dedicated workshop — MANILA24, run by SIGIR, the leading information-retrieval research body — they set the agenda: every AI-assisted claim must carry its source; systems must handle multiple languages and so-called grey literature; they must actively counter geographic bias; and eventually they must handle not just text but data, maps and community knowledge.",
        "The point for us: our platform already implements the first and most important principle on that list — retrieval with citations. We're not improvising; we're building on the research community's own roadmap.",
      ],
      [
        ("AR6 / AR7", "IPCC reports come in numbered cycles: 'Assessment Report 6' (AR6) is the latest completed one; AR7 is the cycle now beginning. Each cycle takes five to seven years."),
        ("SIGIR", "The world's leading academic community for 'information retrieval' — the science behind search engines. When they publish a research agenda, it's the search-technology equivalent of a medical body publishing treatment guidelines."),
        ("MANILA24", "A 2024 SIGIR workshop (held in Manila) specifically about how AI and search technology should support IPCC-style evidence work. Our design choices follow its recommendations."),
        ("Grey literature", "Valuable documents that aren't formal academic papers — government reports, city planning documents, NGO studies. Often the only written evidence for developing regions, so ignoring it creates blind spots."),
        ("Bias mitigation", "Actively correcting the tilt that happens when most published science comes from wealthy, English-speaking countries — so the picture isn't skewed against data-poor regions."),
        ("Multi-modal retrieval", "Searching across more than text: also data tables, maps, images. 'Modes' just means types of content."),
        ("Traceable evidence synthesis", "Combining many sources into one summary in a way where every sentence can be traced back to the source it came from."),
      ],
      "Let the 34,000 number breathe — pause after saying it. This slide reframes the project from 'nice tool' to 'necessary infrastructure for science itself'.")

# ================================================================ SLIDE 6
slide(6, "How an IPCC report is made (and why that matters)",
      "The five-to-seven-year lifecycle behind every IPCC report",
      [
        "A 10-step timeline: Scope → Select authors → Assess evidence → First draft → Expert review → Government review → Final draft → Endorsement → Publication → Synthesis.",
        "Grouped into five phases: Define, Assess &amp; Draft, Review &amp; Refine, Approve &amp; Publish, Synthesize.",
        "Source citations at the bottom (official IPCC procedure documents).",
      ],
      [
        "Why should you trust answers that come out of our assistant? Because of what goes INTO it. This slide shows the journey every report in our library survived — a five-to-seven-year quality gauntlet.",
        "Walking through it quickly: governments first agree the scope — the outline, schedule and budget. The IPCC then selects balanced author teams from around the world. Those authors assess only already-published literature — the IPCC does no new research, it weighs existing evidence. They write a first draft, which goes through expert review where every single comment must be answered on the record — tens of thousands of comments. Then a second draft goes to government review, along with the Summary for Policymakers. After a final draft, comes the remarkable part: at a plenary session, government delegates approve that summary line by line — every sentence negotiated and agreed by the world's governments. Then everything is published — including all the review comments and responses. Finally the working groups are combined into a synthesis report, and the next cycle begins.",
        "So when our assistant quotes a passage, that passage survived two rounds of on-the-record review and, for the summaries, word-by-word sign-off by governments worldwide. That is why grounding answers in this corpus makes them defensible in a boardroom or a council chamber.",
      ],
      [
        ("Scoping", "The 'define the project' phase: governments agree what the report will cover, when, and at what cost — before any writing starts."),
        ("The Bureau", "The IPCC's elected leadership committee of senior scientists, which picks author teams balanced across countries, disciplines and gender."),
        ("Summary for Policymakers (SPM)", "A short, plain-language executive summary at the front of each giant report — the part ministers and CEOs actually read, and the part governments approve line by line."),
        ("Plenary / Endorsement", "The full assembly of all ~195 member governments. 'Line-by-line approval' means delegates literally project each sentence and negotiate until everyone accepts it."),
        ("On the record", "Every reviewer comment and every author response is published for anyone to inspect — radical transparency."),
        ("Corpus", "Simply 'the body of documents' — our collection of eight IPCC reports. You'll hear this word again; it just means 'the library'."),
        ("Synthesis Report", "The final capstone that merges all three working-group reports into one integrated picture."),
      ],
      "Don't read all 10 steps — sweep your hand across the timeline and land on step 8: 'governments approve the summary line by line'. That detail always lands with executives.")

# ================================================================ SLIDE 7
slide(7, "Five workflows, one conversation",
      "One assistant, five ways to work with climate reports",
      [
        "Five workflow cards around a central 'IPCC AI Assistant' hub: Ask, Browse, Summarize, Review, Improve.",
        "Footer: the research journey (Discover → Understand → Verify → Communicate), built with Python services on Cloud Run, intelligence from Vertex AI.",
      ],
      [
        "So what can you actually do with it? Five things — all inside one simple chat conversation, with no new tools to learn and no training curve.",
        "One: Ask. Type a question in plain language and get a sourced answer. This is smart search — it understands what you mean, not just the words you typed. Two: Browse. Open or download the original report PDFs directly, when you want the primary document itself. Three: Summarize. Ask for a digest of an entire report on demand — the two-page version of the two-hundred-page document. Four: Review. Hand it a document — say, a draft city climate plan — and it critiques it against the IPCC evidence. Five: Improve. It suggests clearer, stronger wording for your own climate-related content.",
        "Together these cover the full research journey: discover what's relevant, understand it, verify it against sources, and communicate it. And notice the pattern — five different jobs, one interface, one trusted library underneath. This is not a search box; it's a research colleague.",
      ],
      [
        ("Semantic search", "Search by meaning, not by exact words. Ask 'how will rising heat affect older people in cities?' and it finds passages about 'elderly urban populations and heatwave mortality' even though none of your words match. Ordinary keyword search can't do that."),
        ("Workflow", "Just a fancy word for 'a way of working' or 'a type of task' — here, the five task types the assistant supports."),
        ("Python services", "Python is the programming language our application is written in; a 'service' is a program that runs continuously waiting to serve users."),
        ("Vertex AI", "Google Cloud's umbrella platform for artificial-intelligence services — the 'brain shop' we rent AI capabilities from instead of building our own models."),
        ("Training curve", "The learning effort a new tool demands. Because this is just a chat window, that effort is near zero."),
      ],
      "Demo opportunity: if you have a live connection, this is the natural slide to switch to the real assistant for 60 seconds. If not, describe the 'Ask' example concretely — a real question and its cited answer.")

# ================================================================ SLIDE 8
slide(8, "How a question becomes an answer (RAG)",
      "End-to-end RAG workflow — how a user question becomes an evidence-based answer",
      [
        "A five-step pipeline: 1 Question → 2 Embed (Vertex AI turns the question into a vector) → 3 Retrieve (BigQuery returns closest chunks) → 4 Generate (Gemini writes the response) → 5 Cite (UI shows answer + sources).",
        "Footer: retrieval grounds the answer in IPCC content and reduces unsupported generation.",
      ],
      [
        "Now let's open the hood — gently. The technique we use is called RAG: Retrieval-Augmented Generation. The name sounds technical, but the idea is something we all learned in school: it's an open-book exam. Instead of letting the AI answer from memory — where it might misremember — we make it look up the relevant pages first and answer only from what it found.",
        "Five steps. Step one: you ask a question in plain language. Step two, 'embed': the system converts your question into a list of numbers that captures its meaning — think of it as a GPS coordinate for ideas, where similar meanings sit close together. Step three, 'retrieve': the database compares your question's coordinates against all 10,184 report passages and pulls back the handful that sit closest — the most relevant evidence. Step four, 'generate': Gemini, Google's AI language model, writes a clear answer using those retrieved passages as its only source material. Step five, 'cite': the screen shows the answer together with the passages it was built from.",
        "Why this design? The line at the bottom says it: retrieval grounds the answer in real IPCC content and reduces unsupported generation — the industry's polite phrase for the AI making things up. Open book beats closed book.",
      ],
      [
        ("RAG (Retrieval-Augmented Generation)", "The open-book-exam technique: fetch real documents first, then have the AI write its answer from them. 'Retrieval' = the looking-up; 'generation' = the writing; 'augmented' = the writing is boosted by the lookup."),
        ("Embed / Embedding / Vector", "Converting text into a long list of numbers that represents its meaning — like giving every sentence a map coordinate, where sentences about the same topic land near each other. 'Vector' is just the maths word for that list of numbers."),
        ("Chunks", "The bite-sized passages (a few paragraphs each) we split the reports into. Retrieving whole 3,000-page reports would be useless; retrieving the exact relevant paragraph is gold."),
        ("BigQuery", "Google Cloud's heavy-duty database, able to search enormous amounts of data in seconds. Here it stores all passages and their 'meaning coordinates' and finds the nearest matches."),
        ("Gemini", "Google's flagship AI language model — the same family of technology as ChatGPT, made by Google. It does the 'writing' step."),
        ("Unsupported generation / hallucination", "When an AI confidently states something not backed by any source. Our retrieve-first design is the main defence against it."),
        ("UI", "User interface — simply the screen the user sees."),
      ],
      "Use the open-book exam analogy out loud — it converts this slide from intimidating to obvious. If pressed on 'can it still hallucinate?', the honest answer: the risk is greatly reduced, never zero, which is exactly why every answer carries its sources for checking.")

# ================================================================ SLIDE 9
slide(9, "The architecture on Google Cloud",
      "GCP solution architecture — managed services separate storage, retrieval, intelligence and presentation",
      [
        "A component diagram: IPCC PDFs → Cloud Storage → BigQuery Documents → BigQuery Vector Search, with Vertex AI Embeddings and Gemini Flash feeding in, and Cloud Run hosting the application.",
        "Footer describing two paths — offline pipeline (upload → extract/chunk → embed → index) and online path (question → retrieve top-k chunks → generate answer).",
      ],
      [
        "Here's the same system drawn as a map of its parts — all standard Google Cloud building blocks. Let me translate each box. Cloud Storage is the filing cabinet: it holds the original PDF reports, untouched. BigQuery is the card catalogue: it holds the ten thousand extracted passages, and its vector-search feature is what finds the passages closest in meaning to your question. Vertex AI Embeddings is the translator that turns text into those meaning-coordinates. Gemini Flash is the writer that drafts the final answer. And Cloud Run is the storefront — the web application users actually visit.",
        "Notice there are two journeys through this map. The offline pipeline runs once per document, behind the scenes: upload the PDF, extract and chunk the text, compute the embeddings, build the index. Think of it as the librarian cataloguing a new book before it goes on the shelf. The online path runs every time someone asks a question: take the question, retrieve the top matching chunks, generate the answer. Cataloguing versus serving readers.",
        "One strategic point: every box is a managed service. Google runs the servers, the patching, the scaling. Our team wrote no infrastructure — only the application logic. That means low operational burden and costs that scale with actual use.",
      ],
      [
        ("GCP", "Google Cloud Platform — Google's rent-a-datacentre offering, the same league as Amazon's AWS and Microsoft's Azure."),
        ("Managed service", "A cloud building block Google operates for you — like renting a serviced office instead of building and maintaining your own. No servers to buy, patch or repair."),
        ("Cloud Storage", "A limitless online filing cabinet for raw files — here, the original PDFs (about 73 MB in total)."),
        ("Vector search", "The 'find the nearest meaning' search: given the coordinates of your question, instantly find the stored passages with the closest coordinates. This is what powers search-by-meaning."),
        ("Top-k chunks", "The 'k' best-matching passages — e.g., the top 5 or top 10. A tunable knob for how much evidence the AI gets per question."),
        ("Gemini Flash", "The 'Flash' variant of Gemini is tuned for speed and low cost — right for interactive chat, where users expect answers in seconds."),
        ("Offline vs online", "Offline = preparation work done in advance, no user waiting. Online = the live path a user's question travels, where speed matters."),
        ("Index", "The pre-built lookup structure that makes searching instant — like a book's index page, built once so every later lookup is fast."),
      ],
      "Don't read every box — walk the two journeys instead (the librarian's cataloguing path, then the reader's question path). The 'no servers to manage' point is the CFO-friendly takeaway.")

# ================================================================ SLIDE 10
slide(10, "The three-layer platform view",
      "A three-layer platform: knowledge, intelligence, experience",
      [
        "The same system re-organised into three horizontal layers. Bottom — Knowledge (Cloud Storage with 8 PDFs ≈73 MiB; BigQuery with 10,184 passages). Middle — Intelligence (Vertex AI Embeddings text-embedding-005, BigQuery Vector Search, Gemini Flash). Top — Experience (Cloud Run public endpoint, 1 warm instance, 100% traffic).",
        "Two labelled flows: an offline Knowledge Pipeline (upload → chunk → embed → index) and a live Question Journey (ask → retrieve → answer).",
      ],
      [
        "This slide says the same thing as the previous one, but in the way I'd ask you to remember it — three layers, read bottom-up. At the bottom, Knowledge: where the evidence lives. The eight source PDFs in Cloud Storage and the 10,184 extracted passages in BigQuery. In the middle, Intelligence: where meaning is made. The embedding model that understands text, the vector search that finds relevant evidence, and Gemini that writes grounded answers. At the top, Experience: where people work — the public web application on Cloud Run, kept 'warm' so the first user of the day isn't kept waiting.",
        "The two arrows are the two rhythms of the system: the amber one is the offline knowledge pipeline — how a new report gets ingested: upload, chunk, embed, index. The teal one is the live question journey every user triggers: ask, retrieve, answer.",
        "Why does the layering matter to leadership? Separation of concerns. We can swap in a better AI model in the middle layer without touching the data. We can add new reports at the bottom without touching the app. Nothing to patch, and every layer scales on its own. That's what makes this a platform rather than a one-off tool.",
      ],
      [
        ("text-embedding-005", "The specific Google model that converts text into meaning-coordinates — version 005. Knowing the exact model name matters for reproducibility and upgrades."),
        ("Public endpoint", "An internet address anyone can reach — the front door of the application."),
        ("Warm instance", "One copy of the app is kept running at all times, so there's no cold-start delay for the first visitor — like keeping the engine idling instead of starting from cold."),
        ("100% traffic", "Cloud Run can split visitors between old and new versions during upgrades; '100% on latest' means everyone is served by the newest release — no half-finished rollout."),
        ("MiB", "Mebibyte — for everyday purposes, a megabyte. 73 MiB is small: the entire evidence base fits in less space than a few phone videos."),
        ("Separation of concerns", "Engineering principle: keep storage, thinking and presentation independent, so you can upgrade one without breaking the others — like separate plumbing and wiring in a building."),
      ],
      "Physically gesture bottom-to-top: 'evidence lives here, meaning is made here, people work here.' That nine-word tour is the most memorable summary of the whole architecture.")

# ================================================================ SLIDE 11
slide(11, "Where it stands today — verified, live",
      "Live and verified in project ai-ippc — every figure read from the deployed environment, not from a plan",
      [
        "Four status cards: SERVICE (Cloud Run, revision 00007-lfs, 100% traffic, 1 warm instance, HTTP 200 verified), CORPUS (8 reports, ≈73 MiB in bucket ipcc-srcities-bucket-1), INDEX (10,184 passages embedded in BigQuery dataset climate_ai), MODELS (Gemini Flash preview + text-embedding-005 in us-central1).",
        "A coverage bar: 10,184 / 10,184 passages embedded — 100%.",
      ],
      [
        "This is the accountability slide — the difference between a proposal and a product. Every number here was read from the running system on the day this deck was prepared.",
        "Four checks. The service: the application is live on Cloud Run, on its seventh revision, serving one hundred percent of traffic, and the public address answers with HTTP 200 — the web's standard 'all is well' signal. The corpus: all eight IPCC reports are online in Cloud Storage, about 73 megabytes of source PDFs. The index: all 10,184 passages are stored and embedded in BigQuery. The models: two Vertex AI models — Gemini Flash for writing and text-embedding-005 for understanding — both running in the us-central1 region.",
        "And the bar at the bottom is the number I'm proudest of: 10,184 out of 10,184 — one hundred percent index coverage. Every single stored passage is searchable. No silent gaps, no 'we'll finish indexing later'. When the assistant says it searched the corpus, it searched all of it.",
      ],
      [
        ("HTTP 200", "The standard 'success' code a website returns when it's working. 'HTTP 200 verified' means we called the live address and it answered healthily — the web equivalent of a dial tone."),
        ("Revision 00007-lfs", "Each deployment of the app gets a numbered version; we're on the seventh. Evidence of a real, iterated system rather than a first attempt."),
        ("Bucket", "Cloud Storage's word for a top-level folder. 'ipcc-srcities-bucket-1' is simply the named folder holding our PDFs."),
        ("Dataset (climate_ai)", "BigQuery's word for a named collection of data tables — ours is called 'climate_ai'."),
        ("Embedded", "A passage is 'embedded' once its meaning-coordinates have been computed and stored — i.e., it has been made findable by meaning."),
        ("Preview (model status)", "Google's label for a model that is available but not yet in final general release — cutting-edge, with the small caveat that Google may still evolve it."),
        ("1:1 / 100% coverage", "Every passage stored equals a passage indexed — the search space has no blind spots."),
      ],
      "Deliver this slide with quiet confidence — short sentences, let the numbers work. If asked 'what did this cost?', the honest frame: a small always-on footprint (one warm instance, 73 MB of storage) with pay-per-use AI calls — follow up with exact figures after the meeting.")

# ================================================================ SLIDE 12
slide(12, "Future state — the Enterprise Knowledge Fabric",
      "An Enterprise Knowledge Fabric with reasoning agents",
      [
        "A seven-layer stack. Marked TODAY: L1 Sources &amp; Ingestion, L2 Storage &amp; Processing, L3 Experience &amp; Governance, L4 Semantic Enrichment. Marked NEW: L5 Ontology Layer (shared climate vocabulary), L6 Enterprise Context Graph (entities, relationships, lineage). Marked EVOLVED: L7 Consumption &amp; Reasoning — agents.",
        "A 'what changes' panel: reason over meaning; lineage by default; connect once, reuse everywhere. A 'value flows up' arrow.",
      ],
      [
        "Where does this go next? The headline: the future is not a bigger AI model — it's smarter knowledge. This slide shows the platform evolving into what we call an Enterprise Knowledge Fabric: a seven-layer stack, where value flows from the bottom up.",
        "The good news first: most of it already exists. Layers one to four are running today — sources and ingestion, storage and processing, the experience layer, and semantic enrichment, which is the chunking and embedding work you've already seen.",
        "Two layers are new. Layer five is an ontology — an agreed vocabulary of climate concepts: hazards, sectors, regions, measures. It's the system's dictionary, so 'flood risk', 'coastal inundation' and 'storm surge' are understood as related concepts, not just similar-looking words. Layer six is an enterprise context graph — a living map of things and their relationships: this city faces this hazard, addressed by this measure, evidenced by this report chapter — with full lineage, meaning every fact remembers where it came from.",
        "With those in place, layer seven evolves: instead of one chat assistant, we run specialised AI agents — a research agent, a synthesis agent, a review agent, a governance agent — that reason over the map of meaning rather than just matching similar text.",
        "Three things change for the business, on the right. First, agents reason over meaning — entities and relationships, not just lookalike paragraphs. Second, lineage by default — every claim traces through the graph back to a governed source; auditability is built in, not bolted on. Third, connect once, reuse everywhere — plug in a new source, like city data or multilingual reports, and every agent benefits instantly. That's the economics of a platform: each addition multiplies value instead of adding a silo.",
      ],
      [
        ("Knowledge fabric", "An architecture where all knowledge sources are woven into one connected, consistently governed layer that any application can draw on — a fabric, not a pile of separate silos."),
        ("Ontology", "A formal, agreed vocabulary of concepts and how they relate — the system's official dictionary and family tree of climate terms (hazards, sectors, regions, measures)."),
        ("Context graph / knowledge graph", "A database shaped like a network: dots are things (a city, a hazard, a policy), lines are relationships ('is threatened by', 'is addressed by'). Lets the system answer 'how are these connected?', not just 'what text looks similar?'"),
        ("Entities", "The 'things' the system knows about — cities, hazards, sectors, measures — as concepts, not just words on a page."),
        ("Lineage", "The recorded ancestry of every piece of information — which document, which version, which transformation. The audit trail that makes claims defensible."),
        ("Agents", "AI programs given a role and the ability to carry out multi-step tasks on their own — like specialised junior analysts (one researches, one summarises, one reviews) rather than a single Q&amp;A chat."),
        ("Governed source", "A source that has passed through controlled onboarding — approved, versioned, access-controlled — as opposed to anything scraped off the internet."),
        ("Semantic enrichment", "Adding layers of meaning to raw text: splitting it into chunks, computing embeddings, tagging the entities mentioned."),
      ],
      "This is the investment-ask slide, so keep the framing disciplined: 'we add two layers to a fabric we already run' — evolution, not rebuild. The 'connect once, reuse everywhere' line is the ROI argument; make eye contact when you deliver it.")

# ================================================================ SLIDE 13
slide(13, "The takeaway and the ask",
      "Make evidence easier to use — without losing the ability to verify it",
      [
        "One promise line, one summary sentence: IPCC Climate AI turns a hard-to-navigate report library into a governed, source-grounded research conversation — and the knowledge fabric makes it enterprise-ready.",
        "Three closing words: DISCOVER · VERIFY · ACT. Footer: CEO/CIO briefing, v3.0.",
      ],
      [
        "Let me land this in one sentence: we make evidence easier to use without losing the ability to verify it. That balance is the entire project. Plenty of AI tools are fast; very few can show their receipts. Ours always does.",
        "What you've seen today: a live, verified system on Google Cloud that turns a hard-to-navigate report library into a research conversation — grounded in sources, governed end to end. And a credible next step — the knowledge fabric — that takes it from a strong tool to enterprise infrastructure.",
        "Three words to leave with: Discover — anyone can find the evidence in minutes. Verify — every answer can be traced to its source. Act — decisions get made faster, and they stand up to scrutiny.",
        "And the specific ask today: first, endorse the pilot success gates — the quality, security and cost criteria the pilot must meet; and second, support the knowledge-fabric investment for the future state. The system is live; the question is how far we take it. Thank you — I'm happy to take questions.",
      ],
      [
        ("Governed", "Operated under defined controls — who can access it, which sources are approved, how changes are tracked. The opposite of an unmanaged experiment."),
        ("Enterprise-ready", "Fit for serious organisational use: secure, auditable, scalable and supportable — not just a demo that works on a good day."),
        ("Pilot gates", "Pre-agreed pass/fail criteria a trial must meet before wider rollout — e.g., answer-quality thresholds, a security review, and cost-per-query limits. Gates protect the organisation from scaling something unproven."),
      ],
      "End on the three words — Discover, Verify, Act — then stop talking. Resist adding 'so yeah…' after the ask; silence lets the ask register. Likely first question: 'what would the fabric cost?' Have a range ready or commit to a follow-up date.")

# ------------------------------------------------------------- glossary page
story.append(Paragraph("Quick-reference glossary (one line each)", slide_head))
story.append(Paragraph("Keep this page beside you during Q&amp;A.", slide_sub))
gloss = [
    ("IPCC", "UN body that reviews all climate science and publishes the world's reference reports."),
    ("Corpus", "Our library: the 8 IPCC reports the assistant answers from."),
    ("Chunk / passage", "A bite-sized excerpt of a report; we have 10,184 of them."),
    ("Embedding / vector", "A text's 'meaning coordinates' — numbers that let us search by meaning."),
    ("Vector search", "Finding the stored passages whose meaning sits closest to the question."),
    ("RAG", "Open-book exam for AI: retrieve real passages first, write the answer from them, show sources."),
    ("Hallucination", "An AI stating something unsupported by any source; RAG plus citations is our defence."),
    ("GCP", "Google Cloud Platform — the rented, Google-managed infrastructure everything runs on."),
    ("Cloud Storage", "Filing cabinet for the original PDFs."),
    ("BigQuery", "Heavy-duty database holding passages and doing the vector search."),
    ("Vertex AI", "Google's AI service platform; supplies our two models."),
    ("Gemini Flash", "Google's fast, cost-efficient AI writing model."),
    ("text-embedding-005", "The Google model that computes meaning-coordinates."),
    ("Cloud Run", "The managed hosting service that serves the web application."),
    ("HTTP 200", "The web's 'everything is fine' response code."),
    ("Warm instance", "A copy of the app kept running so no user waits for start-up."),
    ("Ontology", "The agreed dictionary of climate concepts (future layer 5)."),
    ("Context graph", "The map of entities and relationships with full lineage (future layer 6)."),
    ("Lineage", "The recorded ancestry of every fact — its audit trail."),
    ("Agents", "Role-specialised AIs that carry out multi-step research tasks (future layer 7)."),
    ("Grey literature", "Non-academic but valuable documents: government, city and NGO reports."),
    ("Pilot gates", "Pre-agreed quality, security and cost criteria before scaling up."),
]
rows = [[Paragraph(f"<b>{t}</b>", body), Paragraph(d, body)] for t, d in gloss]
tbl = Table(rows, colWidths=[42*mm, 128*mm])
tbl.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [None, LIGHT]),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tbl)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(20*mm, 12*mm, "IPCC Climate AI Assistant — Presenter Script (v3.0 deck)")
    canvas.drawRightString(190*mm, 12*mm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    "/home/appadmin/GCP-Studio/IPCC/IPCC_AI_GCP_Overview_v3.0_Presenter_Script.pdf",
    pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=20*mm,
    title="IPCC Climate AI Assistant — Presenter Script",
    author="Ramamurthy & Monisha",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF written.")
