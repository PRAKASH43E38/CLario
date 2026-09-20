You are the Principal Software Architect, Senior Full-Stack Engineer, AI
Systems Engineer, UX Engineer, Database Architect, and QA Engineer
responsible for building the complete CLARIO application.

Your task is NOT to create a mockup, static prototype, landing page, or
disconnected frontend.

Your task is to DESIGN, IMPLEMENT, CONNECT, TEST, DEBUG, and VERIFY the
complete working CLARIO product.

============================================================ 1. PROJECT
IDENTITY ============================================================

Product Name: CLARIO

Core Promise:

“Come confused. Leave with clarity.”

CLARIO is a personalized, adaptive, interactive, and gamified AI
learning platform.

The primary outcome is:

CONCEPTUAL CLARITY

Do NOT claim guaranteed mastery.

The student’s desired feeling is:

“I came here confused, and now it actually clicks.”

CLARIO must dynamically adapt to the individual learner instead of
forcing every learner through a predefined course structure.

The student must experience CLARIO as ONE intelligent learning system.

Internally, CLARIO uses one Main Agentic AI / Main Orchestrator that
controls six specialized AI agents.

The six agents must NEVER appear to the student as six separate chatbots
or separate products.

============================================================ 2.
NON-NEGOTIABLE PRODUCT PRINCIPLES
============================================================

1.  CLARIO is dynamic, not a fixed course/LMS system.
2.  Conceptual clarity is more important than lesson completion.
3.  Actual learner behavior continuously improves personalization.
4.  The five onboarding mindset questions create only an initial learner
    hypothesis, NOT a permanent learning-style classification.
5.  Session context must influence the current learning journey.
6.  Previous learning history must influence future personalization.
7.  The roadmap is dynamic and can change during learning.
8.  Every important UI action must connect to real application logic.
9.  Do not fake AI behavior when real implementation is required.
10. Do not hardcode a fake learning journey as the final implementation.
11. Avoid unnecessary dependencies and infrastructure.
12. Keep the architecture lightweight, modular, readable, and scalable.
13. Every component must have a clear responsibility.
14. Use typed contracts between frontend, backend, and AI systems.
15. Validate all external/user/LLM data.
16. Handle failures gracefully.
17. Build the application incrementally and verify each phase.
18. Never silently ignore implementation errors.
19. Never leave broken placeholder functionality while claiming the
    feature is complete.
20. If something cannot be implemented immediately, isolate it clearly
    rather than pretending it works.

============================================================ 3. FINAL
TECHNOLOGY STACK
============================================================

FRONTEND - React - TypeScript - Tailwind CSS

Do NOT add: - TanStack Query - Zustand - unnecessary global state
libraries - unnecessary UI frameworks

BACKEND - Python - FastAPI - Pydantic - SQLAlchemy - MySQL

AI - Python - LangChain - LangGraph - Pydantic structured outputs - LLM
provider abstraction - LangSmith for observability

LLM PROVIDERS Primary: - Gemini

Fallback: - Groq

Second fallback: - OpenRouter

Provider architecture must be abstracted so application logic does not
depend directly on one provider.

WEB RESEARCH - Tavily

REAL-TIME - Server-Sent Events (SSE) - LangGraph streaming where
appropriate

DATABASE - MySQL only

Do NOT introduce: - Redis - Qdrant - Pinecone - vector database -
Kafka - unnecessary microservices - unnecessary message queues

============================================================ 4.
HIGH-LEVEL ARCHITECTURE
============================================================

                    CLARIO
                       |
                React Frontend
                       |
                    FastAPI
                       |
              Main Agentic AI
                 /    |    \
                /     |     \
             LangGraph Workflow
                |
    ---------------------------------
    |       |       |      |      |

Nova Mira Ayan Kira Zayn Elara ——————————— | Learner Model | MySQL

Research: Nova → Tavily → web results → clean/structure → relevant
context

Persistent memory: MySQL

Session/workflow state: LangGraph

Streaming: FastAPI SSE ← LangGraph streaming

Observability: LangSmith

============================================================ 5. SIX
SPECIALIZED AGENTS
============================================================

  -----------------------
  NOVA — Research Agent
  -----------------------

Purpose: Research current/relevant external information.

Responsibilities: - web research - retrieve relevant information - use
Tavily - clean noisy web content - extract useful information -
structure research findings - provide only relevant context to
downstream agents

Nova must not dump raw webpages into prompts.

Flow:

User need → Research decision → Crawl/search → Extract → Clean →
Structure → Relevant context → Main Orchestrator

  -----------------------
  MIRA — Teaching Agent
  -----------------------

Purpose: Explain concepts simply and adaptively.

Responsibilities: - concept explanation - examples - analogies - visual
explanation - guided learning - misconception repair - hints - adaptive
explanations

Mira must respond to actual learner state.

Teaching loop:

Explain → Interact → Observe → Respond → Feedback → Adapt

  ------------------------
  AYAN — Reasoning Agent
  ------------------------

Purpose: Develop and evaluate actual reasoning.

Activities can include: - manual typed reasoning - fill in the blanks -
complete logic - predict output - explain missing steps - fix
reasoning - construct a solution - compare explanations - “Why does this
happen?” - “What would happen if…?” - conditional reasoning

Ayan must NOT become merely an MCQ generator.

  -------------------------------------
  KIRA — Real-World Application Agent
  -------------------------------------

Purpose: Convert conceptual knowledge into practical execution.

Activities: - coding - algorithm design - realistic problem solving -
scenario analysis - engineering decisions - business decisions -
solution design - practical tasks

Kira must create tasks requiring actual action.

Example:

Instead of: “What is Newton’s Second Law?”

Use: “You are designing a vehicle. What happens to acceleration if mass
changes while force remains constant?”

  -------------------
  ZAYN — Quiz Agent
  -------------------

Purpose: Structured assessment.

Generate exactly:

5 questions.

Difficulty timing: - Easy → 30 seconds - Medium → 60 seconds - Hard → 90
seconds

Questions should test: - conceptual understanding - reasoning -
application - prediction - problem solving - explanation

Do not make the assessment purely memorization-based.

  --------------------------
  ELARA — Evaluation Agent
  --------------------------

Purpose: Determine evidence of conceptual clarity.

Inputs: - assessment performance - reasoning quality - application
performance - misconceptions - response behavior - difficulty - previous
learning evidence - current session evidence

Elara must NOT simply calculate:

5/5 = clarity

Instead, determine conceptual clarity from multiple evidence signals.

Output should include: - understanding level - remaining
misconceptions - confidence/evidence strength - weak areas - recommended
next action - whether the learner should progress, practice, revisit, or
deepen the concept

============================================================ 6. MAIN
AGENTIC AI / ORCHESTRATOR
============================================================

The Main Agent is the central intelligence.

It decides: - what the learner needs - whether research is required -
which agent should act - when an agent should act - what context to
provide - what output to accept - how to combine outputs - whether the
roadmap should change - whether the learner needs more practice -
whether the learner is ready to progress

The specialized agents NEVER independently control the overall learning
journey.

Architecture:

Student ↓ Main Orchestrator ↓ Decision ↓ Specialized Agent(s) ↓ Agent
output ↓ Main Orchestrator ↓ Learner response ↓ Observation ↓ Adaptation
↓ Next action

Use LangGraph for this stateful orchestration.

Represent workflow state with typed Pydantic models.

Do NOT place all logic into one giant agent prompt.

Separate: - routing - state - agent contracts - learning logic -
evaluation - persistence

============================================================ 7.
ONBOARDING FLOW
============================================================

First-time user flow MUST be:

CLARIO INTRO ↓ SIGN IN ↓ BASIC PROFILE ↓ EXACTLY 5 MINDSET QUESTIONS ↓
MAIN APPLICATION UNLOCKS

Do NOT send a first-time user directly to the dashboard.

============================================================ 8. SIGN-IN

Support exactly:

-   Google
-   Apple
-   Microsoft

Keep authentication modular and provider-agnostic.

Do not tightly couple business logic to authentication implementation.

============================================================ 9. BASIC
PROFILE ============================================================

Collect:

-   Name
-   Email
-   Age / age range
-   Current education level
-   Domain / field
-   Prior learning / experience

Store appropriate persistent learner information in MySQL.

============================================================ 10. FIVE
MINDSET INTAKE QUESTIONS
============================================================

Question 1:

“When you get a new topic, what do you usually do first?”

A)  Watch a video or visual explanation
B)  Read notes or a textbook
C)  Ask a friend or teacher
D)  Start solving problems

Question 2:

“When preparing for an exam, what feels easiest for you?”

A)  Drawing diagrams or using visuals
B)  Listening to explanations or voice notes
C)  Writing or rewriting notes
D)  Solving lots of practice problems

Question 3:

“When you lose focus in class, what helps you most?”

A)  More visuals or diagrams
B)  A clear verbal explanation
C)  Written notes or handouts
D)  A small activity or task

Question 4:

“When you feel stressed about an exam or assignment, what do you usually
do first?”

A)  Overthink and freeze
B)  Start studying at the last minute
C)  Talk to a friend or mentor
D)  Make a plan and work step by step

Question 5:

“Which teaching style do you enjoy most?”

A)  Story or example first, then the concept
B)  Definition or formula first, then examples
C)  Group discussion or activities
D)  Self-study, then clear doubts when needed

IMPORTANT:

These five responses are initial personalization signals.

Do NOT label the learner permanently as: “visual learner” “auditory
learner” etc.

Actual behavior must continuously refine the learner model.

============================================================ 11. NEW
LEARNING SESSION
============================================================

Every new learning session collects EXACTLY four inputs:

1.  TASK What do you want to learn or accomplish?

2.  GOAL What should you be able to do by the end?

3.  LEARNER STATE What do you already know? Where are you stuck?

4.  INTERESTS What interests, examples, or contexts should we use?

These inputs become current session context.

Main Agent combines:

Current session intake + Basic profile + Mindset intake + Learning
history + Previous performance + Strengths + Weaknesses + Recurring
misconceptions + Observed behavior + Progress

Then generate the personalized roadmap.

============================================================ 12. CLARIO
LEARNING MAP
============================================================

The Learning Map is the HEART of CLARIO.

For the initial prototype/product:

Use Duolingo-inspired UX AND visual identity.

Use: - green visual identity - curved learning path - progression
nodes - rounded components - locked/unlocked/current/completed states -
strong CTA hierarchy - XP - streak - progression - immediate feedback -
animated progression

Do not build a generic LMS dashboard.

The roadmap is the complete learning journey.

Possible learning experiences:

-   concept understanding
-   visual exploration
-   guided practice
-   critical thinking
-   real-world application
-   challenge
-   assessment
-   revision
-   clarity checkpoint

BUT:

These are NOT a fixed mandatory sequence.

The Main Agent dynamically decides the path.

============================================================ 13. DYNAMIC
ROADMAP ENGINE
============================================================

The roadmap must be mutable.

The system can:

-   add prerequisites
-   skip known concepts
-   split concepts
-   merge related concepts
-   add misconception repair
-   add additional practice
-   increase difficulty
-   decrease difficulty
-   insert application tasks
-   insert revision
-   add deeper challenges
-   remove unnecessary nodes
-   reorder nodes
-   unlock new nodes
-   expand the roadmap

Example:

Learner knows prerequisite → skip it.

Learner repeatedly misunderstands concept → insert misconception-repair
node.

Learner performs strongly → increase difficulty.

Learner struggles → add guided practice.

Roadmap changes must persist in MySQL.

============================================================ 14. NODE
INTERACTION ============================================================

Every roadmap node is interactive.

Click node ↓ Open learning experience ↓ Complete activity ↓ Evaluate
result ↓ Return to roadmap ↓ Mark node complete ↓ Unlock next node

If more learning is required:

Create new node ↓ Insert into roadmap ↓ Animate roadmap update ↓
Continue learning

============================================================ 15.
LEARNING EXPERIENCE DESIGN
============================================================

Learning must be interactive.

Possible interactions:

-   MCQ
-   drag/drop
-   matching
-   ordering
-   prediction
-   slider
-   visual manipulation
-   scenario decision
-   mini simulation
-   fill-in-the-blank
-   problem solving
-   explain in own words
-   compare situations

Every interaction must serve the learning objective.

Do NOT add random gamification interactions.

============================================================ 16. WRONG
ANSWER BEHAVIOR
============================================================

Never respond only:

“Wrong.”

Instead:

1.  Detect likely misconception.
2.  Explain the important missing idea.
3.  Provide a relevant hint.
4.  Give an alternative example if needed.
5.  Allow retry.
6.  Record the misconception.
7.  Adapt the next learning step.

Example tone:

“Your idea is close, but one important part is missing.”

============================================================ 17.
CONCEPTUAL CLARITY MODEL
============================================================

Conceptual progression:

CONFUSED ↓ EXPLORING ↓ CONNECTING ↓ CLICKING ↓ CLEAR

The system must track conceptual evidence rather than only completion
percentage.

Possible evidence: - correct answer - explanation quality - reasoning -
application - prediction - misconception recovery - consistency -
transfer to new context

============================================================ 18. AHA
MOMENT ============================================================

The learner should experience a clear conceptual breakthrough.

Possible UI:

Concept pieces connect visually ↓ AHA moment ↓ “IT CLICKS.” ↓
“Conceptual clarity achieved.” ↓ +20 Clarity

Do NOT claim: “100% mastery” “guaranteed mastery” “perfect
understanding”

Use evidence-based language.

============================================================ 19.
GAMIFICATION
============================================================

Include:

-   XP
-   Clarity
-   Clarity Streak
-   Daily Mission
-   Levels
-   Achievements
-   Milestones
-   Concept unlocks

Do NOT use hearts/lives.

Rewards must represent meaningful learning.

Examples:

Misconception resolved → +20 Clarity

Concept connected → +15 Clarity

Application completed → +25 XP

============================================================ 20. LEARNER
MEMORY ============================================================

LONG-TERM MEMORY / SOURCE OF TRUTH:

MySQL stores:

-   learner profile
-   interests
-   goals
-   prior knowledge
-   preferences
-   recurring misconceptions
-   strengths
-   weak areas
-   learning behavior
-   progress
-   achievements
-   learning history
-   conceptual clarity evidence

SESSION / WORKFLOW STATE:

LangGraph stores working execution state such as:

-   current task
-   current goal
-   learner state
-   interests
-   current context
-   current misconceptions
-   active roadmap
-   current node
-   agent outputs
-   assessment state

Do NOT use LangGraph runtime state as the permanent application
database.

============================================================ 21.
DATABASE DESIGN
============================================================

Design a normalized MySQL schema.

At minimum consider entities for:

users profiles mindset_responses learning_sessions session_inputs
learner_model learning_goals roadmaps roadmap_nodes learning_activities
activity_attempts concepts concept_progress misconceptions
learning_evidence assessments assessment_questions assessment_attempts
achievements user_achievements streaks xp_transactions clarity_events
agent_runs learning_history

Do not blindly create unnecessary tables.

Each table must have: - primary key - appropriate foreign keys -
timestamps - indexes where needed - constraints - appropriate data types

Use SQLAlchemy models.

Use migration support appropriately.

Never store secrets in the database.

============================================================ 22. API
DESIGN ============================================================

Create clean REST APIs through FastAPI.

Group endpoints logically.

Examples:

/auth /profile /onboarding /mindset /sessions /roadmaps /roadmap-nodes
/learning /activities /attempts /assessments /progress /achievements
/insights /history /stream

Use Pydantic request/response schemas.

Do not expose database models directly as API contracts.

Use consistent error responses.

Validate all inputs.

============================================================ 23. AI API
ABSTRACTION ============================================================

Create a provider abstraction.

Application code should interact with a common interface.

Conceptually:

LLMProvider ├── GeminiProvider ├── GroqProvider └── OpenRouterProvider

Routing:

Gemini ↓ failure/unavailable Groq ↓ failure/unavailable OpenRouter

Handle: - timeout - rate limit - malformed response - provider failure -
invalid structured output

Never expose provider-specific failures directly to the student.

============================================================ 24.
STRUCTURED AI OUTPUTS
============================================================

Do not depend on fragile free-form LLM text for application logic.

Use Pydantic structured schemas for:

-   agent decisions
-   roadmap generation
-   roadmap updates
-   teaching responses
-   reasoning tasks
-   application tasks
-   assessment questions
-   evaluation
-   misconception detection
-   learner model updates

Example conceptual schema:

AgentDecision: - action - agent - reason - context_requirements -
expected_output

RoadmapNode: - id - concept - objective - activity_type - difficulty -
status - prerequisites - estimated_time

EvaluationResult: - conceptual_state - evidence - misconceptions -
strengths - weaknesses - recommendation - confidence

Schemas should be explicit and validated.

============================================================ 25. PROMPT
ENGINEERING ============================================================

Use layered prompting.

Do NOT create one giant prompt containing all runtime information.

Separate:

SYSTEM INSTRUCTIONS + AGENT ROLE + TASK + LEARNER CONTEXT + SESSION
CONTEXT + RELEVANT HISTORY + AVAILABLE TOOLS + OUTPUT SCHEMA

Use: - clear role definition - explicit constraints - structured
context - tool boundaries - few-shot examples only when useful -
structured outputs - validation - retry/repair for invalid outputs

Never place secrets/API keys inside prompts.

Never send irrelevant learner history.

Only provide the minimum useful context to each agent.

============================================================ 26. CONTEXT
MANAGEMENT ============================================================

Do not blindly pass the complete learner database to every agent.

Context should be selected based on the current task.

Example:

Mira needs: - concept - goal - current learner state - relevant
misconceptions - relevant history

Nova needs: - research question - required freshness - domain -
constraints

Ayan needs: - concept - current understanding - reasoning evidence

Kira needs: - concept - goal - application context

Zayn needs: - learning objectives - covered concepts - evidence
requirements

Elara needs: - assessment - reasoning - application - misconceptions -
prior evidence

============================================================ 27.
RESEARCH AGENT / TAVILY
============================================================

When current/external information is required:

Nova decides research is needed.

Tavily retrieves relevant search results and sources.

Pipeline:

Research request ↓ search/retrieve ↓ extract ↓ clean ↓ deduplicate ↓ structure ↓
relevance filtering ↓ context for agent

Never pass huge raw webpages into the LLM.

Research outputs should identify: - source - extracted information -
relevance - freshness when available

============================================================ 28.
REAL-TIME STREAMING
============================================================

Use SSE where real-time interaction improves UX.

Example:

Frontend ↓ POST learning request ↓ FastAPI ↓ LangGraph ↓ agent execution
↓ SSE events ↓ React UI updates progressively

Possible events:

session_started agent_started research_started research_completed
teaching_started activity_generated evaluation_started roadmap_updated
xp_awarded clarity_awarded node_completed error completed

Do not stream sensitive internal chain-of-thought.

Only stream safe user-facing status/results.

============================================================ 29.
FRONTEND STRUCTURE
============================================================

Main application:

INTRO SIGN IN PROFILE MINDSET INTAKE HOME LEARNING MAP NEW SESSION
LEARNING EXPERIENCE PROGRESS ACHIEVEMENTS INSIGHTS PROFILE LEARNING
HISTORY

The application should feel like ONE cohesive product.

============================================================ 30. HOME
SCREEN ============================================================

Show:

-   greeting
-   current goal
-   Continue Learning
-   roadmap preview
-   Clarity Streak
-   XP
-   Clarity
-   Daily Mission
-   recent achievements
-   learning insights
-   New Learning Session CTA

Primary CTA:

Continue Learning

Secondary CTA:

New Learning Session

============================================================ 31.
INSIGHTS ============================================================

Generate evidence-based insights.

Examples:

“You understand concepts faster through examples.”

“You are improving at applying concepts.”

“You tend to struggle when multiple ideas are combined.”

“You recovered quickly from a misconception.”

Avoid unsupported psychological claims.

Insights must be derived from actual learning evidence.

============================================================ 32.
ACHIEVEMENTS
============================================================

Examples:

First Clarity Misconception Breaker Concept Connector Deep Thinker
Application Master Consistency Builder Curiosity Explorer

Achievement conditions must be implemented through real application
events, not static labels.

============================================================ 33. UI / UX

Initial visual direction:

Duolingo-inspired.

Use: - green - rounded UI - curved path - progression nodes - friendly
illustrations - strong CTAs - clear hierarchy - polished modern design -
professional but approachable

Avoid: - generic SaaS dashboard - corporate LMS appearance - static
chatbot appearance - excessive childish styling

Desktop-first:

Primary: 1440px

Also support: 1280px 1024px

Mobile can be added later but architecture should not block it.

============================================================ 34.
ANIMATION ============================================================

Use meaningful animation only.

Examples:

-   path drawing
-   node unlock
-   node completion
-   current-node emphasis
-   feedback
-   XP increment
-   Clarity increment
-   AHA moment
-   achievement unlock
-   dynamic roadmap insertion
-   smooth page transitions

Avoid excessive animation.

============================================================ 35. ERROR /
LOADING / EMPTY STATES
============================================================

Every async operation must have:

Loading state Success state Error state Retry path Empty state where
appropriate

Examples:

LLM unavailable → graceful fallback

Research unavailable → continue with existing knowledge if safe

Malformed agent output → validate → repair/retry → fallback

Database failure → safe error response

Network interruption → recover/retry where appropriate

Never expose raw stack traces to users.

============================================================ 36.
SECURITY ============================================================

Implement basic production-grade security practices:

-   environment variables for secrets
-   never hardcode API keys
-   authentication validation
-   authorization checks
-   input validation
-   SQL injection prevention through ORM/parameterization
-   safe CORS configuration
-   secure error handling
-   rate limiting where appropriate
-   protect sensitive endpoints
-   do not expose internal agent data
-   do not expose chain-of-thought
-   sanitize untrusted research content

============================================================ 37. CODE
QUALITY ============================================================

Code must be:

-   readable
-   modular
-   typed
-   documented where necessary
-   logically organized
-   testable
-   maintainable

Avoid:

-   giant files
-   giant components
-   duplicated logic
-   unnecessary abstractions
-   unnecessary dependencies
-   magic values
-   hidden side effects
-   tightly coupled modules

Prefer simple architecture over premature complexity.

============================================================ 38. PROJECT
STRUCTURE ============================================================

Create a clean structure similar to:

frontend/ src/ components/ pages/ layouts/ hooks/ services/ types/
utils/ features/

backend/ app/ api/ core/ models/ schemas/ services/ repositories/ ai/
orchestrator/ agents/ providers/ prompts/ schemas/ learning/ memory/
research/ db/ main.py

tests/ frontend/ backend/ ai/ integration/

Adjust structure when justified, but preserve clear separation of
responsibilities.

============================================================ 39. AI
AGENT CONTRACTS
============================================================

Every agent must have:

-   explicit purpose
-   input schema
-   output schema
-   allowed tools
-   failure behavior
-   validation
-   test cases

Do not allow agents to directly mutate arbitrary database state.

Database mutations must pass through controlled application services.

============================================================ 40. CORE
LEARNING LOOP
============================================================

Implement and verify this complete loop first:

Student ↓ Session Intake ↓ Main Agent ↓ Personalized Roadmap ↓ One
Learning Node ↓ Mira Teaching ↓ Interactive Activity ↓ Student Response
↓ Evaluate Response ↓ Misconception Detection ↓ Adaptation ↓ Zayn
Assessment ↓ Elara Evaluation ↓ Conceptual Clarity ↓ Clarity / XP ↓
Persist Evidence ↓ Update Learner Model ↓ Update Roadmap ↓ Next Node

This vertical slice is the first major milestone.

Do NOT build all six agents deeply before proving this loop.

============================================================ 41.
DEVELOPMENT STRATEGY
============================================================

PHASE 0 — INSPECT

Before modifying the project:

-   inspect repository
-   inspect existing files
-   inspect package configuration
-   inspect environment configuration
-   identify existing code
-   identify reusable components
-   identify conflicts
-   identify missing pieces

Do NOT blindly overwrite existing work.

Create an implementation plan based on the actual repository.

PHASE 1 — FOUNDATION

Build:

-   project structure
-   frontend shell
-   backend shell
-   database connection
-   configuration
-   environment handling
-   API foundation
-   error handling

PHASE 2 — AUTH + ONBOARDING

Build:

-   Intro
-   Sign In
-   Profile
-   5 mindset questions
-   persistence

PHASE 3 — LEARNING SESSION

Build:

-   New Learning Session
-   four intake inputs
-   session persistence

PHASE 4 — AI FOUNDATION

Build:

-   LLM abstraction
-   Gemini
-   Groq fallback
-   OpenRouter fallback
-   Pydantic schemas
-   LangGraph state
-   Main Orchestrator

PHASE 5 — VERTICAL LEARNING SLICE

Implement:

Session → roadmap → one node → teaching → interaction → evaluation →
clarity → persistence

PHASE 6 — SPECIALIZED AGENTS

Implement:

Nova Mira Ayan Kira Zayn Elara

Integrate each through Main Orchestrator.

PHASE 7 — DYNAMIC ROADMAP

Implement:

-   node insertion
-   skipping
-   difficulty adaptation
-   misconception repair
-   progression
-   roadmap persistence

PHASE 8 — GAMIFICATION

Implement:

-   XP
-   Clarity
-   streak
-   achievements
-   daily mission
-   milestones

PHASE 9 — INSIGHTS + HISTORY

Implement:

-   learner insights
-   learning history
-   progress
-   conceptual clarity trends

PHASE 10 — REAL-TIME

Implement SSE/LangGraph streaming where needed.

PHASE 11 — TESTING

Run:

-   unit tests
-   integration tests
-   API tests
-   AI schema tests
-   frontend tests
-   end-to-end critical flow

PHASE 12 — FINAL VERIFICATION

Verify the complete user journey from:

Intro → Sign In → Profile → Mindset Intake → Home → New Session → Four
Inputs → AI Roadmap → Node → Teaching → Interaction → Mistake →
Misconception Support → Retry → Success → Assessment → Clarity → XP →
Roadmap Update → Next Node → Progress → Achievements → Insights →
History

============================================================ 42. TEST
SCENARIO ============================================================

Create at least one realistic demonstration learner.

Example:

Name: Alex

Domain: Computer Science

Goal: Understand Machine Learning fundamentals.

Session:

Task: “Learn machine learning fundamentals.”

Goal: “Understand how a model learns from data and explain the process.”

Learner State: “I know basic Python but machine learning feels
confusing.”

Interest: “Use coding and real-world examples.”

Demonstrate:

-   initial learner state
-   personalized roadmap
-   teaching
-   interactive reasoning
-   wrong response
-   misconception detection
-   repair
-   retry
-   application
-   5-question assessment
-   Elara evaluation
-   AHA moment
-   Clarity reward
-   roadmap update
-   next-node unlock

This scenario is for validation/demo purposes.

Do NOT hardcode the system to only support Alex or machine learning.

============================================================ 43. DATA
FLOW RULE ============================================================

Every major feature must have a traceable path:

UI ↓ API ↓ Service ↓ Database and/or AI ↓ Validated response ↓ UI

If a button exists, determine what happens when clicked.

If a feature claims personalization, identify its data source.

If a feature claims AI adaptation, identify its AI/application logic.

If a feature claims persistence, identify its database write/read.

============================================================ 44. NO FAKE
FUNCTIONALITY RULE
============================================================

Do NOT use fake functionality such as:

-   random AI responses
-   fake loading screens pretending to call AI
-   hardcoded roadmap generation
-   static progress pretending to come from database
-   fake XP calculations
-   fake achievements
-   static learner insights
-   simulated API responses in production paths
-   hardcoded assessment results

Mocks may exist ONLY inside tests or explicitly isolated development
fixtures.

============================================================ 45.
OBSERVABILITY
============================================================

Use LangSmith for AI observability where configured.

Track useful metadata such as:

-   workflow execution
-   agent invoked
-   latency
-   provider
-   success/failure
-   validation failure
-   fallback usage
-   token/cost metadata when available

Do NOT log: - secrets - API keys - unnecessary sensitive learner
information - chain-of-thought

============================================================ 46.
PERFORMANCE ============================================================

Keep the application lightweight.

Optimize for:

-   fast initial load
-   minimal frontend dependencies
-   efficient database queries
-   limited LLM context
-   structured outputs
-   streaming where useful
-   avoiding duplicate AI calls
-   caching only where genuinely useful

Do not introduce infrastructure solely for theoretical scale.

============================================================ 47.
ADAPTIVE LEARNING LOGIC
============================================================

Personalization must combine:

INITIAL SIGNALS + CURRENT CONTEXT + OBSERVED BEHAVIOR + LEARNING
EVIDENCE + HISTORY

Example:

Initial preference: visual examples.

Observed behavior: learner performs better after worked examples.

System confidence: increase evidence for example-driven teaching.

Observed behavior changes: adapt future teaching.

Therefore:

Learner model = continuously evolving evidence.

Never treat the initial five questions as immutable truth.

============================================================ 48. CLARITY
EVALUATION ============================================================

Conceptual clarity should be inferred from multiple signals.

Example scoring dimensions:

Understanding Reasoning Application Transfer Misconception recovery
Consistency

The exact internal scoring mechanism can evolve.

But the system must avoid reducing clarity to one quiz score.

Elara should produce an interpretable evaluation object.

============================================================ 49. UX
WRITING ============================================================

Use simple, human language.

Prefer:

“Let’s make this click.”

“You’re close.”

“One important idea is missing.”

“Try it again.”

“Nice — that connection is correct.”

“It clicks.”

Avoid:

-   robotic AI language
-   unnecessary technical jargon
-   long explanations
-   system/debug terminology
-   exposing internal agent architecture

============================================================ 50.
INTERNAL VS EXTERNAL ARCHITECTURE
============================================================

INTERNAL:

Main Orchestrator Nova Mira Ayan Kira Zayn Elara LangGraph LLMs Tavily
database services

EXTERNAL:

The learner sees:

CLARIO

The architecture should be sophisticated internally but simple
externally.

============================================================ 51.
ENVIRONMENT CONFIGURATION
============================================================

Use environment variables.

Expected configuration categories:

DATABASE_URL GEMINI_API_KEY GROQ_API_KEY OPENROUTER_API_KEY
MISTRAL_API_KEY TAVILY_API_KEY LANGSMITH_API_KEY AUTH configuration CORS
configuration

Provide a safe .env.example.

Never commit actual credentials.

============================================================ 52.
DOCUMENTATION
============================================================

Create concise documentation for:

-   setup
-   environment variables
-   running frontend
-   running backend
-   database setup
-   migrations
-   AI provider configuration
-   architecture
-   API usage
-   testing

Documentation must match the actual implementation.

============================================================ 53.
ACCEPTANCE CRITERIA
============================================================

The implementation is NOT complete until:

[ ] Frontend runs [ ] Backend runs [ ] MySQL connection works [ ]
Authentication flow is implemented [ ] Onboarding persists [ ] Five
mindset questions persist [ ] New session works [ ] Four intake inputs
persist [ ] Main Orchestrator works [ ] LLM abstraction works [ ]
Provider fallback works [ ] LangGraph workflow works [ ] Roadmap is
generated dynamically [ ] Roadmap persists [ ] Node interaction works []
Teaching works [ ] Reasoning works [ ] Application works [ ] Assessment
generates five questions [ ] Evaluation works [ ] Misconceptions are
recorded [ ] Learner model updates [ ] Clarity is calculated from
evidence [ ] XP works [ ] Streak works [ ] Achievements work [ ]
Insights are evidence-based [ ] Learning history works [ ] SSE works
where implemented [ ] Error states work [ ] Critical journey passes
end-to-end testing [ ] No critical console errors [ ] No critical
backend errors [ ] No broken production placeholders

============================================================ 54.
SELF-REVIEW LOOP
============================================================

After each major implementation phase:

1.  Inspect generated code.
2.  Run tests.
3.  Run the application.
4.  Test the feature manually.
5.  Check frontend console.
6.  Check backend logs.
7.  Check database persistence.
8.  Check API contracts.
9.  Check AI structured outputs.
10. Fix discovered issues.
11. Re-run tests.
12. Only then move forward.

Never assume code works because it compiles.

============================================================ 55. FAILURE
RECOVERY ============================================================

If implementation fails:

DO NOT stop after describing the error.

Instead:

Identify → diagnose → fix → retest → verify

If a provider fails:

Gemini → Groq → OpenRouter

If an AI response fails schema validation:

validate → repair/retry → fallback safely

If a UI/API mismatch occurs:

inspect contract → fix backend/frontend → retest integration

============================================================ 56.
IMPLEMENTATION BEHAVIOR
============================================================

When executing this prompt:

FIRST: Inspect the repository.

SECOND: Summarize the current implementation state.

THIRD: Create a concise implementation plan.

FOURTH: Identify blockers/dependencies.

FIFTH: Implement the highest-priority vertical slice.

SIXTH: Run tests and verify.

SEVENTH: Continue phase by phase.

Do NOT spend the entire execution generating documentation without
implementing the application.

Do NOT ask for confirmation after every small step.

Make reasonable engineering decisions within these constraints.

Only ask a question when a genuinely blocking ambiguity cannot be
resolved safely.

============================================================ 57. FINAL
RULE ============================================================

Build CLARIO as a REAL connected application.

Not:

a landing page.

Not:

a dashboard mockup.

Not:

a chatbot demo.

Not:

a static prototype.

Build:

A functioning personalized adaptive learning platform where:

REAL USER INPUT → REAL APPLICATION LOGIC → REAL AI ORCHESTRATION → REAL
LEARNING EXPERIENCE → REAL LEARNER RESPONSES → REAL EVALUATION → REAL
CONCEPTUAL CLARITY → REAL DATABASE PERSISTENCE → REAL ADAPTATION → REAL
FUTURE PERSONALIZATION

The final product must feel like:

ONE intelligent learning companion.

Internally:

one Main Agentic AI controlling six specialized agents.

Externally:

one seamless CLARIO experience.

Prioritize correctness, simplicity, maintainability, real integration,
and genuine learning value over unnecessary technical complexity.

BEGIN IMPLEMENTATION.

============================================================ 58. CLARIO
CURRENT FINALIZED STATE — SEPTEMBER 14, 2026
============================================================

This section is the current authoritative update to the older
MastriX/CLARIO specification above.

Project identity: - Product name: CLARIO - CLARIO replaces the earlier
MastriX / PeerMind naming. - Core promise: “Come confused. Leave with
clarity.” - Primary outcome: conceptual clarity, not guaranteed
mastery. - The learner should leave a session feeling: “I came here
confused, and now it actually clicks.”

The older MastriX-SIH specification is treated as historical/reference
material. Where it conflicts with this current CLARIO specification, the
current CLARIO decisions below take precedence.

  -------------------------------------------
  58.1 ONE PRODUCT / ONE INTELLIGENT SYSTEM
  -------------------------------------------

CLARIO must feel like ONE intelligent learning companion.

The learner must NOT see six independent chatbots.

Internally: - One Main Agentic AI / Main Orchestrator - Six specialized
agents - LangGraph orchestration - Persistent learner data in MySQL -
Session/workflow state in LangGraph

Externally: - One cohesive CLARIO experience - One consistent product
personality - Specialized agents remain invisible to the learner unless
their contribution needs to be represented as part of the learning flow.

CLARIO’s overall personality: - friendly tutor - curious friend -
practical coach - never childish - never judgmental - never robotic

  --------------------------------------
  58.2 FINAL SIX AGENT NAMES AND ROLES
  --------------------------------------

1.  NOVA — Research Agent Internal personality: The Librarian

    Purpose: Research current/relevant external information when needed.

    Responsibilities:

    -   web research
    -   Tavily
    -   retrieve relevant information
    -   clean noisy content
    -   structure findings
    -   provide relevant context only

2.  MIRA — Teaching Agent Internal personality: The Patient Mentor

    Purpose: Explain concepts simply and adaptively.

    Responsibilities:

    -   explanations
    -   examples
    -   analogies
    -   visual explanations
    -   guided learning
    -   misconception repair
    -   hints
    -   adaptive re-explanation

3.  AYAN — Reasoning / Critical Thinking Agent Internal personality: The
    Socratic Challenger

    Purpose: Develop and evaluate actual reasoning.

    Activities:

    -   manual typed reasoning
    -   fill in blanks
    -   complete logic
    -   predict output
    -   explain missing steps
    -   fix reasoning
    -   construct solutions
    -   compare explanations
    -   why/how questions
    -   what-if reasoning
    -   conditional reasoning

    Ayan is NOT merely an MCQ generator.

4.  KIRA — Real-World Application Agent Internal personality: The
    Practical Coach

    Purpose: Convert conceptual knowledge into practical execution.

    Activities:

    -   coding
    -   algorithm design
    -   realistic problem solving
    -   scenario analysis
    -   engineering decisions
    -   business decisions
    -   solution design
    -   practical tasks

    Kira must require actual action from the learner.

5.  ZAYN — Quiz / Assessment Agent Internal personality: The Fair
    Examiner

    Purpose: Structured assessment.

    IMPORTANT: Zayn generates exactly 5 questions for an assessment.

    Locked timing:

    -   Easy = 30 seconds per question
    -   Medium = 60 seconds per question
    -   Hard = 90 seconds per question

    Assessment should test:

    -   conceptual understanding
    -   reasoning
    -   application
    -   prediction
    -   problem solving
    -   explanation

    Assessment must not be purely memorization-based.

6.  ELARA — Evaluation / Conceptual Clarity Agent Internal personality:
    The Calm Analyst

    Purpose: Determine evidence of conceptual clarity.

    Inputs:

    -   assessment performance
    -   reasoning quality
    -   application performance
    -   misconceptions
    -   response behavior
    -   difficulty
    -   previous learning evidence
    -   current session evidence

    Elara must NOT reduce clarity to a single quiz score.

    Output should include:

    -   understanding level
    -   remaining misconceptions
    -   confidence/evidence strength
    -   weak areas
    -   recommended next action
    -   whether to progress, practice, revisit, or deepen

  -------------------------------------
  58.3 MAIN ORCHESTRATOR — FINAL ROLE
  -------------------------------------

The Main Agentic AI / Main Orchestrator is the central intelligence.

It controls and coordinates: Nova Mira Ayan Kira Zayn Elara

The specialized agents do not independently control the overall learning
journey.

Core loop:

Student ↓ Main Orchestrator ↓ Decision ↓ Specialized Agent(s) ↓
Validated Agent Output ↓ Main Orchestrator ↓ Learner-facing response ↓
Observation ↓ Adaptation ↓ Next action

Use LangGraph for stateful orchestration.

Keep these concerns separate: - routing - workflow state - agent
contracts - learning logic - evaluation - persistence

Do NOT put the complete product logic into one giant agent prompt.

  ----------------------------
  58.4 FINAL ONBOARDING FLOW
  ----------------------------

First-time user flow is locked:

CLARIO INTRO ↓ SIGN IN ↓ BASIC PROFILE ↓ EXACTLY 5 MINDSET QUESTIONS ↓
MAIN APPLICATION UNLOCKS

A first-time learner must not be sent directly to the dashboard.

Supported sign-in providers: - Google - Apple - Microsoft

Authentication must remain modular and provider-agnostic.

Basic profile: - Name - Email - Age / age range - Current education
level - Domain / field - Prior learning / experience

  -----------------------------------
  58.5 FINAL FIVE MINDSET QUESTIONS
  -----------------------------------

Question 1: “When you get a new topic, what do you usually do first?”

A)  Watch a video or visual explanation
B)  Read notes or a textbook
C)  Ask a friend or teacher
D)  Start solving problems

Question 2: “When preparing for an exam, what feels easiest for you?”

A)  Drawing diagrams or using visuals
B)  Listening to explanations or voice notes
C)  Writing or rewriting notes
D)  Solving lots of practice problems

Question 3: “When you lose focus in class, what helps you most?”

A)  More visuals or diagrams
B)  A clear verbal explanation
C)  Written notes or handouts
D)  A small activity or task

Question 4: “When you feel stressed about an exam or assignment, what do
you usually do first?”

A)  Overthink and freeze
B)  Start studying at the last minute
C)  Talk to a friend or mentor
D)  Make a plan and work step by step

Question 5: “Which teaching style do you enjoy most?”

A)  Story or example first, then the concept
B)  Definition or formula first, then examples
C)  Group discussion or activities
D)  Self-study, then clear doubts when needed

IMPORTANT: These answers create only an initial learner hypothesis.

They must NEVER permanently label the learner as: - visual learner -
auditory learner - reading/writing learner - kinesthetic learner or any
other fixed learning-style category.

Actual behavior and evidence must continuously refine the learner model.

  ----------------------------------------
  58.6 FINAL NEW LEARNING SESSION INTAKE
  ----------------------------------------

Every new learning session collects EXACTLY four inputs:

1.  TASK What do you want to learn or accomplish?

2.  GOAL What should you be able to do by the end?

3.  LEARNER STATE What do you already know? Where are you stuck?

4.  INTERESTS What interests, examples, or contexts should we use?

These become current session context.

The Main Orchestrator combines:

Current session intake + Basic profile + Mindset intake + Learning
history + Previous performance + Strengths + Weaknesses + Recurring
misconceptions + Observed behavior + Progress

Then it creates the personalized learning roadmap.

  ---------------------------------------------------
  58.7 FINAL LEARNER-STATE IDENTIFICATION ALGORITHM
  ---------------------------------------------------

ALGORITHM: CLARIO-NLP INITIAL LEARNER STATE IDENTIFICATION

INPUT: - Student_Statement - Learning_Goal - Topic - Interest (optional)

OUTPUT: - Initial_Learner_Profile - Recommended_Starting_Level -
Initial_Learning_Strategy - Confidence

Purpose: Infer an initial learner state from natural-language input
without treating the result as permanent truth.

The algorithm should:

1.  Normalize the student’s statement.
2.  Extract:
    -   known concepts
    -   unknown concepts
    -   confusion/stuck points
    -   goal
    -   requested depth
    -   interest/context
    -   explicit experience level
3.  Identify evidence of prior knowledge.
4.  Identify evidence of difficulty/confusion.
5.  Estimate an initial level:
    -   Beginner
    -   Intermediate
    -   Advanced
6.  Select an initial learning strategy.
7.  Assign confidence to the inference.
8.  Mark uncertain assumptions explicitly.
9.  Use subsequent learner behavior to update the learner model.

The initial result is a hypothesis, not a permanent classification.

Behavioral evidence has higher long-term value than a one-time
self-description.

  ----------------------------------------------------
  58.8 LEARNING MAP / ROADMAP — CURRENT UX DIRECTION
  ----------------------------------------------------

The Learning Map is the heart of CLARIO.

UX direction: - Duolingo-inspired learning-path interaction - green
visual identity - curved learning path - progression nodes - rounded
components - locked / unlocked / current / completed states - strong CTA
hierarchy - XP - Clarity - streak - immediate feedback - meaningful
animation

CLARIO must NOT look like: - a generic LMS - a corporate SaaS
dashboard - a static chatbot - an ordinary course list

The roadmap is dynamic.

Possible experiences include: - concept understanding - visual
exploration - guided practice - critical thinking - real-world
application - challenge - assessment - revision - clarity checkpoint

These are NOT a fixed mandatory sequence.

The Main Orchestrator decides the appropriate next experience.

  -----------------------------
  58.9 DYNAMIC ROADMAP ENGINE
  -----------------------------

The roadmap is mutable and evidence-driven.

The system may: - add prerequisites - skip known concepts - split
concepts - merge related concepts - add misconception repair - add
additional practice - increase difficulty - decrease difficulty - insert
application tasks - insert revision - add deeper challenges - remove
unnecessary nodes - reorder nodes - unlock new nodes - expand the
roadmap

Examples:

Known prerequisite → skip it.

Repeated misunderstanding → insert misconception-repair node.

Strong performance → increase difficulty.

Weak performance → add guided practice.

Roadmap changes must persist in MySQL.

  ------------------------
  58.10 NODE INTERACTION
  ------------------------

Every roadmap node is interactive.

Click node → open learning experience → complete activity → evaluate
result → return to roadmap → mark node complete → unlock next node

If more learning is required:

Create new node → insert into roadmap → animate roadmap update →
continue learning

  --------------------------------
  58.11 CONCEPTUAL CLARITY MODEL
  --------------------------------

Conceptual progression:

CONFUSED ↓ EXPLORING ↓ CONNECTING ↓ CLICKING ↓ CLEAR

Clarity must be evidence-based.

Useful evidence includes: - correct answers - explanation quality -
reasoning - application - prediction - misconception recovery -
consistency - transfer to a new context

Do NOT equate: 5/5 = clarity or completion = clarity.

The learner may be clear on one concept and weak on another.

  ------------------
  58.12 AHA MOMENT
  ------------------

CLARIO should create a meaningful conceptual breakthrough.

Possible interaction:

Concept pieces connect ↓ AHA moment ↓ “IT CLICKS.” ↓ “Conceptual clarity
achieved.” ↓ +20 Clarity

Do not claim: - 100% mastery - guaranteed mastery - perfect
understanding

Use evidence-based language.

  ------------------------------------
  58.13 GAMIFICATION — CURRENT MODEL
  ------------------------------------

Include: - XP - Clarity - Clarity Streak - Daily Mission - Levels -
Achievements - Milestones - Concept unlocks

Do NOT use hearts/lives.

Rewards must correspond to meaningful learning.

Examples: - misconception resolved → +20 Clarity - concept connected →
+15 Clarity - application completed → +25 XP

  -----------------------------------
  58.14 MEMORY ARCHITECTURE — FINAL
  -----------------------------------

LONG-TERM MEMORY / SOURCE OF TRUTH: MySQL

MySQL stores appropriate persistent learner information such as: -
learner profile - interests - goals - prior knowledge - preferences -
recurring misconceptions - strengths - weak areas - learning behavior -
progress - achievements - learning history - conceptual clarity evidence

SESSION / WORKFLOW STATE: LangGraph

LangGraph stores working execution state such as: - current task -
current goal - learner state - interests - current context - current
misconceptions - active roadmap - current node - agent outputs -
assessment state

LangGraph runtime state is NOT the permanent application database.

Real-time/session updates should be persisted to MySQL when they become
part of the learner’s durable record.

Do not blindly pass the complete learner database to every agent.
Context must be selected for the current task.

  -------------------------------
  58.15 FINAL AI PROVIDER ORDER
  -------------------------------

Application code uses a provider abstraction.

Common interface: LLMProvider ├── GeminiProvider ├── GroqProvider ├──
OpenRouterProvider └── MistralProvider

Final routing order:

Gemini ↓ failure / unavailable Groq ↓ failure / unavailable OpenRouter ↓
failure / unavailable Mistral

DeepSeek is NOT part of the CLARIO fallback architecture.

Handle: - timeout - rate limit - malformed response - provider failure -
invalid structured output

Provider-specific failures must not be exposed directly to learners.

  ----------------------------------
  58.16 FINAL TECHNOLOGY DIRECTION
  ----------------------------------

Frontend: - React - TypeScript - Tailwind CSS

Do NOT add: - TanStack Query - Zustand - unnecessary global state
libraries - unnecessary UI frameworks

Backend: - Python - FastAPI - Pydantic - SQLAlchemy - MySQL

AI: - Python - LangChain - LangGraph - Pydantic structured outputs - LLM
provider abstraction - LangSmith observability

Research: - Tavily

Real-time: - Server-Sent Events (SSE) - LangGraph streaming where
appropriate

Database: - MySQL only

Do NOT introduce: - Redis - Qdrant - Pinecone - vector database -
Kafka - unnecessary microservices - unnecessary message queues

  ----------------------------------------
  58.17 FINAL AI OUTPUT / CONTRACT RULES
  ----------------------------------------

Use Pydantic structured outputs for: - agent decisions - roadmap
generation - roadmap updates - teaching responses - reasoning tasks -
application tasks - assessment questions - evaluation - misconception
detection - learner model updates

Every agent must have: - explicit purpose - input schema - output
schema - allowed tools - failure behavior - validation - test cases

Agents must not directly mutate arbitrary database state.

Database mutations pass through controlled application services.

  -------------------------------------------
  58.18 FINAL PROMPT / CONTEXT ARCHITECTURE
  -------------------------------------------

Use layered prompting:

SYSTEM INSTRUCTIONS + AGENT ROLE + TASK + LEARNER CONTEXT + SESSION
CONTEXT + RELEVANT HISTORY + AVAILABLE TOOLS + OUTPUT SCHEMA

Never use one giant prompt containing all runtime information.

Never put secrets/API keys inside prompts.

Never send irrelevant learner history.

Only provide the minimum useful context required by each agent.

  ---------------------------
  58.19 FINAL RESEARCH FLOW
  ---------------------------

When current/external information is required:

Nova → research decision → Tavily → search/retrieve → extract → clean →
deduplicate → structure → relevance filtering → context for downstream
agent

Never pass huge raw webpages directly into an LLM.

Research output should identify: - source - extracted information -
relevance - freshness when available

  ---------------------------------
  58.20 FINAL REAL-TIME STREAMING
  ---------------------------------

Use SSE when real-time interaction improves the learning UX.

Example:

Frontend → learning request → FastAPI → LangGraph → agent execution →
SSE events → React UI update

Safe user-facing event types may include: - session_started -
agent_started - research_started - research_completed -
teaching_started - activity_generated - evaluation_started -
roadmap_updated - xp_awarded - clarity_awarded - node_completed -
error - completed

Never stream sensitive internal chain-of-thought.

  -----------------------------
  58.21 WRONG-ANSWER BEHAVIOR
  -----------------------------

Never respond only: “Wrong.”

Instead:

1.  Detect likely misconception.
2.  Explain the missing idea.
3.  Give a relevant hint.
4.  Provide another example when useful.
5.  Allow retry.
6.  Record the misconception.
7.  Adapt the next learning step.

Preferred tone: “Your idea is close, but one important part is missing.”

  -------------------------------------
  58.22 LEARNING LOOP — CURRENT FINAL
  -------------------------------------

Student ↓ Session Intake ↓ Main Agent ↓ Personalized Roadmap ↓ One
Learning Node ↓ Mira Teaching ↓ Interactive Activity ↓ Student Response
↓ Evaluate Response ↓ Misconception Detection ↓ Adaptation ↓ Zayn
Assessment ↓ Elara Evaluation ↓ Conceptual Clarity ↓ Clarity / XP ↓
Persist Evidence ↓ Update Learner Model ↓ Update Roadmap ↓ Next Node

This vertical slice is the first major milestone.

Do NOT build all six agents deeply before proving this loop.

  ----------------------------------
  58.23 FINAL DEVELOPMENT PRIORITY
  ----------------------------------

Build in this order:

PHASE 0 — INSPECT - inspect repository - inspect package configuration -
inspect environment - identify reusable code - identify conflicts -
identify missing pieces - create implementation plan from actual
repository

PHASE 1 — FOUNDATION - frontend shell - backend shell - MySQL
connection - configuration - environment handling - API foundation -
error handling

PHASE 2 — AUTH + ONBOARDING - Intro - Sign In - Profile - exactly 5
mindset questions - persistence

PHASE 3 — SESSION - New Learning Session - exactly 4 intake inputs -
persistence

PHASE 4 — AI FOUNDATION - LLM abstraction - Gemini - Groq - OpenRouter -
Mistral - Pydantic schemas - LangGraph state - Main Orchestrator

PHASE 5 — VERTICAL LEARNING SLICE - session - roadmap - one node -
teaching - interaction - evaluation - clarity - persistence

PHASE 6 — SIX AGENTS - Nova - Mira - Ayan - Kira - Zayn - Elara -
integrated through Main Orchestrator

PHASE 7 — DYNAMIC ROADMAP - insertion - skipping - difficulty
adaptation - misconception repair - progression - persistence

PHASE 8 — GAMIFICATION - XP - Clarity - streak - achievements - daily
mission - milestones

PHASE 9 — INSIGHTS + HISTORY - learner insights - learning history -
progress - conceptual clarity trends

PHASE 10 — REAL-TIME - SSE - LangGraph streaming where needed

PHASE 11 — TESTING - unit - integration - API - AI schema - frontend -
end-to-end critical flow

PHASE 12 — FINAL VERIFICATION Verify:

Intro → Sign In → Profile → Mindset Intake → Home → New Session → Four
Inputs → AI Roadmap → Node → Teaching → Interaction → Mistake →
Misconception Support → Retry → Success → Assessment → Clarity → XP →
Roadmap Update → Next Node → Progress → Achievements → Insights →
History

After every major phase: - inspect code - run tests - run application -
manually test - check frontend console - check backend logs - check
database persistence - check API contracts - check AI structured
outputs - fix issues - re-run tests - continue only after verification

  ---------------------------------
  58.24 FINAL ACCEPTANCE CRITERIA
  ---------------------------------

The implementation is not complete until:

[ ] Frontend runs [ ] Backend runs [ ] MySQL connection works [ ]
Authentication works [ ] Onboarding persists [ ] Five mindset questions
persist [ ] New session works [ ] Four session inputs persist [ ] Main
Orchestrator works [ ] LLM abstraction works [ ] Gemini → Groq →
OpenRouter → Mistral fallback works [ ] LangGraph workflow works [ ]
Dynamic roadmap generation works [ ] Roadmap persistence works [ ] Node
interaction works [ ] Teaching works [ ] Reasoning works [ ] Application
works [ ] Zayn generates exactly five assessment questions [ ] Easy
timing = 30 sec/question [ ] Medium timing = 60 sec/question [ ] Hard
timing = 90 sec/question [ ] Elara evaluation works [ ] Misconceptions
are recorded [ ] Learner model updates [ ] Clarity uses multiple
evidence signals [ ] XP works [ ] Clarity works [ ] Clarity Streak works
[ ] Achievements work [ ] Insights are evidence-based [ ] Learning
history works [ ] SSE works where implemented [ ] Error states work [ ]
Critical journey passes end-to-end testing [ ] No critical console
errors [ ] No critical backend errors [ ] No broken production
placeholders

  -------------------------------
  58.25 FINAL PRODUCT PRINCIPLE
  -------------------------------

CLARIO is not:

-   a landing page
-   a dashboard mockup
-   a chatbot demo
-   a static prototype
-   a fixed LMS course

CLARIO is:

REAL USER INPUT → REAL APPLICATION LOGIC → REAL AI ORCHESTRATION → REAL
LEARNING EXPERIENCE → REAL LEARNER RESPONSES → REAL EVALUATION → REAL
CONCEPTUAL CLARITY → REAL DATABASE PERSISTENCE → REAL ADAPTATION → REAL
FUTURE PERSONALIZATION

The final product must feel like:

ONE intelligent learning companion.

Internally: one Main Agentic AI controlling six specialized agents.

Externally: one seamless CLARIO experience.

The governing principle remains:

“Come confused. Leave with clarity.”

============================================================ 59. VERSION
/ PRECEDENCE NOTE
============================================================

Document basis: - Earlier CLARIO/MastriX implementation specification -
Current finalized CLARIO decisions through September 14, 2026

This September 14, 2026 section is the authoritative update for
decisions that changed after the older specification.

In particular, the current decisions supersede older references to: -
MastriX / PeerMind naming - old generic Agent 1–6 names - old agent role
labels where the final names are now Nova/Mira/Ayan/ Kira/Zayn/Elara -
old assessment timing if different - old provider fallback order if
different - fixed learning-style classification - fixed learning
sequence - mastery-oriented claims - LangGraph as permanent learner
database - static/fake learning journeys

END OF UPDATED CLARIO MASTER SPECIFICATION

============================================================ 60. FINAL
AUTHENTICATION — REAL GOOGLE OAUTH + SIGN-IN/OUT
============================================================

CLARIO MUST use real Google OAuth/OIDC authentication in production.

Do NOT use fake login, simulated OAuth, hardcoded demo users,
frontend-only authentication, or localStorage flags as the source of
truth.

AUTHENTICATION FLOW

CLARIO ↓ Continue with Google ↓ Real Google OAuth/OIDC ↓ Backend
validates authentication result ↓ Find/create CLARIO user ↓ Create
secure CLARIO application session ↓ Determine onboarding state ↓ Route
to Profile/Onboarding or Home

The backend is the authentication trust boundary.

SECURITY REQUIREMENTS

-   Store OAuth credentials only in environment variables.
-   Never commit client secrets or API credentials.
-   Validate issuer, audience/client ID, token integrity/signature,
    expiration, and OAuth state/nonce as appropriate to the selected
    flow.
-   Use HTTPS in production.
-   Configure exact authorized origins and redirect URIs.
-   Never accept arbitrary redirect URIs.
-   Do not use email alone as the permanent provider identity.
-   Store Google’s stable subject/provider identifier for account
    linking.
-   Never store Google passwords.
-   Do not expose OAuth client secrets or unnecessary provider tokens to
    the frontend.
-   Use secure session/cookie handling.

Expected configuration categories:

GOOGLE_CLIENT_ID GOOGLE_CLIENT_SECRET GOOGLE_REDIRECT_URI SESSION_SECRET
/ AUTH_SECRET FRONTEND_URL BACKEND_URL

Use the exact variables required by the final implementation and
document them in .env.example.

CLARIO USER IDENTITY

Authentication identity and learner profile are separate.

Google Identity ↓ Authenticated CLARIO User ↓ Learner Profile ↓ Mindset
Responses ↓ Learner Model ↓ Learning History

The same authenticated account must retain its profile, onboarding
state, mindset responses, sessions, roadmap, progress, achievements, XP,
Clarity, Clarity Streak, and learning history across future logins.

SIGN-IN

Primary production CTA:

“Continue with Google”

After successful authentication: 1. Validate Google authentication on
the backend. 2. Find or create the CLARIO user. 3. Establish a secure
application session. 4. Determine onboarding state. 5. Route
appropriately.

Authenticated + onboarding incomplete → Profile / remaining onboarding
Authenticated + onboarding complete → Home Unauthenticated → Intro /
Sign-In

SIGN-OUT

CLARIO MUST provide a real Sign Out action.

Sign Out must: 1. Invalidate the CLARIO application session. 2. Clear
authentication/session cookies securely. 3. Clear authenticated frontend
state. 4. Return the user to the unauthenticated entry screen.

After sign-out, protected APIs must reject the old session.

If provider-side logout/session behavior is relevant to the selected
OAuth architecture, implement it according to Google’s supported
behavior. Never pretend that changing a frontend variable is logout.

AUTHORIZATION

Authentication is not authorization.

Every protected backend endpoint must derive identity from the validated
server-side authentication/session state.

Users must only access their own: - profile - sessions - roadmaps -
activities - attempts - progress - achievements - learner model -
learning history

Never trust a client-supplied user_id for authorization.

AUTH API

Keep authentication separate from learning logic.

Conceptual endpoints:

/auth/google/start /auth/google/callback /auth/me /auth/logout

Exact names may change, but responsibilities must remain separated.

AUTH DATABASE MODEL

The MySQL user/auth model should support: - internal CLARIO user ID -
Google provider stable identifier - email - display name where
appropriate - account creation timestamp - last login timestamp -
account status

Do not use email as the only permanent provider identity key.

FRONTEND AUTH STATE

React must resolve authentication state from the real backend.

Do NOT hardcode isLoggedIn=true. Do NOT use fake localStorage
authentication flags.

Startup:

Frontend → /auth/me → backend validates session →
authenticated/unauthenticated result → render correct state

Provide an authentication loading state while this is being resolved.

ERROR HANDLING

Handle: - user cancels Google authentication - OAuth callback failure -
invalid OAuth state - invalid/expired token - provider unavailable -
session creation failure - database failure during user creation -
expired application session - unauthorized protected API request

Show simple safe user-facing errors and retry paths where appropriate.
Never expose secrets, stack traces, raw provider errors, or internal
authentication details.

TESTING

Verify:

[ ] Unauthenticated user sees Sign-In [ ] Google OAuth starts correctly
[ ] Valid Google authentication creates/locates a user [ ] Existing user
can sign in again [ ] New user is routed to onboarding [ ] Completed
user is routed to Home [ ] /auth/me returns correct authenticated state
[ ] Protected APIs reject unauthenticated requests [ ] Protected APIs
return only current user’s data [ ] Sign Out invalidates the application
session [ ] Signed-out session cannot access protected APIs [ ] Re-login
restores the same CLARIO account [ ] Onboarding state survives re-login
[ ] OAuth errors have safe recovery [ ] No fake production
authentication remains [ ] No credentials are hardcoded

For automated tests, mocks/test credentials may be used only in the
isolated test environment. Production authentication must remain real
Google OAuth.

AUTHENTICATION ACCEPTANCE CRITERIA

[ ] Real Google OAuth works end-to-end [ ] Backend validates Google
authentication [ ] User identity is persisted safely [ ] Secure CLARIO
session is created [ ] Protected APIs enforce authentication [ ]
User-resource authorization is enforced [ ] Real Sign Out works [ ]
Session invalidation works [ ] Re-login preserves the learner account [
] Onboarding survives re-login [ ] No fake authentication remains in
production [ ] .env.example documents auth configuration [ ]
Authentication failures are handled safely [ ] End-to-end authentication
is verified

AUTHENTICATION PRECEDENCE

This section supersedes older instructions that made multiple
authentication providers mandatory.

CURRENT CLARIO REQUIREMENT:

REAL GOOGLE OAUTH is the required production authentication provider for
the current implementation.

Apple and Microsoft can be added later through the provider-agnostic
authentication abstraction, but they must NOT block the current build.

CLARIO must never ship with fake sign-in/sign-out behavior.

END OF AUTHENTICATION UPDATE
