#!/usr/bin/env python3
"""
Generate a complete frontend engineering curriculum as a library of markdown books.
"""

from __future__ import annotations

import re
import textwrap
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "frontend-engineering"


MODULES = [
    {
        "name": "Computing and Network Foundations",
        "theme": "Ground the student in the machine, the network, and the protocols that make web software possible.",
        "family": "foundations",
        "foundations": [],
        "topics": [
            "Computer Science for Frontend Engineers",
            "Computer Architecture Basics",
            "Operating Systems for Web Engineers",
            "Command Line and Unix Thinking",
            "How the Internet Works",
            "Client-Server Architecture",
            "Networking Fundamentals",
            "DNS and Name Resolution",
            "HTTP and HTTPS",
            "TCP, TLS, and Sockets",
        ],
    },
    {
        "name": "The Open Web and HTML",
        "theme": "Teach the browser's document model, standards culture, semantic structure, forms, media, and accessibility-first markup.",
        "family": "html",
        "foundations": [
            "How the Internet Works",
            "HTTP and HTTPS",
            "Browsers and Rendering Engines",
        ],
        "topics": [
            "Browsers and Rendering Engines",
            "Web Standards and the Open Web",
            "HTML Fundamentals",
            "Semantic HTML",
            "Document Structure and Landmarks",
            "Links, Navigation, and URLs",
            "Forms and Validation",
            "Media, Images, Audio, and Video",
            "Accessibility Foundations",
            "ARIA and Assistive Technology",
        ],
    },
    {
        "name": "CSS Foundations",
        "theme": "Move from raw documents to visual systems by teaching how the browser computes style and exposes layout primitives.",
        "family": "css",
        "foundations": [
            "HTML Fundamentals",
            "Semantic HTML",
            "Browsers and Rendering Engines",
        ],
        "topics": [
            "CSS Fundamentals",
            "Selectors, Specificity, and the Cascade",
            "CSS Units and Sizing",
            "Box Model and Layout Basics",
            "Display, Visibility, and Flow",
            "Positioning and Stacking Context",
            "Typography on the Web",
            "Colors, Backgrounds, and Gradients",
            "Borders, Shadows, and Visual Effects",
            "Modern CSS Features and Functions",
        ],
    },
    {
        "name": "Layout, Motion, and Responsive Interfaces",
        "theme": "Teach the layout algorithms and adaptive design decisions that turn CSS primitives into resilient user interfaces.",
        "family": "css",
        "foundations": [
            "CSS Fundamentals",
            "Box Model and Layout Basics",
            "Display, Visibility, and Flow",
        ],
        "topics": [
            "Flexbox",
            "CSS Grid",
            "Floats and Legacy Layout",
            "Overflow, Scrolling, and Scroll Behavior",
            "Responsive Design",
            "Media Queries",
            "Container Queries",
            "Responsive Images",
            "Transforms, Transitions, and Animations",
            "Design Systems and Tokens",
        ],
    },
    {
        "name": "JavaScript Language Foundations",
        "theme": "Build fluency with the language that powers the browser and most frontend tooling stacks.",
        "family": "javascript",
        "foundations": [
            "Computer Science for Frontend Engineers",
            "HTML Fundamentals",
            "CSS Fundamentals",
        ],
        "topics": [
            "JavaScript Fundamentals",
            "Data Types and Values",
            "Variables, Scope, and Hoisting",
            "Operators, Expressions, and Control Flow",
            "Functions and Abstractions",
            "Objects, Prototypes, and Classes",
            "Arrays, Strings, and Collections",
            "Time, Dates, and Internationalization",
            "Error Handling and Defensive Programming",
            "Modules, Packages, and the JavaScript Ecosystem",
        ],
    },
    {
        "name": "JavaScript Internals",
        "theme": "Reveal what the JavaScript engine is actually doing so the student can reason about correctness, memory, and runtime behavior.",
        "family": "js-internals",
        "foundations": [
            "JavaScript Fundamentals",
            "Functions and Abstractions",
            "Objects, Prototypes, and Classes",
        ],
        "topics": [
            "Execution Context and the JavaScript Runtime",
            "Call Stack, Stack Frames, and Recursion",
            "Memory Management in JavaScript",
            "Garbage Collection",
            "Closures and Lexical Environments",
            "this Binding and Object Invocation",
            "Prototype Chain and Object Delegation",
            "Iterators, Generators, and Iteration Protocols",
            "Functional Programming in JavaScript",
            "Object-Oriented Design in JavaScript",
        ],
    },
    {
        "name": "The Browser Runtime and Core Web APIs",
        "theme": "Connect the language runtime to the DOM, the event system, storage, history, and the network APIs used every day.",
        "family": "browser",
        "foundations": [
            "Browsers and Rendering Engines",
            "JavaScript Fundamentals",
            "Execution Context and the JavaScript Runtime",
        ],
        "topics": [
            "Event Loop and Task Queues",
            "Concurrency, Parallelism, and the Browser",
            "Callbacks, Promises, and Async Await",
            "Fetch, Streams, and Networking APIs",
            "DOM Fundamentals",
            "DOM Manipulation and Traversal",
            "Events, Propagation, and Delegation",
            "Browser Storage, Cookies, and IndexedDB",
            "History, Navigation, and the URL API",
            "Browser APIs and Capabilities",
        ],
    },
    {
        "name": "Advanced Browser Platform Features",
        "theme": "Teach the capabilities that make the browser a serious application platform rather than a passive document viewer.",
        "family": "platform",
        "foundations": [
            "Browser APIs and Capabilities",
            "DOM Fundamentals",
            "Event Loop and Task Queues",
        ],
        "topics": [
            "Canvas and SVG",
            "Clipboard, Drag and Drop, and File APIs",
            "Web Workers and Background Processing",
            "Service Workers and Offline Architectures",
            "Progressive Web Apps",
            "Web Components, Custom Elements, and Shadow DOM",
            "Observers: Intersection, Mutation, and Resize",
            "Notifications, Permissions, and Device APIs",
            "WebAssembly for Frontend Engineers",
            "Browser Internals and Process Architecture",
        ],
    },
    {
        "name": "TypeScript and Frontend Tooling",
        "theme": "Explain the development machinery that turns source code into dependable browser bundles and safer codebases.",
        "family": "tooling",
        "foundations": [
            "JavaScript Fundamentals",
            "Modules, Packages, and the JavaScript Ecosystem",
            "Command Line and Unix Thinking",
        ],
        "topics": [
            "TypeScript Fundamentals",
            "Types and Type Inference",
            "Generics, Utility Types, and Advanced Types",
            "Build Tools and Development Servers",
            "Package Managers: npm, pnpm, and Yarn",
            "Module Bundlers: Webpack, Rollup, and ESBuild",
            "Transpilers, Compilers, and Babel",
            "Linters, Formatters, and Static Analysis",
            "Environment Variables, Configuration, and Secrets",
            "Debugging and Browser DevTools",
        ],
    },
    {
        "name": "Version Control, Collaboration, and Testing",
        "theme": "Build the engineering habits that make teams fast, safe, and trustworthy.",
        "family": "testing",
        "foundations": [
            "Command Line and Unix Thinking",
            "JavaScript Fundamentals",
            "Debugging and Browser DevTools",
        ],
        "topics": [
            "Git Fundamentals",
            "Branching, Merging, and Rebasing",
            "GitHub Collaboration and Open Source Workflows",
            "Testing Fundamentals",
            "Unit Testing",
            "Integration Testing",
            "End-to-End Testing",
            "Test-Driven Development",
            "Accessibility and Visual Testing",
            "Performance Testing and Profiling",
        ],
    },
    {
        "name": "Performance, Rendering, and Discoverability",
        "theme": "Teach how pixels get to the screen quickly and how applications stay observable, searchable, and resilient.",
        "family": "performance",
        "foundations": [
            "Browsers and Rendering Engines",
            "Fetch, Streams, and Networking APIs",
            "CSS Fundamentals",
        ],
        "topics": [
            "Performance Fundamentals",
            "Critical Rendering Path",
            "Rendering Pipeline, Layout, Paint, and Compositing",
            "Reflow, Repaint, and Layout Thrashing",
            "Code Splitting, Lazy Loading, and Prioritization",
            "Image, Font, and Asset Optimization",
            "Caching, Compression, and CDNs",
            "Web Performance Metrics and Core Web Vitals",
            "SEO, Metadata, and Structured Data",
            "Observability, Monitoring, and Logging for Frontends",
        ],
    },
    {
        "name": "Security, Identity, and Privacy",
        "theme": "Teach the threat models and defensive practices needed to ship web software responsibly.",
        "family": "security",
        "foundations": [
            "HTTP and HTTPS",
            "Browser Storage, Cookies, and IndexedDB",
            "JavaScript Fundamentals",
        ],
        "topics": [
            "Web Security Fundamentals",
            "Same-Origin Policy, CORS, and CSP",
            "Cross-Site Scripting and Content Injection",
            "CSRF, Clickjacking, and UI Redressing",
            "Authentication and Session Management",
            "Authorization and Access Control",
            "JWT, OAuth, and OpenID Connect",
            "Secure Storage, Privacy, and Compliance",
            "Threat Modeling and Secure Coding",
            "Browser Security Architecture",
        ],
    },
    {
        "name": "Design, UX, Accessibility, and Content",
        "theme": "Expand beyond implementation to the human factors that make products understandable, inclusive, and trustworthy.",
        "family": "design",
        "foundations": [
            "Semantic HTML",
            "Accessibility Foundations",
            "CSS Fundamentals",
        ],
        "topics": [
            "Design Fundamentals for Engineers",
            "UI Principles and Visual Hierarchy",
            "UX Research, Information Architecture, and Content",
            "Color Theory and Contrast",
            "Typography Principles and Readability",
            "Layout Composition and Spacing Systems",
            "Component Design and API Design",
            "Accessibility Engineering and Inclusive Design",
            "Localization, Internationalization, and BiDi",
            "Design Systems Governance and Documentation",
        ],
    },
    {
        "name": "Frontend Architecture and State",
        "theme": "Move from components to systems by teaching rendering strategies, state boundaries, and maintainable frontend structures.",
        "family": "architecture",
        "foundations": [
            "Design Systems and Tokens",
            "JavaScript Fundamentals",
            "TypeScript Fundamentals",
        ],
        "topics": [
            "State Management Principles",
            "Client-Side Routing and Navigation Architecture",
            "Rendering Strategies: CSR, SSR, SSG, and ISR",
            "Hydration, Resumability, and Islands",
            "Reactivity Models, Virtual DOM, and Signals",
            "Framework Architecture and Trade-offs",
            "Component-Driven Development",
            "Micro Frontends and Federated UI",
            "Frontend Architecture Patterns",
            "Clean Code, Refactoring, and Maintainability",
        ],
    },
    {
        "name": "Modern Frameworks",
        "theme": "Teach popular framework mental models while comparing how different systems manage state, rendering, styling, and data.",
        "family": "framework",
        "foundations": [
            "State Management Principles",
            "Reactivity Models, Virtual DOM, and Signals",
            "Framework Architecture and Trade-offs",
        ],
        "topics": [
            "React Fundamentals",
            "React State, Effects, and Data Flow",
            "React Rendering, Reconciliation, and Performance",
            "Next.js and Full-Stack React",
            "Vue Fundamentals",
            "Angular Fundamentals",
            "Svelte and Compiler-Driven UI",
            "State Libraries and Server State",
            "Styling Strategies in Modern Frameworks",
            "Frontend Testing in Framework Applications",
        ],
    },
    {
        "name": "Data, Delivery, and Production Operations",
        "theme": "Connect frontend applications to APIs, real-time systems, deployment workflows, and operational maturity.",
        "family": "delivery",
        "foundations": [
            "Fetch, Streams, and Networking APIs",
            "State Management Principles",
            "GitHub Collaboration and Open Source Workflows",
        ],
        "topics": [
            "API Design for Frontend Consumers",
            "REST, GraphQL, and RPC from the Client",
            "Real-Time Systems, WebSockets, SSE, and Streaming",
            "Data Fetching, Caching, and Synchronization",
            "Forms, Mutations, and Optimistic UI",
            "Edge Computing, CDNs, and Distributed Frontend Delivery",
            "Deployment Environments and Release Management",
            "CI CD for Frontend Applications",
            "Feature Flags, Experimentation, and Rollouts",
            "Incidents, Debugging Production, and Postmortems",
        ],
    },
    {
        "name": "Computer Science, Scale, and System Design",
        "theme": "Develop the deeper analytical toolkit needed for complex applications and senior-level architecture work.",
        "family": "systems",
        "foundations": [
            "Computer Science for Frontend Engineers",
            "Performance Fundamentals",
            "Frontend Architecture Patterns",
        ],
        "topics": [
            "Data Structures for UI Engineers",
            "Algorithms and Complexity",
            "Compiler and Parser Basics",
            "Databases, Data Modeling, and Client Storage",
            "Scalability, Reliability, and Resilience",
            "System Design for Frontend Engineers",
            "Distributed Systems for Product Engineers",
            "Browser-Based Graphics and Rendering Architectures",
            "AI Integration in Frontend Products",
            "Technical Communication and Leadership",
        ],
    },
    {
        "name": "Professional Practice and the Future of the Web",
        "theme": "Prepare the learner to lead projects, communicate decisions, ship sustainably, and keep pace with change.",
        "family": "professional",
        "foundations": [
            "Technical Communication and Leadership",
            "System Design for Frontend Engineers",
            "GitHub Collaboration and Open Source Workflows",
        ],
        "topics": [
            "Software Engineering Best Practices",
            "Code Reviews, Mentoring, and Teamwork",
            "Documentation, ADRs, and RFCs",
            "Versioning, Release Trains, and Change Management",
            "Product Thinking and Experimentation",
            "Business Metrics, Analytics, and Decision Making",
            "Career Growth and Staff-Level Impact",
            "Capstone System Design Studio",
            "Open Source Contribution and Community Practice",
            "Emerging Web Standards",
        ],
    },
]


FAMILY_DATA = {
    "foundations": {
        "domain": "computing, machines, and networks",
        "inputs": "physical signals, bytes, protocol rules, and program state",
        "outputs": "delivered resources, computed results, and measurable latency",
        "history": "The ideas in this family grew out of early computing, Unix, ARPANET, RFC culture, and the standardization work that turned isolated machines into a global network.",
        "analogy": "a combination of roads, postal systems, customs checkpoints, and warehouses that must all cooperate before a package reaches a destination",
        "metrics": "latency, throughput, packet loss, cache hit rate, and utilization",
        "risk": "misunderstanding failure modes, over-trusting happy paths, and treating the network as infinitely fast or reliable",
        "a11y": "users on low-end devices, metered networks, and assistive technology often feel infrastructure mistakes first",
        "references": [
            "RFC 9110 HTTP Semantics",
            "RFC 1034 and RFC 1035 for DNS",
            "The Linux Programming Interface",
            "Computer Systems: A Programmer's Perspective",
            "MDN Web Docs platform overviews",
        ],
    },
    "html": {
        "domain": "documents, semantics, and accessible structure",
        "inputs": "markup, attributes, document order, and user intent",
        "outputs": "DOM trees, accessible names, navigation affordances, and media playback surfaces",
        "history": "HTML evolved from a simple document linking format into the semantic backbone of applications, documents, forms, media players, and assistive experiences.",
        "analogy": "the blueprint and signage system for a public building where every room, label, entrance, and emergency route must make sense",
        "metrics": "document validity, semantic clarity, form completion rate, task success, and accessibility audit scores",
        "risk": "div soup, broken form controls, inaccessible names, and content that only works when JavaScript succeeds",
        "a11y": "this family is accessibility's foundation because screen readers, keyboard users, and search engines all start from structure",
        "references": [
            "WHATWG HTML Living Standard",
            "WAI-ARIA Authoring Practices",
            "MDN HTML guides",
            "WCAG 2.2",
            "Inclusive Components",
        ],
    },
    "css": {
        "domain": "style calculation, layout, and visual presentation",
        "inputs": "DOM structure, style rules, device constraints, and user preferences",
        "outputs": "computed values, layout boxes, painted layers, and animated transitions",
        "history": "CSS emerged to separate content from presentation, then expanded from simple styling into a sophisticated constraint and rendering language with responsive and component-scale capabilities.",
        "analogy": "urban planning for pixels where zoning rules, dimensions, flow, and movement determine how people experience a space",
        "metrics": "layout stability, readability, paint cost, reuse, and adaptability across viewports",
        "risk": "specificity wars, brittle breakpoints, layout hacks, and styles that fight user preferences",
        "a11y": "good CSS respects zoom, contrast, reduced motion, logical order, and content readability",
        "references": [
            "MDN CSS reference",
            "CSS Cascading and Inheritance Level 5",
            "CSS Display and Box Alignment specs",
            "Every Layout",
            "web.dev layout and responsive design guides",
        ],
    },
    "javascript": {
        "domain": "programming logic and application behavior",
        "inputs": "values, control flow, functions, and state transitions",
        "outputs": "computed results, side effects, and reusable abstractions",
        "history": "JavaScript began as a lightweight scripting language and became the dominant language of frontend tooling, browser applications, and increasingly the full web stack.",
        "analogy": "a workshop full of tools where functions are jigs, data structures are materials, and control flow is the production process",
        "metrics": "correctness, clarity, cyclomatic complexity, mutation rate, and testability",
        "risk": "implicit coercion, accidental globals, brittle abstractions, and unreadable control flow",
        "a11y": "JavaScript should enhance experiences rather than block content, focus movement, or keyboard interaction",
        "references": [
            "ECMA-262",
            "MDN JavaScript guide",
            "You Don't Know JS Yet",
            "JavaScript: The Definitive Guide",
            "Exploring JS",
        ],
    },
    "js-internals": {
        "domain": "language runtime semantics, memory, and execution behavior",
        "inputs": "source code, lexical scope, call sites, and heap allocations",
        "outputs": "stack frames, closures, objects, garbage, and scheduled work",
        "history": "As applications became richer, developers had to understand why seemingly simple code behaved differently under async scheduling, memory pressure, and engine optimization.",
        "analogy": "a theater backstage system where actors, props, cues, and storage all have to be tracked precisely while the show continues",
        "metrics": "allocation rate, pause time, stack depth, deoptimization, and observable event latency",
        "risk": "memory leaks, stale closures, incorrect this binding, recursion errors, and accidental shared mutation",
        "a11y": "runtime mistakes often surface as frozen UIs, delayed announcements, lost focus, and broken assistive workflows",
        "references": [
            "ECMA-262 execution semantics",
            "V8 blog posts on memory and optimization",
            "MDN closures and prototype guides",
            "JavaScript engine talks from BlinkOn and JSConf",
            "Web Performance Working Group resources",
        ],
    },
    "browser": {
        "domain": "the DOM, event system, navigation, storage, and network integration",
        "inputs": "user input, markup, scripts, network responses, and browser events",
        "outputs": "interactive documents, event dispatch, persisted state, and navigable history",
        "history": "The browser transformed from a document viewer into an operating environment with a DOM, event system, storage APIs, and asynchronous networking primitives.",
        "analogy": "a busy control room where sensors, buttons, queues, and message lines coordinate one shared interface",
        "metrics": "interaction latency, event handler cost, storage reliability, and navigation correctness",
        "risk": "event storms, stale DOM references, storage corruption, race conditions, and history traps",
        "a11y": "input events, focus changes, and persisted preferences must all work for keyboards, switch devices, screen readers, and reduced-capability devices",
        "references": [
            "MDN DOM and Web API guides",
            "WHATWG DOM Standard",
            "HTML navigation and history sections",
            "web.dev eventing and storage guides",
            "Chrome Developers articles on browser APIs",
        ],
    },
    "platform": {
        "domain": "advanced browser capabilities such as workers, service workers, graphics, components, and device integration",
        "inputs": "messages, pixels, user grants, caches, and browser-managed processes",
        "outputs": "offline experiences, background computation, custom UI primitives, and richer platform integrations",
        "history": "HTML5 and subsequent platform work expanded the browser into a serious application runtime with graphics, local processing, installability, and encapsulation.",
        "analogy": "adding specialized rooms to a workshop: a paint booth, an assembly robot, a storage room, and a front desk",
        "metrics": "main-thread relief, offline hit rate, graphics throughput, permission acceptance, and component reuse",
        "risk": "permission fatigue, cache confusion, thread messaging bugs, and isolated components that break usability",
        "a11y": "advanced capability should never mean hidden controls, inaccessible canvases, or offline paths that bypass inclusive UX",
        "references": [
            "MDN PWA, service worker, and worker docs",
            "W3C and WHATWG component specs",
            "web.dev PWA courses",
            "Canvas and SVG specs and tutorials",
            "Chrome platform status resources",
        ],
    },
    "tooling": {
        "domain": "type systems, build pipelines, configuration, and debugging tools",
        "inputs": "source files, configuration, dependency graphs, and compiler options",
        "outputs": "diagnostics, bundles, source maps, and reproducible builds",
        "history": "As frontend codebases grew, teams built compilers, bundlers, type systems, and linting workflows to tame scale and accelerate feedback loops.",
        "analogy": "an industrial assembly line where raw materials are inspected, cut, packaged, labeled, and tracked before shipping",
        "metrics": "build time, cache reuse, type coverage, warning count, and debugging fidelity",
        "risk": "config drift, hidden transpilation costs, dependency sprawl, and build chains that no one can explain",
        "a11y": "tooling quality matters because it protects semantics, catches regressions, and preserves debuggability in production",
        "references": [
            "TypeScript Handbook",
            "Vite and Webpack docs",
            "Babel docs",
            "ESBuild and Rollup docs",
            "Chrome DevTools docs",
        ],
    },
    "testing": {
        "domain": "verification, collaboration, and safe change management",
        "inputs": "requirements, code changes, assertions, fixtures, and repository history",
        "outputs": "confidence, reproducibility, documented intent, and controlled delivery",
        "history": "Version control and testing matured together because teams needed ways to coordinate change, undo mistakes, and prove that behavior remained correct.",
        "analogy": "a laboratory notebook paired with a quality-control line where every experiment and shipment must be traceable",
        "metrics": "test signal quality, review throughput, failure rate, branch health, and change lead time",
        "risk": "flaky tests, cargo-cult coverage, merge conflicts, and histories that hide the real story",
        "a11y": "collaboration practices should explicitly protect accessibility behavior instead of treating it as a manual afterthought",
        "references": [
            "Pro Git",
            "Testing Library guiding principles",
            "Playwright docs",
            "Jest and Vitest docs",
            "Google Testing Blog",
        ],
    },
    "performance": {
        "domain": "render speed, network efficiency, discoverability, and production observability",
        "inputs": "resource sizes, scheduling choices, rendering work, and real user telemetry",
        "outputs": "faster paints, stable interactions, better search visibility, and measurable production health",
        "history": "Performance engineering moved from niche optimization to a first-class discipline as mobile usage, Core Web Vitals, and search visibility became business-critical.",
        "analogy": "traffic engineering for a city where throughput, bottlenecks, and wayfinding shape every trip",
        "metrics": "LCP, INP, CLS, TTFB, cache hit rate, and error budgets",
        "risk": "optimizing the wrong layer, guessing instead of measuring, and sacrificing maintainability for tiny wins",
        "a11y": "slow experiences are inaccessible experiences, especially for users on constrained hardware or assistive software",
        "references": [
            "web.dev performance guides",
            "Core Web Vitals documentation",
            "High Performance Browser Networking",
            "MDN performance docs",
            "Google Search Central docs",
        ],
    },
    "security": {
        "domain": "trust boundaries, identity, defensive coding, and privacy",
        "inputs": "user data, tokens, origins, policies, and attacker-controlled input",
        "outputs": "safe sessions, constrained capabilities, auditable behavior, and reduced blast radius",
        "history": "Web security evolved as the platform grew more powerful, forcing browsers and application teams to continuously strengthen boundaries, policies, and identity flows.",
        "analogy": "running a secure public venue with badges, locks, safes, cameras, and clear rules for who can enter which room",
        "metrics": "incident count, vulnerability severity, token lifetime, policy coverage, and auditability",
        "risk": "assuming the client is trusted, exposing secrets, and shipping convenience features without a threat model",
        "a11y": "security should protect users without making legitimate use impossible for keyboard-only, low-vision, or international audiences",
        "references": [
            "OWASP Cheat Sheet Series",
            "MDN web security guides",
            "OAuth 2.1 drafts and OpenID Connect docs",
            "WebAppSec working group drafts",
            "Browser vendor security blogs",
        ],
    },
    "design": {
        "domain": "human-centered interface design, content, and inclusive experience quality",
        "inputs": "human goals, content hierarchy, visual constraints, and product context",
        "outputs": "usable flows, understandable interfaces, and accessible communication",
        "history": "Frontend engineering increasingly overlaps with HCI, content strategy, and design systems because implementation quality directly shapes user understanding.",
        "analogy": "museum curation where lighting, labels, pacing, and room layout determine whether visitors understand the exhibition",
        "metrics": "task completion, comprehension, error rate, readability, and inclusive reach",
        "risk": "pretty but confusing interfaces, inaccessible contrast, and component APIs that optimize convenience over comprehension",
        "a11y": "inclusive design is not a bolt-on; it is the operating principle of the whole family",
        "references": [
            "Laws of UX",
            "Refactoring UI",
            "Inclusive Design Principles",
            "WCAG 2.2",
            "Design Systems Handbook",
        ],
    },
    "architecture": {
        "domain": "state boundaries, rendering strategies, and scalable frontend structure",
        "inputs": "user interactions, data flow, rendering decisions, and team constraints",
        "outputs": "composable systems, predictable updates, and sustainable codebases",
        "history": "As single-page applications grew, teams needed stronger models for state, rendering, routing, and modularity to avoid entropy and rewrite cycles.",
        "analogy": "city planning for software neighborhoods where roads, zoning, utilities, and ownership boundaries must be coherent",
        "metrics": "change cost, defect rate, render churn, onboarding time, and deploy confidence",
        "risk": "global state sprawl, abstraction mania, leaky rendering boundaries, and architecture chosen for fashion rather than needs",
        "a11y": "architectural choices affect focus management, navigation semantics, hydration timing, and inclusive fallback behavior",
        "references": [
            "Patterns.dev",
            "Frontend Architecture for Design Systems",
            "React, Vue, and Angular architecture docs",
            "Martin Fowler on refactoring and modularity",
            "web.dev rendering strategy guides",
        ],
    },
    "framework": {
        "domain": "component models, reactivity, framework APIs, and application composition",
        "inputs": "state, props, templates, compiler output, and rendering rules",
        "outputs": "interactive components, scheduled updates, and framework-managed UI trees",
        "history": "Frameworks emerged to manage complexity, then diverged into runtime-driven, compiler-driven, and hybrid models with different trade-offs for ergonomics and performance.",
        "analogy": "different orchestras playing the same score with different conductors, notation systems, and rehearsal styles",
        "metrics": "render frequency, bundle size, developer velocity, and escape-hatch cost",
        "risk": "treating framework conventions as universal truth, fighting the framework, and hiding platform fundamentals under abstractions",
        "a11y": "framework ergonomics should help rather than obscure semantics, focus, and progressive enhancement",
        "references": [
            "React docs",
            "Next.js docs",
            "Vue docs",
            "Angular docs",
            "Svelte docs",
        ],
    },
    "delivery": {
        "domain": "API consumption, real-time data, deployment, experimentation, and production operations",
        "inputs": "requests, responses, release artifacts, telemetry, and user cohorts",
        "outputs": "shipped features, synchronized state, safe rollouts, and recoverable systems",
        "history": "Frontend teams became delivery teams as SPAs, Jamstack, edge runtimes, and continuous deployment pushed more operational responsibility to the client side.",
        "analogy": "running a restaurant with supply chains, a live dining room, reservation systems, and daily service operations",
        "metrics": "error rate, stale data rate, deployment success, rollback time, and experiment validity",
        "risk": "ignoring backpressure, hiding network failure, over-coupling releases, and deploying without recovery plans",
        "a11y": "loading states, optimistic updates, and production fallbacks must still communicate clearly and preserve control",
        "references": [
            "MDN Fetch and Streams docs",
            "GraphQL spec and docs",
            "Playwright and CI platform docs",
            "Cloudflare and Vercel edge docs",
            "SRE workbooks for incident and release practice",
        ],
    },
    "systems": {
        "domain": "data structures, algorithms, graphics, storage, and system design for large frontend products",
        "inputs": "data models, constraints, workloads, and architectural requirements",
        "outputs": "better asymptotic behavior, scalable designs, and deliberate trade-off analysis",
        "history": "Rich frontend applications forced client engineers to think more like systems engineers, balancing data structures, storage, graphics, and distributed concerns inside the browser.",
        "analogy": "civil engineering for software where load, shape, materials, and long-term maintenance all matter",
        "metrics": "time complexity, space complexity, throughput, failure isolation, and reliability",
        "risk": "using the wrong data structure, ignoring scale assumptions, and designing systems that work only for demos",
        "a11y": "scale decisions influence responsiveness, power usage, and the ability of assistive tools to keep up with the interface",
        "references": [
            "Introduction to Algorithms",
            "Designing Data-Intensive Applications",
            "Graphics and rendering texts",
            "MDN storage and performance docs",
            "System design references from major engineering blogs",
        ],
    },
    "professional": {
        "domain": "leadership, communication, decision quality, and sustained professional growth",
        "inputs": "requirements, trade-offs, organizational context, and evolving platform change",
        "outputs": "healthy teams, better decisions, durable systems, and long-term career leverage",
        "history": "Senior engineering is increasingly about systems of people and decisions, not just systems of code.",
        "analogy": "directing a long-running production where casting, rehearsal, notes, budgets, audience feedback, and future planning all matter",
        "metrics": "decision clarity, onboarding speed, change failure rate, team trust, and product impact",
        "risk": "local optimization, weak communication, undocumented decisions, and stagnation",
        "a11y": "strong teams institutionalize inclusion instead of relying on heroic individual effort",
        "references": [
            "Staff Engineer",
            "The Manager's Path",
            "Accelerate",
            "Engineering management and architecture blog essays",
            "W3C and WHATWG standards processes",
        ],
    },
}


DIAGRAMS = {
    "internet": """\
+---------+      +------+      +------+      +---------+
| Browser | ---> | DNS  | ---> | TLS  | ---> | Origin  |
+---------+      +------+      +------+      +---------+
     |                |             |              |
     |<-- cached? ----|             |              |
     |-------------------------------------------->|
     |<--------------- response bytes -------------|
""",
    "html": """\
HTML bytes
   |
   v
Tokenizer ---> Tree builder ---> DOM
   |                               |
   |                               v
Semantics -----------------> Accessibility tree
""",
    "css": """\
DOM -----------+
               |--> Style engine --> CSSOM --> Computed styles
CSS source ----+                               |
                                               v
                                         Layout boxes
                                               |
                                               v
                                             Pixels
""",
    "javascript": """\
Source code --> Parser --> AST --> Bytecode/JIT hints --> Execution
                                      |
                                      v
                              Values and objects
""",
    "js-internals": """\
Call Stack                Heap
+------------------+      +-----------------------------+
| global()         |      | closure env { value: 11 }   |
| createCounter()  | ---> | function next()             |
| next()           |      | object/prototype graph      |
+------------------+      +-----------------------------+
             |
             v
        Event loop queues future work
""",
    "dom-api": """\
User input --> Event target --> Capture --> Target --> Bubble
                                   |
                                   v
                              JS handler
                                   |
                                   v
                         DOM / network / storage side effect
""",
    "platform": """\
Main thread <---- postMessage ----> Worker thread
     |                                   |
     v                                   v
 DOM / UI                         CPU-heavy work

Service worker sits beside navigation and fetch:
Browser --> SW --> Cache / Network
""",
    "typescript": """\
.ts source --> Parser --> Type checker --> Emit / diagnostics
                  |             |
                  |             v
                  |       inferred constraints
                  v
             syntax tree
""",
    "tooling": """\
Source files --> Resolver --> Transformer --> Bundler --> Output assets
      |               |            |             |
      v               v            v             v
 package.json      aliases      source maps    chunks
""",
    "workflow": """\
Working tree --> Index --> Commit graph --> Remote
      |             |           |             |
      v             v           v             v
   edits         staged      history      collaboration
""",
    "testing": """\
Requirement --> Test case --> Execution --> Assertion --> Feedback
                    |             |
                    v             v
                 fixture       browser/app state
""",
    "performance": """\
Navigation
   |
   v
HTML --> CSS --> JS --> Layout --> Paint --> Composite --> Interaction
   |       |      |        |         |           |
   v       v      v        v         v           v
TTFB      CSSOM  parse    reflow    pixels      INP/CLS/LCP
""",
    "security": """\
User --> Browser --> Origin boundary --> App --> Data
            |             |              |
            |             v              v
            |         policy checks    auth checks
            v
        attacker input tries to cross trust boundary
""",
    "design": """\
User goal --> Information hierarchy --> Layout --> Copy --> Interaction --> Feedback
     |                |                    |           |           |            |
     v                v                    v           v           v            v
 mental model      grouping            spacing      labels      controls     confirmation
""",
    "architecture": """\
Route --> Data boundary --> State boundary --> Component tree --> Render output
   |            |                |                   |                 |
   v            v                v                   v                 v
 URL        loader/cache     local/global state   composition      hydration/update
""",
    "framework": """\
State change --> Framework scheduler --> Diff / compile result --> DOM patch
      |                   |                      |                    |
      v                   v                      v                    v
   props/store         batching            virtual tree or output    browser paint
""",
    "delivery": """\
Client --> API / stream --> cache --> UI
  |            |             |        |
  v            v             v        v
deploy ----> release ----> observe -> rollback if needed
""",
    "ops": """\
Source change --> CI --> verified artifact --> rollout --> observe --> rollback or continue
      |            |           |                |            |              |
      v            v           v                v            v              v
   commit       tests       build output     deployment    telemetry     incident response
""",
    "systems": """\
Input data --> Data structure --> Algorithm --> Storage / rendering --> User-perceived behavior
      |               |               |                 |                     |
      v               v               v                 v                     v
 workload        shape/lookup      complexity       reliability           latency
""",
    "professional": """\
Problem --> Constraints --> Proposal --> Review --> Decision --> Delivery --> Learning
   |            |             |            |           |            |            |
   v            v             v            v           v            v            v
 users       business      ADR/RFC      peers       owner      rollout      postmortem
""",
}


GLOSSARY = {
    "internet": {
        "Latency": "The time it takes for a message or resource to travel through the system.",
        "Throughput": "How much useful work or data the system can move in a given time window.",
        "Protocol": "An agreed set of rules that lets independent systems communicate.",
        "Origin": "The scheme, host, and port combination that identifies a web authority boundary.",
        "Cache": "A faster copy of data kept closer to the consumer.",
    },
    "html": {
        "DOM": "The in-memory tree representation of a parsed HTML document.",
        "Semantics": "Meaning encoded by choosing elements that describe content and relationships.",
        "Landmark": "A structural region that helps users and assistive tools navigate a page.",
        "Accessible name": "The human-readable label a browser exposes to assistive technology.",
        "Progressive enhancement": "Designing the core experience to work before advanced scripting succeeds.",
    },
    "css": {
        "Cascade": "The rule system that decides which style wins for an element and property.",
        "Computed value": "The normalized value the browser determines before layout and paint.",
        "Formatting context": "The local layout rules that govern how boxes behave relative to one another.",
        "Intrinsic size": "The size content naturally wants before external constraints are applied.",
        "Compositing": "Combining painted layers into the final pixels shown on screen.",
    },
    "javascript": {
        "Expression": "Code that produces a value.",
        "Statement": "Code that performs an action or controls evaluation order.",
        "Scope": "The region in which a binding name can be resolved.",
        "Abstraction": "A simplified interface that hides lower-level detail.",
        "Mutation": "Changing existing state rather than creating a new value.",
    },
    "js-internals": {
        "Execution context": "The engine record that tracks scope, this, and other runtime details for active code.",
        "Stack frame": "A slice of the call stack representing one active invocation.",
        "Heap": "The memory region used for longer-lived objects and closures.",
        "Closure": "A function packaged together with access to variables from its creation scope.",
        "Garbage collection": "Automatic recovery of memory that is no longer reachable.",
    },
    "dom-api": {
        "Event target": "The object that receives an event first.",
        "Propagation": "The path an event follows through capture, target, and bubble phases.",
        "Persistence": "Keeping state beyond a single function call or page lifecycle step.",
        "Navigation": "A browser transition from one URL state to another.",
        "Capability": "A browser-provided power such as storage, clipboard access, or network I/O.",
    },
    "platform": {
        "Worker": "A background JavaScript execution context separate from the main thread.",
        "Service worker": "A scriptable network proxy and cache coordinator for an origin.",
        "Shadow DOM": "A scoped subtree with encapsulated structure and styling boundaries.",
        "Permission": "A user-controlled gate that protects a sensitive browser capability.",
        "Progressive web app": "A web application that adopts installability, offline support, and app-like behavior.",
    },
    "typescript": {
        "Type inference": "The compiler's ability to derive a type without an explicit annotation.",
        "Union": "A type that can be one of several alternatives.",
        "Generic": "A reusable type or function parameterized over other types.",
        "Narrowing": "Using control flow to reduce the possible types of a value.",
        "Emit": "The JavaScript output produced after type-checking and transformation.",
    },
    "tooling": {
        "Bundler": "A tool that follows module imports and packages them into deployable assets.",
        "Transpilation": "Converting source code into a different but semantically similar target form.",
        "Source map": "A mapping that helps tools connect generated code back to the original source.",
        "Dependency graph": "The network of modules and packages required to build an application.",
        "Static analysis": "Inspecting code without executing it to catch defects or enforce conventions.",
    },
    "workflow": {
        "Working tree": "The current checkout of files on disk.",
        "Index": "Git's staging area between edited files and a commit.",
        "Commit": "An immutable snapshot plus metadata recorded in version control.",
        "Rebase": "Reapplying commits onto a new base to create a cleaner history.",
        "Pull request": "A reviewable proposal to merge a branch into a shared code line.",
    },
    "testing": {
        "Assertion": "A rule the test checks to determine whether behavior matches expectations.",
        "Fixture": "The known setup data or environment a test depends on.",
        "Mock": "A test double that simulates behavior and records interactions.",
        "Flake": "A test that passes or fails unpredictably without a real code change.",
        "Confidence": "The justified belief that code behaves correctly under relevant conditions.",
    },
    "performance": {
        "LCP": "Largest Contentful Paint, a measure of when the main content appears.",
        "INP": "Interaction to Next Paint, a measure of input responsiveness.",
        "CLS": "Cumulative Layout Shift, a measure of visual stability.",
        "Critical path": "The minimum set of work required before something useful can appear or become interactive.",
        "Budget": "A performance limit that guides engineering decisions before regressions happen.",
    },
    "security": {
        "Trust boundary": "The line where assumptions about safety and authority must be rechecked.",
        "Origin": "The web security boundary defined by scheme, host, and port.",
        "Token": "A bearer artifact used to represent identity or authorization claims.",
        "Attack surface": "All the places an attacker can attempt to influence a system.",
        "Defense in depth": "Using multiple protective layers so one failure does not become a breach.",
    },
    "design": {
        "Hierarchy": "The ordering of importance communicated by layout, size, and emphasis.",
        "Affordance": "A signal that suggests how an interface element can be used.",
        "Contrast": "A difference in luminance or color that improves distinction and readability.",
        "Cognitive load": "The amount of mental effort required to understand or use a system.",
        "Consistency": "Using familiar patterns so people can reuse existing knowledge.",
    },
    "architecture": {
        "Boundary": "A place where responsibility, ownership, or data flow changes shape.",
        "Hydration": "Connecting server-rendered HTML to client-side behavior.",
        "Reactivity": "Automatically updating outputs when dependencies change.",
        "Routing": "Mapping URLs and navigation intents to application state and views.",
        "Maintainability": "How easy a system is to understand, change, and verify over time.",
    },
    "framework": {
        "Component": "A reusable unit of UI plus the logic that supports it.",
        "Props": "Inputs passed into a component by its parent.",
        "State": "Data owned by a component or store that can change over time.",
        "Reconciliation": "A framework's process for deciding how UI changes map to real updates.",
        "Compiler": "A tool that transforms higher-level source into a more executable form.",
    },
    "delivery": {
        "Backpressure": "A signal that the system cannot safely process incoming work as fast as it arrives.",
        "Rollout": "A controlled release of new behavior to some or all users.",
        "Synchronization": "Keeping multiple views of the same data meaningfully aligned.",
        "Rollback": "Reverting a release to restore a known good state.",
        "Postmortem": "A written analysis of an incident, its causes, and how to prevent a repeat.",
    },
    "systems": {
        "Complexity": "How resource usage grows as inputs grow.",
        "Data structure": "A representation optimized for particular operations and access patterns.",
        "Reliability": "The probability that a system continues to perform its function correctly.",
        "Scalability": "The ability to handle growth without a proportional collapse in efficiency.",
        "Resilience": "The ability to recover from faults and continue serving useful work.",
    },
    "professional": {
        "ADR": "An architecture decision record that captures a decision and its context.",
        "RFC": "A design proposal intended for discussion and alignment before implementation.",
        "Change management": "The process of introducing change without unnecessary disruption.",
        "Staff impact": "The leverage created by decisions, systems, and team enablement rather than only individual code output.",
        "Standard": "A shared specification or norm that allows teams and technologies to interoperate.",
    },
}


REFERENCE_MAP = {
    "internet": "foundations",
    "html": "html",
    "css": "css",
    "javascript": "javascript",
    "js-internals": "js-internals",
    "dom-api": "browser",
    "platform": "platform",
    "typescript": "tooling",
    "tooling": "tooling",
    "workflow": "testing",
    "testing": "testing",
    "performance": "performance",
    "security": "security",
    "design": "design",
    "architecture": "architecture",
    "framework": "framework",
    "delivery": "delivery",
    "ops": "delivery",
    "systems": "systems",
    "professional": "professional",
}


STOP_WORDS = {
    "and",
    "the",
    "for",
    "of",
    "to",
    "in",
    "on",
    "with",
    "from",
    "a",
    "an",
    "cd",
    "ui",
}


@dataclass
class Topic:
    number: int
    module_number: int
    module_name: str
    module_theme: str
    family: str
    title: str
    filename: str
    local_index: int
    foundations: list[str]
    prerequisites: list[str]
    unlocks: list[str]
    difficulty: int
    study_hours: int
    practice_hours: int


def slugify(value: str) -> str:
    value = value.replace("&", " and ")
    value = value.replace("/", " ")
    value = value.replace(":", " ")
    value = value.replace(",", " ")
    value = value.replace(".", " ")
    value = value.replace("+", " plus ")
    value = value.replace("'", "")
    value = value.replace("(", " ")
    value = value.replace(")", " ")
    value = value.replace("BiDi", "bidi")
    value = value.replace("CI CD", "ci-cd")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    value = re.sub(r"-+", "-", value)
    return value


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    output = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            output.append(item)
    return output


def build_topics() -> list[Topic]:
    flattened: list[tuple[int, dict, int, str]] = []
    number = 1
    for module_number, module in enumerate(MODULES, start=1):
        for local_index, title in enumerate(module["topics"], start=1):
            flattened.append((number, module, local_index, title))
            number += 1

    title_lookup: dict[str, tuple[int, dict, int, str]] = {title: entry for entry in flattened for title in [entry[3]]}
    topics: list[Topic] = []
    for number, module, local_index, title in flattened:
        previous_same_module = [item[3] for item in flattened if item[1] is module and item[0] < number][-2:]
        previous_global = [item[3] for item in flattened if item[0] < number]
        prereq_candidates = list(module["foundations"]) + previous_same_module
        if not prereq_candidates and previous_global:
            prereq_candidates.append(previous_global[-1])
        prerequisites = dedupe([item for item in prereq_candidates if item != title])[:4]

        next_same_module = [item[3] for item in flattened if item[1] is module and item[0] > number][:2]
        next_global = [item[3] for item in flattened if item[0] > number]
        unlock_candidates = next_same_module[:]
        if next_global:
            unlock_candidates.append(next_global[0])
        unlocks = dedupe([item for item in unlock_candidates if item != title])[:4]

        difficulty = min(10, 2 + (module["topics"].index(title) // 3) + ((MODULES.index(module)) // 2))
        study_hours = min(9, max(3, 2 + difficulty // 2))
        practice_hours = min(12, study_hours + 2 + (1 if difficulty >= 7 else 0))

        topics.append(
            Topic(
                number=number,
                module_number=MODULES.index(module) + 1,
                module_name=module["name"],
                module_theme=module["theme"],
                family=module["family"],
                title=title,
                filename=f"{number:03d}-{slugify(title)}.md",
                local_index=local_index,
                foundations=list(module["foundations"]),
                prerequisites=prerequisites,
                unlocks=unlocks,
                difficulty=difficulty,
                study_hours=study_hours,
                practice_hours=practice_hours,
            )
        )

    return topics


def kind_for_topic(title: str, family: str) -> str:
    lower = title.lower()
    if any(term in lower for term in ["internet", "client-server", "network", "dns", "http", "https", "tcp", "tls", "socket"]):
        return "internet"
    if any(term in lower for term in ["html", "semantic", "forms", "validation", "document structure", "landmarks", "links", "navigation", "url", "media", "images", "audio", "video", "aria", "assistive"]):
        return "html"
    if any(term in lower for term in ["css", "selectors", "specificity", "cascade", "units", "box model", "display", "positioning", "stacking", "typography", "colors", "backgrounds", "gradients", "borders", "shadows", "visual effects", "flexbox", "grid", "floats", "overflow", "scrolling", "responsive", "media queries", "container queries", "transforms", "transitions", "animations", "design systems", "tokens"]):
        return "css"
    if any(term in lower for term in ["javascript fundamentals", "data types", "values", "variables", "scope", "hoisting", "operators", "control flow", "functions", "abstractions", "objects", "arrays", "strings", "collections", "dates", "internationalization", "defensive programming", "modules, packages"]):
        return "javascript"
    if any(term in lower for term in ["execution context", "call stack", "memory management", "garbage collection", "closures", "lexical", "this binding", "prototype chain", "iterators", "generators", "functional programming", "object-oriented design"]):
        return "js-internals"
    if any(term in lower for term in ["dom", "events", "delegation", "fetch", "streams", "browser storage", "cookies", "indexeddb", "history", "browser apis"]):
        return "dom-api"
    if any(term in lower for term in ["canvas", "svg", "workers", "service workers", "progressive web apps", "web components", "shadow dom", "notifications", "permissions", "webassembly", "process architecture"]):
        return "platform"
    if "typescript" in lower or "type inference" in lower or "utility types" in lower or "advanced types" in lower:
        return "typescript"
    if any(term in lower for term in ["build tools", "package managers", "bundlers", "webpack", "rollup", "esbuild", "transpilers", "babel", "linters", "formatters", "static analysis", "environment variables", "devtools"]):
        return "tooling"
    if any(term in lower for term in ["git", "github", "branching", "merging", "rebasing", "versioning", "release trains", "open source contribution"]):
        return "workflow"
    if "test" in lower or "testing" in lower or "profiling" in lower:
        return "testing"
    if any(term in lower for term in ["performance", "rendering", "critical rendering path", "reflow", "repaint", "layout thrashing", "code splitting", "lazy loading", "image", "font", "asset optimization", "caching", "compression", "cdns", "core web vitals", "seo", "metadata", "structured data", "observability", "monitoring", "logging"]):
        return "performance"
    if any(term in lower for term in ["security", "same-origin", "cors", "csp", "cross-site scripting", "csrf", "clickjacking", "authentication", "authorization", "jwt", "oauth", "openid", "privacy", "threat"]):
        return "security"
    if any(term in lower for term in ["design", "ui", "ux", "color theory", "typography principles", "layout composition", "spacing systems", "component design", "inclusive design", "localization", "bidi"]):
        return "design"
    if any(term in lower for term in ["state management", "routing", "rendering strategies", "hydration", "resumability", "islands", "reactivity", "virtual dom", "signals", "framework architecture", "component-driven", "micro frontends", "frontend architecture", "clean code", "maintainability"]):
        return "architecture"
    if any(term in lower for term in ["react", "next.js", "vue", "angular", "svelte", "server state", "framework applications"]):
        return "framework"
    if any(term in lower for term in ["api design", "rest", "graphql", "rpc", "real-time", "websockets", "streaming", "data fetching", "optimistic ui", "edge computing", "deployment", "ci cd", "feature flags", "incidents", "postmortems"]):
        if any(term in lower for term in ["deployment", "ci cd", "feature flags", "incidents", "postmortems"]):
            return "ops"
        return "delivery"
    if any(term in lower for term in ["data structures", "algorithms", "compiler", "parser", "databases", "scalability", "reliability", "resilience", "system design", "distributed systems", "graphics", "ai integration"]):
        return "systems"
    if family == "professional":
        return "professional"
    return {
        "foundations": "internet",
        "html": "html",
        "css": "css",
        "javascript": "javascript",
        "js-internals": "js-internals",
        "browser": "dom-api",
        "platform": "platform",
        "tooling": "tooling",
        "testing": "testing",
        "performance": "performance",
        "security": "security",
        "design": "design",
        "architecture": "architecture",
        "framework": "framework",
        "delivery": "delivery",
        "systems": "systems",
        "professional": "professional",
    }[family]


def topic_keywords(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9]+", title.lower())
    output = []
    for word in words:
        if word not in STOP_WORDS and len(word) > 2:
            output.append(word)
    return output[:6]


def sentence_list(items: list[str]) -> str:
    if not items:
        return "none"
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def topic_link(title: str, topics_by_title: dict[str, Topic]) -> str:
    topic = topics_by_title[title]
    return f"[{topic.number:03d} {topic.title}]({topic.filename})"


def dependency_links(items: list[str], topics_by_title: dict[str, Topic]) -> str:
    if not items:
        return "None. This chapter is designed as a starting point."
    return ", ".join(topic_link(item, topics_by_title) for item in items)


def concept_dependencies(topic: Topic) -> list[str]:
    profile = FAMILY_DATA[topic.family]
    return [
        f"Understanding of {profile['inputs']}",
        "Comfort tracing cause and effect through a system",
        "Willingness to reason about edge cases, failure, and trade-offs",
    ]


def unlocked_concepts(topic: Topic, topics_by_title: dict[str, Topic]) -> list[str]:
    unlocks = [topic_link(item, topics_by_title) for item in topic.unlocks]
    unlocks.append(f"Deeper work in module {topic.module_number}: {topic.module_name}")
    return unlocks[:4]


def section_bullets(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def numbered(lines: list[str]) -> str:
    return "\n".join(f"{index}. {line}" for index, line in enumerate(lines, start=1))


def wrap(text: str) -> str:
    return textwrap.dedent(text).strip()


def example_bundle(kind: str, title: str) -> dict[str, str | list[str]]:
    bundles = {
        "internet": {
            "purpose": f"Trace how {title} turns a simple request into a network round-trip with observable success and failure states.",
            "language": "js",
            "code": wrap(
                """
                async function loadProfile() {
                  const response = await fetch("https://api.example.com/profile");
                  if (!response.ok) throw new Error(`HTTP ${response.status}`);
                  const profile = await response.json();
                  return { name: profile.name, plan: profile.plan };
                }

                loadProfile().then(console.log).catch(console.error);
                """
            ),
            "line_by_line": [
                "Line 1 defines an async function, which means the function immediately returns a promise to its caller.",
                "Line 2 asks the browser to create or reuse a connection and begin an HTTP request.",
                "Line 3 protects the happy path by converting non-success responses into explicit failures.",
                "Line 4 parses the response body stream into a JavaScript object.",
                "Line 5 returns a smaller object shaped for UI use rather than exposing the entire payload.",
                "Line 8 starts the work and attaches success and failure handlers so nothing is silently dropped.",
            ],
            "execution": [
                "The call to `loadProfile()` pushes a new stack frame and allocates a promise.",
                "The browser sends a request after DNS, connection setup, and security checks are satisfied.",
                "When bytes arrive, the promise is resolved or rejected and queued for microtask processing.",
                "The attached handlers run and log either the transformed data or the error.",
            ],
            "memory": wrap(
                """
                Network layer buffers:
                [request headers] -> [response headers] -> [body stream chunks]

                Application state:
                promise -> response object -> parsed profile object
                """
            ),
            "stack": wrap(
                """
                Call stack
                +----------------+
                | global script   |
                | loadProfile()   |
                +----------------+

                Microtask queue
                +------------------------------+
                | then(console.log)            |
                | catch(console.error)         |
                +------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap objects
                +-----------------------------------+
                | Promise                           |
                | Response                          |
                | { name: "...", plan: "..." }      |
                +-----------------------------------+
                """
            ),
            "runtime": "Most of the wall-clock cost is network latency rather than local CPU time. The browser spends local time scheduling, parsing headers, decoding JSON, and settling promises.",
            "time": "Local CPU work is O(n) in the size of the response body, but total latency is dominated by network round-trips and transfer size.",
            "space": "O(n) for the parsed response body plus small constant overhead for the promise and response wrapper.",
            "alternatives": "You could use `XMLHttpRequest`, a higher-level data client, or server rendering to move part of the work off the client.",
            "bugs": "Common bugs include forgetting error checks, parsing the wrong content type, ignoring cancellation, and assuming the network always resolves quickly.",
            "debug": "Use the Network panel to inspect DNS timing, TLS, status codes, headers, caching, and the response body. Reproduce with throttling turned on.",
            "refactor": "Move request creation, timeout policy, retry policy, and response validation into a shared API client instead of duplicating logic.",
            "best": "Normalize data at the boundary, surface failure explicitly, and keep browser-visible latency measurable.",
        },
        "html": {
            "purpose": f"Show how {title} combines structure, semantics, accessibility, and behavior in one minimal document.",
            "language": "html",
            "code": wrap(
                """
                <form id="signup-form">
                  <label for="email">Email</label>
                  <input id="email" name="email" type="email" required />
                  <button type="submit">Join</button>
                  <p id="status" aria-live="polite"></p>
                </form>
                <script>
                document.getElementById("signup-form").addEventListener("submit", (event) => {
                  event.preventDefault();
                  document.getElementById("status").textContent = "Submitted";
                });
                </script>
                """
            ),
            "line_by_line": [
                "Line 1 creates a form element, which gives the browser native submission semantics and keyboard behavior.",
                "Line 2 provides a programmatic label so the input has a clear accessible name.",
                "Line 3 declares validation and input semantics directly in HTML instead of only in JavaScript.",
                "Line 4 uses a real button so Enter-key submission and focus behavior come for free.",
                "Line 5 creates a live region so updates are announced by assistive technology.",
                "Lines 8 to 11 attach progressive enhancement: the form still exists even before the script runs.",
            ],
            "execution": [
                "The browser tokenizes the HTML and builds DOM nodes in document order.",
                "Accessibility relationships such as label-to-input and live-region behavior are derived from semantics and attributes.",
                "When the form submits, the event listener intercepts default navigation and updates the status text.",
                "The changed text becomes visible and may also be announced by assistive technology.",
            ],
            "memory": wrap(
                """
                DOM memory
                form
                ├── label
                ├── input
                ├── button
                └── p#status
                """
            ),
            "stack": wrap(
                """
                Call stack on submit
                +------------------------------+
                | submit listener callback     |
                | preventDefault()             |
                | textContent assignment       |
                +------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap / browser object graph
                +--------------------------------------+
                | DOM nodes                            |
                | Event listener function              |
                | Accessibility relationships metadata |
                +--------------------------------------+
                """
            ),
            "runtime": "The browser performs most of the heavy lifting: form semantics, validation affordances, focus rules, and live-region behavior are platform features, not custom code.",
            "time": "All local work is effectively O(1) for this tiny form, though full validation cost scales with the number of controls and rules.",
            "space": "O(n) in the number of DOM nodes and attached listeners.",
            "alternatives": "You could replace this with a div-based form shell, but you would then need to rebuild semantics, focus, submission, and announcement behavior manually.",
            "bugs": "Common bugs include missing labels, relying on placeholder text as a label, using clickable divs instead of buttons, and hiding validation state from screen readers.",
            "debug": "Inspect the Accessibility panel, tab through the form with a keyboard, and disable JavaScript to confirm the structure still makes sense.",
            "refactor": "Extract repeated field patterns into reusable semantic components without throwing away native behavior.",
            "best": "Prefer native elements first, then add behavior only where the platform does not already give you the correct semantics.",
        },
        "css": {
            "purpose": f"Demonstrate how {title} turns abstract style rules into a concrete layout and visual hierarchy.",
            "language": "html",
            "code": wrap(
                """
                <main class="layout">
                  <aside class="sidebar">Filters</aside>
                  <section class="content">Results</section>
                </main>
                <style>
                  .layout { display: grid; grid-template-columns: 16rem 1fr; gap: 1rem; }
                  .sidebar { position: sticky; top: 1rem; }
                  .content { min-height: 20rem; background: linear-gradient(#fff, #f3f6fb); }
                </style>
                """
            ),
            "line_by_line": [
                "Lines 1 to 3 create a simple DOM structure that the layout algorithm can reason about.",
                "Line 6 establishes a grid formatting context with one fixed track and one flexible track.",
                "Line 7 uses sticky positioning so the sidebar participates in flow until the scroll threshold is crossed.",
                "Line 8 adds a visual treatment without changing document structure.",
            ],
            "execution": [
                "The browser parses HTML into the DOM and CSS into the CSSOM.",
                "Selector matching assigns rules to elements and the cascade chooses winners.",
                "Computed values are resolved, then layout calculates box sizes and positions.",
                "Paint turns boxes into pixels and compositing assembles the final frame.",
            ],
            "memory": wrap(
                """
                Browser structures
                DOM ----------+
                               +--> Render tree --> Layout boxes
                CSSOM --------+
                """
            ),
            "stack": wrap(
                """
                Style / layout pipeline
                +-------------------------------+
                | style recalc                  |
                | layout                        |
                | paint                         |
                | composite                     |
                +-------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap-like engine objects
                +----------------------------------------+
                | element nodes                          |
                | matched rule sets                      |
                | computed style objects                 |
                | layout box tree                        |
                +----------------------------------------+
                """
            ),
            "runtime": "Most cost comes from style recalculation, layout, paint, and compositing rather than JavaScript execution. Small rule changes can have large rendering consequences.",
            "time": "Selector matching and layout are approximately proportional to the number of relevant nodes and rules, though browser engines use many optimizations.",
            "space": "O(n) in DOM nodes, style objects, and layout boxes.",
            "alternatives": "The same interface could be built with flexbox, floats, or absolute positioning, but each choice changes responsiveness and maintenance cost.",
            "bugs": "Common bugs include unintended overflow, specificity escalation, layout that depends on magic numbers, and animations that trigger layout on every frame.",
            "debug": "Use DevTools to inspect computed styles, box metrics, paint flashing, and layer composition. Toggle rules one by one.",
            "refactor": "Replace one-off values with tokens, collapse duplicate rules, and choose layout primitives that encode intent instead of hacks.",
            "best": "Author for resilience: let content size itself where possible, prefer composition over overrides, and respect user preferences.",
        },
        "javascript": {
            "purpose": f"Use a small data transformation to expose the core reasoning patterns behind {title}.",
            "language": "js",
            "code": wrap(
                """
                function groupOrdersByStatus(orders) {
                  return orders.reduce((groups, order) => {
                    const key = order.status ?? "unknown";
                    groups[key] = [...(groups[key] ?? []), order.id];
                    return groups;
                  }, {});
                }

                console.log(groupOrdersByStatus([{ id: 1, status: "paid" }, { id: 2, status: "pending" }]));
                """
            ),
            "line_by_line": [
                "Line 1 defines a function boundary and names the input clearly.",
                "Line 2 uses `reduce` to accumulate state rather than mutating external variables.",
                "Line 3 guards against missing data with nullish coalescing.",
                "Line 4 creates a new array for the target bucket and appends the current order id.",
                "Line 8 executes the function with a small sample to make behavior visible.",
            ],
            "execution": [
                "The function is stored in memory and later invoked with an array.",
                "Each array element becomes the current `order` parameter for one reducer call.",
                "The accumulator object grows new keys and arrays as needed.",
                "The final grouped object is logged to the console.",
            ],
            "memory": wrap(
                """
                Heap
                orders array --> order objects
                groups object --> arrays by status
                """
            ),
            "stack": wrap(
                """
                Call stack
                +------------------------------+
                | global()                     |
                | groupOrdersByStatus()        |
                | reducer callback             |
                +------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap objects
                +--------------------------------------+
                | [{ id: 1, ... }, { id: 2, ... }]     |
                | { paid: [1], pending: [2] }          |
                +--------------------------------------+
                """
            ),
            "runtime": "The work is synchronous and CPU-bound. For large arrays, allocation strategy and mutation choices affect garbage collection pressure and readability.",
            "time": "O(n) over the number of orders.",
            "space": "O(n) for the output object and its grouped arrays.",
            "alternatives": "A `for...of` loop is often simpler, while a Map can make key handling more explicit.",
            "bugs": "Common bugs include mutating shared objects unintentionally, using the wrong defaulting operator, and forgetting that arrays preserve insertion order.",
            "debug": "Log intermediate reducer states, step through the callback, and inspect variable scope in the debugger.",
            "refactor": "Extract the key selection logic, add type information, and avoid unnecessary array copying when immutability is not required.",
            "best": "Write transformations so the data flow is obvious and failure modes are easy to observe.",
        },
        "js-internals": {
            "purpose": f"Expose the runtime behavior behind {title} with a closure that survives across calls.",
            "language": "js",
            "code": wrap(
                """
                function createCounter(start = 0) {
                  let value = start;
                  return function next() {
                    value += 1;
                    return value;
                  };
                }

                const counter = createCounter(10);
                console.log(counter(), counter());
                """
            ),
            "line_by_line": [
                "Line 1 creates a function that allocates a new lexical environment each time it runs.",
                "Line 2 binds `value` in that environment.",
                "Lines 3 to 6 return an inner function that keeps access to the outer binding even after the outer call completes.",
                "Line 8 creates one specific counter instance with its own private state.",
                "Line 9 proves that the inner function retains and mutates that private state across calls.",
            ],
            "execution": [
                "Calling `createCounter(10)` creates a stack frame and a lexical environment.",
                "The inner function is allocated and stores a reference to the environment containing `value`.",
                "When `counter()` runs later, a new stack frame is created but it still points at the preserved environment.",
                "The engine updates `value` from 10 to 11 to 12 across successive calls.",
            ],
            "memory": wrap(
                """
                Lexical environment
                +--------------------+
                | value: 12          |
                +--------------------+
                retained by:
                function next()
                """
            ),
            "stack": wrap(
                """
                During counter()
                +---------------------------+
                | global()                  |
                | next()                    |
                +---------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +-------------------------------------+
                | function createCounter              |
                | function next                       |
                | closure environment { value: 12 }   |
                +-------------------------------------+
                """
            ),
            "runtime": "This example is tiny, but it illustrates why closures are powerful and why careless capture can accidentally keep large objects alive.",
            "time": "O(1) per call.",
            "space": "O(1) for one counter, though the closure keeps its environment alive until references are dropped.",
            "alternatives": "A class instance or plain object with methods can model the same state explicitly.",
            "bugs": "Common bugs include stale closures in UI frameworks, capturing loop variables incorrectly, and confusing shared versus instance-local state.",
            "debug": "Inspect closure variables in DevTools and watch what remains reachable after you think work has finished.",
            "refactor": "Promote state to a clearer abstraction if too much behavior becomes hidden inside one closure.",
            "best": "Use closure intentionally for encapsulation, not accidentally through convenience.",
        },
        "dom-api": {
            "purpose": f"Connect {title} to the real browser event, DOM, and network machinery developers touch every day.",
            "language": "html",
            "code": wrap(
                """
                <button id="load">Load profile</button>
                <pre id="output"></pre>
                <script>
                document.getElementById("load").addEventListener("click", async () => {
                  const response = await fetch("/api/profile");
                  const data = await response.json();
                  document.getElementById("output").textContent = JSON.stringify(data, null, 2);
                });
                </script>
                """
            ),
            "line_by_line": [
                "Line 1 defines a real focusable control that can be activated by mouse, touch, or keyboard.",
                "Line 2 reserves a DOM node that will hold the result.",
                "Line 4 attaches a click listener to the button rather than polling or inlining behavior.",
                "Line 5 initiates a fetch request when the user acts.",
                "Line 6 parses JSON into a JavaScript value.",
                "Line 7 updates the DOM with a serialized representation of the result.",
            ],
            "execution": [
                "The listener is registered during initial script evaluation.",
                "A click event is dispatched when the user activates the button.",
                "The async handler pauses at the `await` while the browser performs network I/O.",
                "When the promise settles, the handler resumes and mutates the DOM.",
            ],
            "memory": wrap(
                """
                DOM
                button#load
                pre#output

                JS
                listener -> promise -> parsed JSON object
                """
            ),
            "stack": wrap(
                """
                Call stack after click
                +----------------------------+
                | click handler              |
                | fetch continuation later   |
                +----------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap / browser-managed objects
                +---------------------------------+
                | button element                  |
                | pre element                     |
                | event listener                  |
                | Response and parsed data        |
                +---------------------------------+
                """
            ),
            "runtime": "This example spans both browser-managed state and application-managed state. Timing is event-driven and partially controlled by the network.",
            "time": "Local work is O(n) in the size of the JSON stringification; total latency is dominated by the network.",
            "space": "O(n) for the parsed object and rendered JSON text.",
            "alternatives": "A data library can manage caching and retries, while server rendering can move the initial fetch off the client.",
            "bugs": "Common bugs include double requests, stale UI updates after navigation, and event handlers attached to disappearing nodes.",
            "debug": "Inspect event listeners, network waterfalls, DOM breakpoints, and async stacks in DevTools.",
            "refactor": "Separate data loading, state representation, and DOM rendering to keep the code explainable.",
            "best": "Let the browser handle what it already does well, and make your own state transitions explicit.",
        },
        "platform": {
            "purpose": f"Show how {title} uses browser capabilities beyond the main thread and standard document flow.",
            "language": "js",
            "code": wrap(
                """
                // main.js
                const worker = new Worker("/worker.js");
                worker.postMessage([4, 7, 9]);
                worker.onmessage = ({ data }) => console.log(data.total);

                // worker.js
                self.onmessage = ({ data }) => {
                  const total = data.reduce((sum, value) => sum + value, 0);
                  self.postMessage({ total });
                };
                """
            ),
            "line_by_line": [
                "Line 2 creates a separate execution context managed by the browser.",
                "Line 3 sends structured-clone data to the worker instead of sharing the same call stack.",
                "Line 4 subscribes to the worker's reply.",
                "Lines 7 to 10 define the worker-side message handler and return a computed result.",
            ],
            "execution": [
                "The main thread creates the worker and hands it a URL.",
                "The browser starts a separate context and evaluates `worker.js` there.",
                "Messages cross the thread boundary by cloning or transferring data.",
                "The worker computes the total without blocking the main thread and posts the result back.",
            ],
            "memory": wrap(
                """
                Main thread heap          Worker heap
                [Worker object]           [data array clone]
                [message handler]         [reduce callback]
                """
            ),
            "stack": wrap(
                """
                Main thread stack         Worker stack
                +----------------+        +----------------+
                | global()       |        | onmessage()    |
                +----------------+        +----------------+
                """
            ),
            "heap": wrap(
                """
                Separate heaps
                +------------------------------+   +---------------------------+
                | main thread objects          |   | worker thread objects     |
                +------------------------------+   +---------------------------+
                """
            ),
            "runtime": "The browser isolates execution contexts for safety and responsiveness. Message passing is cheaper than blocking the main thread with long CPU work.",
            "time": "O(n) over the array length in the worker, plus fixed messaging overhead.",
            "space": "O(n) for the transferred or cloned payload.",
            "alternatives": "For tiny calculations, main-thread execution is simpler. For shared memory, SharedArrayBuffer can be used with stricter security constraints.",
            "bugs": "Common bugs include assuming shared mutable state, forgetting to terminate workers, and caching stale service worker assets indefinitely.",
            "debug": "Use worker inspection tools, application cache views, and performance traces to confirm work actually moved off the main thread.",
            "refactor": "Define a message protocol and isolate heavy logic so the worker boundary stays explicit and testable.",
            "best": "Use advanced APIs where they meaningfully change capability or responsiveness, not just because they are available.",
        },
        "typescript": {
            "purpose": f"Use a typed state model to show how {title} makes invalid states harder to represent.",
            "language": "ts",
            "code": wrap(
                """
                type ApiState<T> =
                  | { status: "idle" }
                  | { status: "success"; data: T }
                  | { status: "error"; message: string };

                function renderMessage(state: ApiState<{ name: string }>) {
                  return state.status === "success" ? state.data.name : "Loading...";
                }
                """
            ),
            "line_by_line": [
                "Lines 1 to 4 define a discriminated union that models mutually exclusive states.",
                "Line 6 makes the expected state shape explicit to readers and tooling.",
                "Line 7 narrows the union using the `status` field before accessing `data`.",
            ],
            "execution": [
                "The TypeScript compiler parses the source and builds a syntax tree.",
                "The checker validates that `data` is only read when the type has been narrowed to the success case.",
                "At runtime, only the resulting JavaScript conditional remains; the type information has already done its job.",
            ],
            "memory": wrap(
                """
                Compiler structures
                syntax tree -> symbol table -> inferred union relationships
                """
            ),
            "stack": wrap(
                """
                Runtime stack
                +---------------------------+
                | renderMessage()           |
                +---------------------------+
                """
            ),
            "heap": wrap(
                """
                Runtime heap
                +---------------------------------+
                | state object                    |
                | optional nested data object     |
                +---------------------------------+
                """
            ),
            "runtime": "The big win is pre-runtime. TypeScript turns potential runtime mistakes into compile-time feedback without adding significant runtime cost.",
            "time": "Type-checking cost grows with project size, while runtime execution remains O(1) for this example.",
            "space": "Negligible runtime overhead beyond the actual JavaScript objects.",
            "alternatives": "JSDoc plus type checking, runtime schemas, or fully untyped JavaScript are alternatives with different feedback and enforcement trade-offs.",
            "bugs": "Common bugs include overly broad `any`, weak discriminants, and assuming type safety without validating untrusted runtime data.",
            "debug": "Inspect editor hover types, compiler output, and narrowing paths. If a type feels confusing, reduce the example until the checker behavior is obvious.",
            "refactor": "Extract state machines, use helper types, and make impossible states unrepresentable rather than adding comments that hope people remember.",
            "best": "Use types to encode domain truth, not just to appease the compiler.",
        },
        "tooling": {
            "purpose": f"Demonstrate how {title} turns developer intent into reproducible tooling behavior.",
            "language": "ts",
            "code": wrap(
                """
                import { defineConfig } from "vite";

                export default defineConfig({
                  server: { port: 3000 },
                  build: { sourcemap: true, target: "es2022" },
                });
                """
            ),
            "line_by_line": [
                "Line 1 imports a helper that gives the config file structure and editor support.",
                "Line 3 exports the configuration object that the tool will evaluate.",
                "Line 4 sets local development behavior.",
                "Line 5 sets production build behavior so output is both modern and debuggable.",
            ],
            "execution": [
                "Node loads the config file and evaluates it before the dev server or build begins.",
                "The tool reads the object, applies defaults, and constructs an internal pipeline.",
                "Source maps and targets then influence transformation, bundling, and debugging.",
            ],
            "memory": wrap(
                """
                Tool process memory
                config object -> normalized options -> plugin graph
                """
            ),
            "stack": wrap(
                """
                Call stack
                +-----------------------------+
                | CLI entrypoint              |
                | config loader               |
                | defineConfig()              |
                +-----------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +--------------------------------------+
                | config object                        |
                | plugin list                          |
                | resolver and bundler state           |
                +--------------------------------------+
                """
            ),
            "runtime": "Tooling often runs in Node rather than the browser, but the choices it makes shape the bundle, debugging experience, and runtime compatibility of browser code.",
            "time": "Usually O(n) in project files and dependency graph size, plus plugin-specific cost.",
            "space": "Proportional to the dependency graph, transformed modules, and source maps held during the build.",
            "alternatives": "Equivalent behavior can come from Webpack, Rollup, Parcel, or custom scripts, each with different ergonomics and plugin ecosystems.",
            "bugs": "Common bugs include mismatched targets, hidden polyfill gaps, and environment-dependent config behavior.",
            "debug": "Inspect generated bundles, source maps, and resolved config output. Run builds in CI to catch machine-specific assumptions.",
            "refactor": "Keep configuration layered, documented, and close to the actual problems it solves instead of accreting mystery flags.",
            "best": "Favor boring, explainable build chains that the whole team can debug.",
        },
        "workflow": {
            "purpose": f"Show how {title} preserves team intent and traceability through a simple version-control workflow.",
            "language": "sh",
            "code": wrap(
                """
                git checkout -b feature/profile-form
                git add src/profile-form.tsx
                git commit -m "Add accessible profile form"
                git rebase origin/main
                git push -u origin feature/profile-form
                """
            ),
            "line_by_line": [
                "Line 1 creates an isolated branch so work can evolve without destabilizing shared history.",
                "Line 2 stages only the intended file changes.",
                "Line 3 records an immutable snapshot with a message that explains intent.",
                "Line 4 reapplies local work onto the latest shared base to reduce integration surprises.",
                "Line 5 publishes the branch and establishes upstream tracking for collaboration.",
            ],
            "execution": [
                "Git updates HEAD to point at a new branch name.",
                "The index records which file contents will become the next commit.",
                "A commit object, tree object, and blob objects are written into the repository database.",
                "Rebase rewrites commit ancestry, then push transfers objects to the remote if they are missing there.",
            ],
            "memory": wrap(
                """
                Repository state
                working tree -> index -> commit graph -> remote refs
                """
            ),
            "stack": wrap(
                """
                Process stack
                shell -> git subcommand -> repository plumbing
                """
            ),
            "heap": wrap(
                """
                Persistent object graph
                +--------------------------------------+
                | commit -> tree -> blobs             |
                | refs and branch pointers            |
                +--------------------------------------+
                """
            ),
            "runtime": "The key runtime is the Git process itself and the repository object database on disk. The browser never sees Git directly, but users feel the effects of clean or chaotic collaboration.",
            "time": "Most commands are near O(changed files), while rebase or history scans scale with the number of affected commits.",
            "space": "Repository growth scales with stored objects, history, and packfiles.",
            "alternatives": "Merge-based workflows, trunk-based development, and stacked diffs all solve similar problems with different integration rhythms.",
            "bugs": "Common bugs include rebasing public history carelessly, staging unrelated files, and writing commit messages that explain neither intent nor risk.",
            "debug": "Use `git status`, `git log --graph`, and `git diff --staged` to inspect the exact state before publishing.",
            "refactor": "Split large changes into smaller, reviewable commits and branch scopes.",
            "best": "Treat history as a communication tool, not just a backup mechanism.",
        },
        "testing": {
            "purpose": f"Demonstrate how {title} turns expectations into executable feedback.",
            "language": "tsx",
            "code": wrap(
                """
                import { render, screen } from "@testing-library/react";
                import { ProfileCard } from "./ProfileCard";

                test("renders the customer name", () => {
                  render(<ProfileCard name="Ada" />);
                  expect(screen.getByText("Ada")).toBeVisible();
                });
                """
            ),
            "line_by_line": [
                "Line 1 imports a rendering utility that exercises the component the way a user would encounter it.",
                "Line 2 imports the unit under test instead of reaching into implementation details.",
                "Line 4 gives the test a human-readable statement of behavior.",
                "Line 5 renders the component with a realistic prop.",
                "Line 6 asserts on visible output rather than private state.",
            ],
            "execution": [
                "The test runner loads the module and creates an isolated test environment.",
                "Rendering mounts the component into a DOM-like container.",
                "The query searches for visible text, and the assertion passes or fails based on actual rendered output.",
            ],
            "memory": wrap(
                """
                Test environment
                rendered DOM -> query helpers -> assertion metadata
                """
            ),
            "stack": wrap(
                """
                Call stack
                +----------------------------+
                | test callback              |
                | render()                   |
                | query / assertion          |
                +----------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +--------------------------------------+
                | component props                      |
                | rendered node tree                   |
                | matcher objects                      |
                +--------------------------------------+
                """
            ),
            "runtime": "Test code is ordinary program execution with a specialized harness. The value comes from targeted feedback, not from maximizing line count.",
            "time": "Usually O(n) in rendered nodes and queried elements for this style of test.",
            "space": "O(n) in the size of the rendered output and test harness state.",
            "alternatives": "You can test through end-to-end flows, contract tests, or lower-level pure functions depending on the risk you want to cover.",
            "bugs": "Common bugs include over-mocking, testing implementation details, and allowing flakes to erode trust.",
            "debug": "Print the rendered DOM, run the test in watch mode, and reproduce failures with the smallest possible fixture.",
            "refactor": "Move repeated setup into helpers, but keep assertions specific enough that failures remain easy to interpret.",
            "best": "Write tests that explain behavior, not tests that merely touch code.",
        },
        "performance": {
            "purpose": f"Measure how {title} affects real user experience rather than guessing from intuition.",
            "language": "js",
            "code": wrap(
                """
                const observer = new PerformanceObserver((list) => {
                  for (const entry of list.getEntries()) {
                    console.log(entry.name, entry.startTime, entry.duration);
                  }
                });

                observer.observe({ type: "largest-contentful-paint", buffered: true });
                """
            ),
            "line_by_line": [
                "Line 1 creates an observer for browser-generated performance entries.",
                "Line 2 iterates through the entries the browser has collected.",
                "Line 3 logs useful timing fields so the event becomes visible to developers.",
                "Line 7 subscribes to one of the metrics that matters for user-perceived load.",
            ],
            "execution": [
                "The browser records timing entries as page work happens.",
                "When relevant entries are available, the observer callback runs asynchronously.",
                "The callback turns hidden browser metrics into application-visible data.",
            ],
            "memory": wrap(
                """
                Browser telemetry buffers
                [performance entries] -> observer callback -> analytics/logging
                """
            ),
            "stack": wrap(
                """
                Call stack when metrics flush
                +-------------------------------+
                | observer callback             |
                | console.log                   |
                +-------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +--------------------------------------+
                | PerformanceObserver                  |
                | entry list objects                   |
                +--------------------------------------+
                """
            ),
            "runtime": "Measurement code should be cheap and intentional; otherwise the act of measuring becomes part of the problem.",
            "time": "Observer handling is O(n) in the number of entries processed.",
            "space": "Small constant overhead plus any storage used for logs or analytics batching.",
            "alternatives": "Synthetic lab tools, browser traces, Real User Monitoring vendors, and framework profilers complement this low-level API.",
            "bugs": "Common bugs include reading metrics in the wrong lifecycle phase, sampling too little, and treating one device or one browser as universal truth.",
            "debug": "Correlate observer output with Lighthouse, DevTools traces, and real-device throttling.",
            "refactor": "Wrap metrics collection in a reusable telemetry layer and standardize naming and sampling.",
            "best": "Measure before, during, and after optimization so every change remains evidence-based.",
        },
        "security": {
            "purpose": f"Illustrate how {title} relies on explicit trust boundaries and defensive defaults.",
            "language": "js",
            "code": wrap(
                """
                async function updateProfile(input, csrfToken) {
                  const response = await fetch("/api/profile", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                      "X-CSRF-Token": csrfToken,
                    },
                    body: JSON.stringify(input),
                    credentials: "same-origin",
                  });
                  return response.ok;
                }
                """
            ),
            "line_by_line": [
                "Line 1 makes the trust-sensitive inputs explicit: user data plus a CSRF token.",
                "Line 3 chooses a state-changing method so the request semantics match intent.",
                "Lines 4 to 7 declare content type and attach an anti-CSRF header.",
                "Line 8 serializes input rather than concatenating unsafe strings.",
                "Line 9 scopes credential sending to the same origin.",
            ],
            "execution": [
                "The function assembles a request with explicit headers and credentials policy.",
                "The browser applies origin and transport rules before sending anything.",
                "The server can validate method, token, origin, and payload structure before mutating data.",
            ],
            "memory": wrap(
                """
                Sensitive data flow
                input object -> JSON body
                csrf token -> request header
                """
            ),
            "stack": wrap(
                """
                Call stack
                +-------------------------------+
                | updateProfile()               |
                | fetch()                       |
                +-------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +----------------------------------------+
                | request options object                 |
                | serialized payload string              |
                +----------------------------------------+
                """
            ),
            "runtime": "Security often looks like extra ceremony, but that ceremony creates auditable, enforceable boundaries between trustworthy and untrustworthy input.",
            "time": "Local cost is negligible; security checks mainly affect architecture and failure handling rather than asymptotic complexity.",
            "space": "O(n) for the request body and small constant overhead for headers.",
            "alternatives": "Cookie-only flows, signed requests, or same-site protections can complement this example, but they do not eliminate the need for layered defenses.",
            "bugs": "Common bugs include storing tokens in unsafe places, blindly trusting server responses, and rendering unsanitized HTML.",
            "debug": "Inspect request headers, cookies, CSP reports, and origin behavior in DevTools and browser security panels.",
            "refactor": "Centralize trusted fetch wrappers, validation, and policy configuration to avoid one-off exceptions scattered through the codebase.",
            "best": "Assume every boundary will be tested by mistakes or attackers, and make the safe path the default path.",
        },
        "design": {
            "purpose": f"Show how {title} combines structure, copy, and visual treatment to make intent obvious to users.",
            "language": "html",
            "code": wrap(
                """
                <button class="primary-action" type="button">
                  <span class="label">Send invoice</span>
                  <span class="meta">Takes about 10 seconds</span>
                </button>
                <style>
                  .primary-action { display: grid; gap: 0.25rem; padding: 1rem 1.25rem; }
                  .label { font-weight: 700; }
                  .meta { font-size: 0.875rem; opacity: 0.8; }
                </style>
                """
            ),
            "line_by_line": [
                "Line 1 uses a real button because semantics and affordance should align.",
                "Lines 2 and 3 separate primary intent from supportive context.",
                "Line 6 uses spacing to create hierarchy before color or motion is added.",
                "Line 7 emphasizes the main action through weight instead of only color.",
                "Line 8 keeps supporting detail legible but clearly secondary.",
            ],
            "execution": [
                "The browser parses structure first, then applies visual rules.",
                "Users scan label, context, and spacing before deciding whether to act.",
                "Assistive technology receives a meaningful control rather than a styled generic container.",
            ],
            "memory": wrap(
                """
                DOM structure
                button
                ├── span.label
                └── span.meta
                """
            ),
            "stack": wrap(
                """
                Rendering pipeline
                +-------------------------------+
                | parse                         |
                | style                         |
                | layout                        |
                | paint                         |
                +-------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap / engine objects
                +--------------------------------------+
                | DOM nodes                            |
                | computed style objects               |
                +--------------------------------------+
                """
            ),
            "runtime": "Even simple interface choices shape user understanding, confidence, and error rates. Design engineering is about encoding meaning, not merely decoration.",
            "time": "Local rendering cost is tiny; the more important metric is human time saved or wasted by the design.",
            "space": "Minimal browser memory beyond the small DOM and style objects.",
            "alternatives": "A link, menu item, or form submit button may be more appropriate depending on navigation, risk, and information architecture.",
            "bugs": "Common bugs include hiding essential context in tiny text, relying on color alone, and making every action look equally urgent.",
            "debug": "Test with real tasks, keyboard navigation, zoom, and a screen reader. Ask whether people understand the action before they click.",
            "refactor": "Promote repeated patterns into documented components and tokenized spacing, type, and color decisions.",
            "best": "Make intent obvious with hierarchy, language, and semantics before visual flourish.",
        },
        "architecture": {
            "purpose": f"Use a small state container to show how {title} organizes ownership, updates, and reasoning boundaries.",
            "language": "ts",
            "code": wrap(
                """
                type State = { count: number };
                type Action = { type: "increment" } | { type: "reset" };

                function reducer(state: State, action: Action): State {
                  if (action.type === "increment") return { count: state.count + 1 };
                  return { count: 0 };
                }
                """
            ),
            "line_by_line": [
                "Line 1 defines the owned state shape.",
                "Line 2 defines the allowed transitions rather than allowing arbitrary mutation.",
                "Line 4 centralizes update rules in one pure function.",
                "Line 5 handles one transition explicitly.",
                "Line 6 handles the fallback transition in a deterministic way.",
            ],
            "execution": [
                "A caller passes current state and an action into the reducer.",
                "The reducer computes the next state without mutating the old one.",
                "A rendering layer can then compare the old and new states to decide what to update.",
            ],
            "memory": wrap(
                """
                State snapshots
                previous state -> reducer -> next state
                """
            ),
            "stack": wrap(
                """
                Call stack
                +---------------------------+
                | dispatch()                |
                | reducer()                 |
                +---------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +-----------------------------------+
                | old state { count: 1 }           |
                | new state { count: 2 }           |
                +-----------------------------------+
                """
            ),
            "runtime": "Architecture is partly about runtime behavior and partly about change behavior. Pure transitions make both easier to reason about.",
            "time": "O(1) for this example, though real reducers may scale with the size of the state tree touched.",
            "space": "O(1) here, or O(changed data) when immutable copies are created in larger systems.",
            "alternatives": "Mutable stores, signals, event sourcing, and actor models all provide different update semantics and debugging trade-offs.",
            "bugs": "Common bugs include global state misuse, ambiguous ownership, and side effects hidden inside supposedly pure update logic.",
            "debug": "Trace state transitions as a timeline and confirm which component or route owns each piece of state.",
            "refactor": "Split reducers or stores by ownership boundaries rather than by file size alone.",
            "best": "Make state ownership boringly explicit so the rest of the application can be dynamic without becoming chaotic.",
        },
        "framework": {
            "purpose": f"Demonstrate how {title} packages state, rendering, and event handling into a component-level abstraction.",
            "language": "tsx",
            "code": wrap(
                """
                export function Counter() {
                  const [count, setCount] = useState(0);

                  return (
                    <button onClick={() => setCount((value) => value + 1)}>
                      Count: {count}
                    </button>
                  );
                }
                """
            ),
            "line_by_line": [
                "Line 1 declares a component boundary that the framework can mount and update.",
                "Line 2 allocates local state using the framework's state primitive.",
                "Lines 4 to 8 return a button whose event handler describes a state transition.",
                "Line 5 uses an updater function so the framework can safely handle queued updates.",
            ],
            "execution": [
                "The framework calls the component to produce a render description.",
                "The button is mounted into the DOM and wired to the framework's event system.",
                "On click, the framework records a state update, schedules work, re-runs the component, and patches the DOM.",
            ],
            "memory": wrap(
                """
                Framework state
                component instance -> state slot -> render output
                """
            ),
            "stack": wrap(
                """
                Render cycle stack
                +-------------------------------+
                | framework scheduler           |
                | Counter()                     |
                | event handler                 |
                +-------------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +--------------------------------------+
                | component instance metadata          |
                | state cell                           |
                | virtual/render output                |
                +--------------------------------------+
                """
            ),
            "runtime": "Frameworks add structure around platform primitives. The benefit is consistency and composition; the cost is extra abstraction and framework-specific rules.",
            "time": "O(1) for the state update itself, though reconciliation cost scales with affected subtree size.",
            "space": "Small per-component overhead for framework bookkeeping plus rendered output structures.",
            "alternatives": "Web components, fine-grained reactive systems, server-rendered templates, and compiler-first frameworks offer different trade-offs.",
            "bugs": "Common bugs include stale closures, effect misuse, unnecessary re-renders, and forgetting that browser semantics still matter under the framework.",
            "debug": "Use framework devtools, render highlighting, and profiling to inspect update paths and component ownership.",
            "refactor": "Split components by responsibility, isolate side effects, and prefer stable data flow over clever prop drilling workarounds.",
            "best": "Learn the framework's mental model deeply enough that you can tell when the platform should do more of the work.",
        },
        "delivery": {
            "purpose": f"Show how {title} connects frontend state to external systems that can fail, lag, or change independently.",
            "language": "ts",
            "code": wrap(
                """
                async function loadFeed(signal?: AbortSignal) {
                  const response = await fetch("/api/feed", { signal });
                  if (!response.ok) throw new Error("Could not load feed");
                  return response.json();
                }
                """
            ),
            "line_by_line": [
                "Line 1 exposes cancellation because real frontend data work must react to navigation and stale requests.",
                "Line 2 performs a request while passing the abort signal through.",
                "Line 3 normalizes failure into an exception so the caller must deal with it.",
                "Line 4 returns parsed data for higher-level state management.",
            ],
            "execution": [
                "The caller requests data, perhaps on route entry or user action.",
                "The browser sends a request and may later abort it if the signal fires.",
                "The caller can cache, retry, or render fallback UI based on the result.",
            ],
            "memory": wrap(
                """
                Data flow
                request promise -> response -> parsed feed entries
                """
            ),
            "stack": wrap(
                """
                Call stack
                +--------------------------+
                | loadFeed()               |
                | fetch()                  |
                +--------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +--------------------------------------+
                | AbortSignal                          |
                | request promise                      |
                | parsed JSON result                   |
                +--------------------------------------+
                """
            ),
            "runtime": "Frontend delivery work is dominated by coordination: request lifecycles, stale data, retries, cache invalidation, and rollout safety.",
            "time": "O(n) in payload size locally, but end-to-end latency depends mostly on the network and the upstream system.",
            "space": "O(n) for the parsed response and any cache layer storing it.",
            "alternatives": "Framework loaders, data fetching libraries, GraphQL clients, and stream-based protocols provide richer orchestration with more abstraction.",
            "bugs": "Common bugs include race conditions between requests, showing stale data after navigation, and retries that amplify an outage.",
            "debug": "Correlate request ids, cache state, feature flags, and deploy versions when investigating behavior in production.",
            "refactor": "Consolidate request policies into a client layer and make cache ownership explicit.",
            "best": "Design the unhappy path first: loading, stale, partial, failed, retried, and rolled-back states are the real system.",
        },
        "ops": {
            "purpose": f"Show how {title} turns frontend delivery into a repeatable and recoverable operational process.",
            "language": "yaml",
            "code": wrap(
                """
                name: frontend-ci
                on: [push]
                jobs:
                  test-and-build:
                    runs-on: ubuntu-latest
                    steps:
                      - uses: actions/checkout@v4
                      - run: npm ci
                      - run: npm test -- --runInBand
                      - run: npm run build
                """
            ),
            "line_by_line": [
                "Line 1 names the workflow so its purpose is obvious in the delivery system.",
                "Line 2 defines the event that triggers the pipeline.",
                "Line 4 names a job that turns source history into verified artifacts.",
                "Line 6 checks out the exact revision being evaluated.",
                "Lines 7 to 9 install dependencies, run tests, and produce a build artifact.",
            ],
            "execution": [
                "The platform receives a push event and provisions an isolated runner.",
                "The repository is checked out at the requested revision.",
                "Each step executes in order, failing fast if a prerequisite signal is red.",
                "Successful pipelines create confidence for deployment or release decisions.",
            ],
            "memory": wrap(
                """
                Runner state
                workflow config -> job graph -> step results -> artifacts
                """
            ),
            "stack": wrap(
                """
                Process stack
                CI orchestrator -> runner -> shell -> npm -> test/build tools
                """
            ),
            "heap": wrap(
                """
                Runner storage
                +--------------------------------------+
                | checked-out source                   |
                | dependency cache                     |
                | build artifacts and logs             |
                +--------------------------------------+
                """
            ),
            "runtime": "Operational excellence is mostly about feedback loops, failure isolation, and safe repeatability rather than glamorous code.",
            "time": "Pipeline duration scales with dependency installation, test execution, and build complexity.",
            "space": "Runner storage usage scales with dependencies, caches, and artifact size.",
            "alternatives": "Other CI systems, preview environments, and progressive delivery platforms solve similar problems with different ergonomics and cost models.",
            "bugs": "Common bugs include environment drift, flaky runners, missing secrets, and pipelines that test something different from what production actually deploys.",
            "debug": "Compare local and CI environments, inspect logs step by step, and capture artifact hashes so you know what actually shipped.",
            "refactor": "Split slow pipelines into parallel tracks, cache safely, and make promotion and rollback paths first-class.",
            "best": "Treat release automation as production software, because it is.",
        },
        "systems": {
            "purpose": f"Use a small algorithmic example to connect {title} to measurable computational trade-offs.",
            "language": "ts",
            "code": wrap(
                """
                function uniqueIds(ids: number[]) {
                  const seen = new Set<number>();
                  for (const id of ids) seen.add(id);
                  return [...seen];
                }
                """
            ),
            "line_by_line": [
                "Line 1 defines a function whose behavior depends directly on data shape and algorithm choice.",
                "Line 2 chooses a Set because membership and uniqueness are its core strengths.",
                "Line 3 iterates through the input once and records each id.",
                "Line 4 converts the set back into an array for UI-friendly consumption.",
            ],
            "execution": [
                "The function allocates a Set and then processes each input value once.",
                "The data structure absorbs duplicates while preserving insertion order.",
                "The resulting unique array can feed rendering, caching, or further computation.",
            ],
            "memory": wrap(
                """
                Data structures
                input array -> Set bucket structure -> output array
                """
            ),
            "stack": wrap(
                """
                Call stack
                +--------------------------+
                | uniqueIds()              |
                | loop body                |
                +--------------------------+
                """
            ),
            "heap": wrap(
                """
                Heap
                +-----------------------------------+
                | input array                       |
                | Set internal storage              |
                | output array                      |
                +-----------------------------------+
                """
            ),
            "runtime": "What looks like a tiny implementation choice often determines whether a UI scales elegantly or degrades under real workloads.",
            "time": "Expected O(n) time for insertion and iteration over `n` ids.",
            "space": "O(n) extra space for the Set and output array.",
            "alternatives": "Sorting followed by linear deduplication uses different time and space trade-offs and may be preferable when ordered output needs are different.",
            "bugs": "Common bugs include choosing arrays for membership checks, ignoring asymptotic growth, and modeling data without considering access patterns.",
            "debug": "Measure with realistic input sizes, profile allocations, and inspect whether the chosen structure matches actual operations.",
            "refactor": "Document why the data structure was chosen so later maintainers do not simplify it into something slower by accident.",
            "best": "Pick structures and algorithms based on workload, not habit.",
        },
        "professional": {
            "purpose": f"Show how {title} becomes concrete through explicit written engineering decisions.",
            "language": "md",
            "code": wrap(
                """
                # ADR: Adopt Server Rendering for Product Pages

                ## Context
                Product pages need faster first paint and better crawlability.

                ## Decision
                Render product pages on the server and hydrate only interactive widgets.
                """
            ),
            "line_by_line": [
                "Line 1 gives the decision a searchable, stable title.",
                "Lines 3 and 4 describe the real problem, not just the preferred tool.",
                "Lines 6 and 7 record the chosen direction in a way future engineers can revisit.",
            ],
            "execution": [
                "A human reads the document before or during implementation planning.",
                "The team uses it to compare alternatives, align trade-offs, and preserve context.",
                "Later maintainers can inspect the ADR to understand why the system looks the way it does.",
            ],
            "memory": wrap(
                """
                Team memory
                context -> decision -> consequences -> future revisions
                """
            ),
            "stack": wrap(
                """
                Decision stack
                problem -> options -> review -> decision -> follow-up
                """
            ),
            "heap": wrap(
                """
                Organizational knowledge graph
                ADR -> related tickets -> code changes -> release notes
                """
            ),
            "runtime": "The runtime here is organizational rather than computational. Written decisions reduce confusion, repeated debate, and accidental architecture drift.",
            "time": "The direct cost is human reading and writing time; the payoff is lower long-term coordination cost.",
            "space": "Storage cost is trivial compared with the cost of losing context.",
            "alternatives": "Architecture diagrams, RFCs, design docs, and annotated pull requests can complement or partially replace ADRs.",
            "bugs": "Common bugs include writing decisions after the fact, skipping rejected alternatives, and letting documents rot away from the code they describe.",
            "debug": "When teams disagree repeatedly, inspect whether the real issue is undocumented assumptions rather than technical difficulty.",
            "refactor": "Shorten bloated documents, link them to code and metrics, and keep a living decision index.",
            "best": "Write to help future teammates make good decisions without you in the room.",
        },
    }
    return bundles[kind]


def build_section_intro(topic: Topic, profile: dict, topics_by_title: dict[str, Topic]) -> str:
    prereq_names = sentence_list(topic.prerequisites)
    unlock_names = sentence_list(topic.unlocks)
    return wrap(
        f"""
        {topic.title} sits in the middle of {profile['domain']}. It matters because a frontend engineer is never only arranging pixels; they are shaping how information, state, and user intent move through a real system.

        This chapter assumes you are building from {prereq_names if prereq_names != 'none' else 'the beginning of the curriculum'} and pushes toward {unlock_names if unlock_names != 'none' else 'deeper architectural practice'}. By the end, you should be able to explain {topic.title.lower()} from first principles, implement it in code, debug it under pressure, and reason about its trade-offs like a senior engineer.
        """
    )


def first_principles(topic: Topic, profile: dict) -> list[str]:
    return [
        f"Every system can be described as inputs, transformation rules, and outputs. In {topic.title}, the key inputs are {profile['inputs']}, and the outputs are {profile['outputs']}.",
        "Abstractions exist to hide detail, but senior engineers learn which details are safe to ignore and which details become production bugs if ignored.",
        "Constraints are not annoyances; they are the shape of the problem. Device limits, human limits, browser limits, and network limits all matter.",
        "State changes over time, so timing matters. A correct model must explain not only what a system is, but when each part runs and what can interrupt it.",
        f"Good engineering depends on measurement. The most useful measures for this topic usually include {profile['metrics']}.",
    ]


def mental_models(topic: Topic, profile: dict) -> list[str]:
    return [
        f"Think of {topic.title} as {profile['analogy']}.",
        "Picture the system as a pipeline: something enters, the browser or runtime applies rules, and a visible result or side effect emerges.",
        "Track ownership explicitly: ask which layer owns structure, style, state, security, persistence, or scheduling at each moment.",
        "Prefer causal graphs over memorized trivia. If you can explain cause and effect, you can reconstruct details you forget.",
    ]


def core_concepts(topic: Topic, profile: dict) -> list[str]:
    keywords = topic_keywords(topic.title)
    return [
        f"Definition: what counts as {topic.title} and what sits outside its boundary.",
        f"Inputs: the role of {profile['inputs']} in shaping behavior.",
        f"Outputs: the visible or measurable results, including {profile['outputs']}.",
        f"Invariants: the rules that should remain true even as features change, such as correctness, clarity, and safety.",
        f"Failure modes: how {topic.title.lower()} breaks under edge cases, scale, latency, or misunderstanding.",
        f"Vocabulary: the keywords you should be comfortable using after this chapter include {sentence_list(keywords) if keywords else 'core domain terms and mental models'}.",
    ]


def step_by_step_lines(topic: Topic, profile: dict) -> list[str]:
    return [
        f"Name the user or system goal that makes {topic.title} necessary in the first place.",
        f"List the inputs involved: {profile['inputs']}.",
        "Trace how the browser, runtime, toolchain, or team transforms those inputs step by step.",
        f"Identify the outputs: {profile['outputs']}.",
        f"Measure the critical properties, especially {profile['metrics']}.",
        f"Model the unhappy path, because {profile['risk']} is where real systems become interesting.",
        "Generalize the insight into a reusable checklist you can apply to future projects and code reviews.",
    ]


def difficulty_progression(topic: Topic) -> list[str]:
    return [
        f"Level 1, absolute beginner: define {topic.title} in plain language and identify where it appears in a webpage or web app.",
        f"Level 2, basic understanding: trace a simple example and name the major moving parts involved in {topic.title}.",
        f"Level 3, intermediate: implement a working example from scratch and explain the happy path clearly.",
        f"Level 4, advanced: debug a broken implementation, reason about edge cases, and compare alternatives.",
        f"Level 5, professional: make trade-offs using measurable constraints such as {FAMILY_DATA[topic.family]['metrics']}.",
        f"Level 6, senior engineer: design patterns, guardrails, and diagnostics for teams that use {topic.title} at scale.",
        f"Level 7, architect: connect {topic.title} to system design, organizational process, platform evolution, and long-term maintainability.",
    ]


def knowledge_checks(topic: Topic, example: dict) -> list[str]:
    return [
        f"Quick quiz: in one sentence, why does {topic.title} exist rather than leaving the problem to ad hoc code or human memory?",
        f"Multiple choice: which layer should own the main responsibilities of {topic.title} in a production frontend system, and why?",
        f"True or false: if the happy path works once on your machine, you already understand {topic.title} well enough for production.",
        f"Code prediction: before running the example below, predict its output and the intermediate state changes that produce it.",
        f"Find-the-bug exercise: remove one safety or semantic detail from the example and explain what breaks first.",
        f"Explain-the-output prompt: describe why the runtime, browser, or tooling produced the exact result it did.",
        f"Reflection question: what assumptions about users, devices, networks, or teams does {topic.title} force you to make explicit?",
    ]


def misconceptions(topic: Topic) -> list[str]:
    return [
        f"{topic.title} is not just syntax or API trivia; it is a model for how a system behaves over time.",
        "Newer tooling does not erase first principles. Frameworks and libraries rearrange responsibilities; they do not eliminate them.",
        "If a pattern is convenient but invisible to users, debuggers, or teammates, it may still be the wrong pattern.",
        "Performance, security, and accessibility are not optional add-ons. They are part of the definition of done.",
        "A working demo is not the same thing as a robust design under scale, failure, and change.",
    ]


def exercise_block(topic: Topic, level: str) -> list[str]:
    stem = {
        "beginner": "Work with a tiny, single-page example and focus on observation.",
        "intermediate": "Add realistic state, edge cases, and debugging instrumentation.",
        "advanced": "Scale the idea to a multi-component or multi-route application.",
    }[level]
    return [
        stem,
        f"Implement a minimal example that demonstrates {topic.title.lower()} without using a large framework abstraction unless the chapter itself is about frameworks.",
        "Write down the expected state transitions before you run the code, then compare expectation with reality.",
        "Intentionally introduce one bug, measure the impact, and document how you found it.",
    ]


def challenge_problems(topic: Topic) -> list[str]:
    return [
        f"Re-implement the chapter's core example using a different abstraction style and explain the trade-offs.",
        f"Design a failure-resilient version of {topic.title} for low-bandwidth networks, low-end devices, and keyboard-only users.",
        "Explain how you would teach this topic to a new teammate using only a whiteboard and no slides.",
        "Define a code review checklist that would catch the most expensive mistakes teams make with this topic.",
    ]


def interview_questions(topic: Topic) -> list[str]:
    return [
        f"Explain {topic.title} from first principles to a junior engineer.",
        f"What are the most important trade-offs when choosing one approach to {topic.title.lower()} over another?",
        f"How would you debug a production issue where {topic.title.lower()} appears correct in development but fails under real traffic or real users?",
        "What performance, security, and accessibility concerns should be reviewed before approving code in this area?",
        "How has modern practice evolved from older approaches, and what future trends matter next?",
    ]


def practical_learning(topic: Topic) -> list[str]:
    return [
        f"Mini project: build the smallest believable example that demonstrates {topic.title.lower()} in isolation.",
        f"Real-world project: integrate {topic.title.lower()} into a multi-page or componentized application with logging and tests.",
        f"Portfolio project: write a case study showing the before-and-after impact of good {topic.title.lower()} on user experience or maintainability.",
        f"Debugging exercise: break the example in a realistic way, then capture a step-by-step repair diary.",
        f"Performance optimization exercise: define one measurable budget related to {topic.title.lower()} and improve the result without harming correctness.",
        f"Refactoring exercise: remove duplication, clarify ownership boundaries, and document your design decisions.",
        f"Stretch goal: teach the concept in a short internal workshop or write an ADR that records the trade-offs you discovered.",
        "Further reading: revisit the references at the end and compare the chapter's mental models with official specifications and production case studies.",
    ]


def learning_outcomes(topic: Topic) -> list[str]:
    return [
        f"Explain {topic.title} from first principles in plain language and precise technical language.",
        f"Teach {topic.title} to another person using examples, diagrams, and trade-offs rather than memorized rules.",
        f"Implement {topic.title.lower()} from scratch in a small but correct example.",
        f"Debug real-world problems that involve {topic.title.lower()}, including timing issues, edge cases, and bad assumptions.",
        "Recognize performance issues before they become user-visible incidents.",
        "Recognize security risks before convenience shortcuts become vulnerabilities.",
        "Apply accessibility and inclusive-design expectations as part of normal engineering work.",
        "Answer senior-level interview questions with both theory and operational judgment.",
    ]


def related_topics(topic: Topic, topics_by_title: dict[str, Topic]) -> list[str]:
    related = []
    for item in topic.prerequisites[:2]:
        related.append(topic_link(item, topics_by_title))
    for item in topic.unlocks[:2]:
        related.append(topic_link(item, topics_by_title))
    return dedupe(related)


def glossary_lines(kind: str) -> list[str]:
    key = kind if kind in GLOSSARY else REFERENCE_MAP.get(kind, kind)
    if key not in GLOSSARY:
        key = "professional"
    base = GLOSSARY[key]
    return [f"{term}: {definition}" for term, definition in base.items()]


def reference_lines(kind: str) -> list[str]:
    return FAMILY_DATA[REFERENCE_MAP[kind]]["references"]


def render_topic(topic: Topic, topics: list[Topic], topics_by_title: dict[str, Topic]) -> str:
    profile = FAMILY_DATA[topic.family]
    kind = kind_for_topic(topic.title, topic.family)
    example = example_bundle(kind, topic.title)
    next_topic = topics[topic.number] if topic.number < len(topics) else None
    related = related_topics(topic, topics_by_title)

    return f"""# {topic.title}

- Prerequisites: {dependency_links(topic.prerequisites, topics_by_title)}
- Required knowledge: {', '.join(concept_dependencies(topic))}
- Concepts it depends on: {profile['inputs']}, explicit constraints, and a clear understanding of cause and effect.
- Concepts unlocked after completing it: {', '.join(unlocked_concepts(topic, topics_by_title))}
- Estimated study time: {topic.study_hours} hours
- Estimated practice time: {topic.practice_hours} hours
- Difficulty rating: {topic.difficulty}/10

## Introduction

{build_section_intro(topic, profile, topics_by_title)}

## Why This Exists

{topic.title} exists because frontend systems need reliable ways to turn intent into outcomes inside {profile['domain']}. Without a shared model for this topic, teams fall back to folklore, copy-pasted snippets, and accidental complexity. The result is fragile software that seems easy only until the first outage, redesign, localization bug, accessibility audit, or scaling milestone.

## Historical Background

{profile['history']} The modern practice around {topic.title} is therefore a historical compromise: old constraints, new expectations, and many lessons learned from failure. Understanding that evolution matters because it explains why certain rules feel awkward, why browser behavior is sometimes surprising, and why some "best practices" are reactions to pain rather than arbitrary style choices.

## The Problem It Solves

At its core, {topic.title} solves a coordination problem. Multiple forces are competing at once: user goals, browser behavior, developer ergonomics, long-term maintenance, security boundaries, and performance budgets. This topic gives you a stable way to reason about those forces instead of letting whichever force is loudest at the moment dominate the design.

## First Principles

{section_bullets(first_principles(topic, profile))}

## Mental Models

{section_bullets(mental_models(topic, profile))}

## Real World Analogies

If you need an intuition pump before the formal model clicks, treat {topic.title} as {profile['analogy']}. The analogy is imperfect, but it helps because it forces you to think in flows, boundaries, bottlenecks, and failure points instead of isolated syntax.

## Core Concepts

{section_bullets(core_concepts(topic, profile))}

## Internal Mechanics

Internally, {topic.title} is about transforming {profile['inputs']} into {profile['outputs']}. A senior engineer can explain that transformation step by step, name which layer is responsible for each step, and predict what happens when one step becomes slow, invalid, insecure, or unavailable. That explanatory power is more valuable than memorizing API signatures because the browser platform and tooling ecosystem keep evolving while first principles stay stable.

## Architecture

Architecturally, this topic usually spans several layers: author intent, source code or markup, build-time transformations, browser or runtime execution, and the final user-visible behavior. Good architecture keeps these layers legible. Bad architecture collapses them together so tightly that no one can tell whether a bug belongs to data, rendering, state, network, tooling, or design.

## Mathematical Foundations (when applicable)

The mathematics behind this chapter is usually not advanced calculus; it is applied reasoning. Think in ratios, counts, queueing, set membership, state transitions, percentiles, and asymptotic growth. For {topic.title}, the useful quantitative lens is {profile['metrics']}. Senior frontend engineers use these measurements to argue from evidence rather than intuition.

## Computer Science Foundations

This topic connects directly to classic computer science themes: abstraction, state, algorithms, data representation, resource limits, and fault handling. If you can describe {topic.title.lower()} in terms of inputs, outputs, invariants, and complexity, you are already thinking like a computer scientist rather than a framework user.

## Browser Perspective

From the browser's perspective, {topic.title} is never isolated. It sits inside a larger runtime that is parsing documents, matching selectors, scheduling tasks, dispatching events, enforcing security policy, handling network I/O, and painting frames. Even when the chapter emphasizes tooling or team process, the final judge is still the user agent that must interpret and deliver the result.

## Implementation Details

Implementation quality comes from making boundaries explicit. Name the inputs, validate assumptions, keep state close to ownership, instrument the slow or risky parts, and document trade-offs. If you find yourself unable to explain how a feature using {topic.title.lower()} works without hand-waving, the implementation is probably too magical for its own good.

## Step-by-Step Walkthrough

{numbered(step_by_step_lines(topic, profile))}

## Visual Diagrams (ASCII)

```text
{DIAGRAMS[kind]}
```

## Difficulty Progression

{numbered(difficulty_progression(topic))}

## Knowledge Checks

{section_bullets(knowledge_checks(topic, example))}

## Common Misconceptions

{section_bullets(misconceptions(topic))}

## Practical Examples

**Purpose:** {example['purpose']}

### Complete Source Code

```{example['language']}
{example['code']}
```

### Line-by-Line Explanation

{numbered(example['line_by_line'])}

### Execution Walkthrough

{numbered(example['execution'])}

### Memory Visualization

```text
{example['memory']}
```

### Stack Visualization

```text
{example['stack']}
```

### Heap Visualization

```text
{example['heap']}
```

### Runtime Behavior

{example['runtime']}

### Time Complexity

{example['time']}

### Space Complexity

{example['space']}

### Alternative Solutions

{example['alternatives']}

### Common Bugs

{example['bugs']}

### Debugging Walkthrough

{example['debug']}

### Refactoring Opportunities

{example['refactor']}

### Best Practices

{example['best']}

## Beginner Exercises

{section_bullets(exercise_block(topic, "beginner"))}

## Intermediate Exercises

{section_bullets(exercise_block(topic, "intermediate"))}

## Advanced Exercises

{section_bullets(exercise_block(topic, "advanced"))}

## Challenge Problems

{section_bullets(challenge_problems(topic))}

## Interview Questions

{section_bullets(interview_questions(topic))}

## Performance Considerations

For this topic, performance means more than speed. It means doing the right amount of work, at the right time, on the right device, with enough observability to notice regressions. Review {profile['metrics']} regularly, define budgets early, and measure in conditions that resemble real users rather than only development hardware.

## Security Considerations

Every topic has a security angle because every abstraction can be misused or misunderstood. The main risk here is {profile['risk']}. Ask what input is attacker-controlled, what trust boundary is crossed, what data becomes persistent, and how failure should be contained instead of amplified.

## Accessibility Considerations

Accessibility is central here because {profile['a11y']}. Review keyboard flows, focus handling, readable structure, reduced-motion behavior, zoom resilience, screen-reader output, and error communication as part of normal implementation rather than a final checklist.

## Debugging Guide

Start by reproducing the problem in the smallest environment that still shows the bug. Then ask five questions in order: what input triggered the issue, which layer owns the next step, what state changed unexpectedly, what measurement confirms the suspicion, and what simpler example still reproduces the problem? This discipline prevents random guessing and turns debugging into engineering.

## Best Practices

{section_bullets([
    f"Start with the platform and first principles before reaching for heavy abstractions around {topic.title}.",
    "Name invariants explicitly in code, tests, and documentation.",
    "Measure behavior with tools rather than relying on anecdotes.",
    "Design for failure, interruption, and change instead of assuming the happy path.",
    "Protect accessibility, security, and performance together because production quality is multi-dimensional.",
])}

## Anti-patterns

{section_bullets([
    "Copy-pasting patterns without understanding their assumptions.",
    "Global side effects that make ownership unclear.",
    "Abstractions that hide essential timing or failure details.",
    "One-off fixes that bypass shared standards or reusable layers.",
    "Treating browser behavior as a black box instead of something you can model and inspect.",
])}

## Common Mistakes

{section_bullets([
    f"Using {topic.title.lower()} successfully once and assuming the same approach generalizes automatically.",
    "Ignoring the unhappy path until production traffic reveals it.",
    "Failing to connect implementation choices to measurable outcomes.",
    "Optimizing syntax while neglecting system behavior.",
    "Skipping documentation because the current team remembers the context today.",
])}

## Design Trade-offs

There is no universally correct implementation of {topic.title}. The right design depends on user needs, product risk, performance budgets, team skill, and operational constraints. Senior engineers stay honest about those trade-offs: they can explain what was gained, what was sacrificed, what alternatives were rejected, and what future signal would justify revisiting the decision.

## Practical Learning

{section_bullets(practical_learning(topic))}

## Learning Outcomes

{section_bullets(learning_outcomes(topic))}

## Related Topics

{section_bullets(related if related else ["This chapter is an early foundation and therefore mainly points forward through the curriculum."])}

## Summary

{topic.title} is worth mastering because it teaches you how to reason instead of memorize. Once you can model the inputs, transformations, outputs, measurements, and failure modes involved here, you can debug faster, design with more confidence, and make better trade-offs under real-world constraints. That is the difference between knowing a tool and practicing engineering.

## Key Takeaways

{section_bullets([
    f"{topic.title} exists to solve a real coordination problem in {profile['domain']}.",
    "First principles beat memorized snippets when systems become large, slow, or surprising.",
    "Good implementations make ownership, constraints, and failure states explicit.",
    "Performance, security, and accessibility are part of the core model, not separate electives.",
    "Senior-level understanding means being able to teach, debug, measure, and redesign the concept under pressure.",
])}

## Glossary

{section_bullets(glossary_lines(kind))}

## References

{section_bullets(reference_lines(kind))}

## Suggested Next Topic

{f"Continue with {topic_link(next_topic.title, topics_by_title)} to keep the conceptual momentum going and see how this chapter unlocks the next layer of engineering depth." if next_topic else "You have reached the end of the formal curriculum. Revisit earlier chapters, expand your capstone, and keep tracking emerging standards and browser changes."}
"""


def render_readme(topics: list[Topic]) -> str:
    total_study = sum(topic.study_hours for topic in topics)
    total_practice = sum(topic.practice_hours for topic in topics)
    module_lines = []
    for module_number, module in enumerate(MODULES, start=1):
        module_topics = [topic for topic in topics if topic.module_number == module_number]
        topic_links = ", ".join(f"[{topic.number:03d} {topic.title}]({topic.filename})" for topic in module_topics)
        module_lines.append(
            f"### Module {module_number}: {module['name']}\n\n{module['theme']}\n\n{topic_links}"
        )

    milestones = [
        "Milestone 1, apprentice foundation: complete modules 1 to 4 and build a fully semantic, responsive, accessible multi-page site without frameworks.",
        "Milestone 2, language fluency: complete modules 5 to 7 and build a vanilla JavaScript application with persistent storage and network data.",
        "Milestone 3, platform depth: complete modules 8 to 10 and ship a tested TypeScript application with service-worker support and CI.",
        "Milestone 4, production quality: complete modules 11 to 13 and perform measurable performance, SEO, security, and accessibility improvements.",
        "Milestone 5, architecture maturity: complete modules 14 to 16 and design a production-ready framework application with safe deployments.",
        "Milestone 6, senior breadth: complete module 17 and defend system-design choices using data structures, complexity, and reliability trade-offs.",
        "Milestone 7, architect practice: complete module 18 and deliver the capstone with ADRs, rollout strategy, and future-facing standards awareness.",
    ]

    projects = [
        "Project 1: a personal site built with semantic HTML, modern CSS, and no framework.",
        "Project 2: a keyboard-accessible budgeting tool in vanilla JavaScript with local persistence.",
        "Project 3: a PWA note-taking or habit-tracking app with offline support and background sync patterns.",
        "Project 4: a TypeScript dashboard that consumes an external API and includes unit, integration, and end-to-end tests.",
        "Project 5: a framework-based commerce or content app using SSR, caching, and performance budgets.",
        "Project 6: a design-system package with documented tokens, components, accessibility guarantees, and visual tests.",
        "Project 7: the final capstone, a production-style frontend system with experimentation, observability, and deployment automation.",
    ]

    capstone = [
        "Phase 1: choose a domain with enough complexity to require routing, state, accessibility, performance, and security decisions.",
        "Phase 2: write an architecture brief, performance budget, accessibility goals, and threat model before implementation.",
        "Phase 3: build a progressively enhanced MVP with semantic HTML, resilient CSS, and a documented data model.",
        "Phase 4: evolve the MVP into a typed, tested framework application with CI, observability, and staged releases.",
        "Phase 5: run performance, accessibility, and security audits; fix issues; and document trade-offs in ADRs.",
        "Phase 6: present the system as if you were handing it to a senior engineering team for long-term ownership.",
    ]

    return f"""# Frontend Engineering Curriculum

## Curriculum Overview

This repository is a full-stack-of-the-browser curriculum designed to take a complete beginner from first principles to senior frontend engineering judgment. It blends computer science, internet fundamentals, browser internals, JavaScript and CSS depth, testing, security, accessibility, architecture, system design, delivery, and professional practice.

The curriculum is organized into 180 self-contained markdown books. Each chapter can stand alone, but the order is intentional: the path moves from machine and network fundamentals through browser documents, styling, programming, runtime internals, web APIs, tooling, performance, security, architecture, frameworks, production delivery, and finally senior-level design and leadership.

## Learning Philosophy

- Learn from first principles before memorizing APIs.
- Treat the browser as a real operating environment with resource limits, security boundaries, and scheduling behavior.
- Study theory and implementation together so intuition becomes operational judgment.
- Use diagrams, experiments, exercises, and teaching-back to turn passive reading into durable understanding.
- Revisit topics in spirals: beginner understanding becomes professional judgment only through repeated application.

## How to Study the Material

1. Read one chapter actively, not passively. Pause to predict outputs, sketch diagrams, and explain the model in your own words.
2. Run or rewrite the example code, then modify it until it breaks in interesting ways.
3. Complete at least the beginner and intermediate exercises before moving on.
4. Keep a learning journal with definitions, failure modes, diagrams, and trade-offs.
5. Build milestone projects that force you to combine multiple chapters at once.
6. Re-teach completed topics to another person or to your future self in written notes.

## Estimated Hours

- Total reading and study time: about {total_study} hours
- Total deliberate practice time: about {total_practice} hours
- Total guided curriculum time: about {total_study + total_practice} hours
- Recommended pacing: 8 to 12 hours per week for 3 to 5 years, depending on project depth and repetition

## Prerequisites

- No formal computer science degree is required.
- Comfort with basic computer use is enough to begin.
- Persistence matters more than prior exposure.
- A willingness to build small projects, debug failures, and revisit hard topics is essential.

## Difficulty Progression

The curriculum deliberately climbs seven levels of mastery:

1. Absolute beginner
2. Basic understanding
3. Intermediate
4. Advanced
5. Professional
6. Senior Engineer
7. Architect

You will revisit many themes at higher levels. For example, HTML begins as page structure, later becomes accessibility infrastructure, and finally becomes a design-systems and architecture concern.

## Learning Roadmap

{"\n\n".join(module_lines)}

## Milestones

{section_bullets(milestones)}

## Recommended Projects

{section_bullets(projects)}

## Final Capstone Roadmap

{numbered(capstone)}

## How to Navigate the Chapters

- Each file is numbered with zero padding so the reading order is explicit.
- Each chapter contains prerequisites, required knowledge, unlocked concepts, and study estimates.
- The required sections are consistent across chapters so you can build a repeatable study ritual.
- Cross-links point both backward to prerequisites and forward to the next conceptual layer.

## Suggested Study Rhythm

- Early stage: 3 to 4 chapters per week plus tiny experiments.
- Middle stage: 1 to 2 chapters per week plus a running product project.
- Senior stage: fewer chapters per week, but deeper project work, audits, design reviews, and architecture writing.

## What Completion Should Feel Like

By the end of the curriculum, you should be able to build and debug production frontends, explain how the browser works under the hood, reason about performance and security from evidence, choose frameworks and architecture deliberately, communicate trade-offs clearly, and mentor less experienced engineers from first principles rather than folklore.
"""


def main() -> None:
    topics = build_topics()
    assert len(topics) == 180, f"Expected 180 topics, got {len(topics)}"
    topics_by_title = {topic.title: topic for topic in topics}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT_DIR.glob("[0-9][0-9][0-9]-*.md"):
        stale.unlink()

    for topic in topics:
        content = render_topic(topic, topics, topics_by_title).strip() + "\n"
        (OUTPUT_DIR / topic.filename).write_text(content)

    (OUTPUT_DIR / "README.md").write_text(render_readme(topics).strip() + "\n")

    print(f"Generated {len(topics)} topic books plus README in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
