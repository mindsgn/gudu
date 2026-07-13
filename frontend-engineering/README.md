# Frontend Engineering Curriculum

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

- Total reading and study time: about 954 hours
- Total deliberate practice time: about 1418 hours
- Total guided curriculum time: about 2372 hours
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

### Module 1: Computing and Network Foundations

Ground the student in the machine, the network, and the protocols that make web software possible.

[001 Computer Science for Frontend Engineers](001-computer-science-for-frontend-engineers.md), [002 Computer Architecture Basics](002-computer-architecture-basics.md), [003 Operating Systems for Web Engineers](003-operating-systems-for-web-engineers.md), [004 Command Line and Unix Thinking](004-command-line-and-unix-thinking.md), [005 How the Internet Works](005-how-the-internet-works.md), [006 Client-Server Architecture](006-client-server-architecture.md), [007 Networking Fundamentals](007-networking-fundamentals.md), [008 DNS and Name Resolution](008-dns-and-name-resolution.md), [009 HTTP and HTTPS](009-http-and-https.md), [010 TCP, TLS, and Sockets](010-tcp-tls-and-sockets.md)

### Module 2: The Open Web and HTML

Teach the browser's document model, standards culture, semantic structure, forms, media, and accessibility-first markup.

[011 Browsers and Rendering Engines](011-browsers-and-rendering-engines.md), [012 Web Standards and the Open Web](012-web-standards-and-the-open-web.md), [013 HTML Fundamentals](013-html-fundamentals.md), [014 Semantic HTML](014-semantic-html.md), [015 Document Structure and Landmarks](015-document-structure-and-landmarks.md), [016 Links, Navigation, and URLs](016-links-navigation-and-urls.md), [017 Forms and Validation](017-forms-and-validation.md), [018 Media, Images, Audio, and Video](018-media-images-audio-and-video.md), [019 Accessibility Foundations](019-accessibility-foundations.md), [020 ARIA and Assistive Technology](020-aria-and-assistive-technology.md)

### Module 3: CSS Foundations

Move from raw documents to visual systems by teaching how the browser computes style and exposes layout primitives.

[021 CSS Fundamentals](021-css-fundamentals.md), [022 Selectors, Specificity, and the Cascade](022-selectors-specificity-and-the-cascade.md), [023 CSS Units and Sizing](023-css-units-and-sizing.md), [024 Box Model and Layout Basics](024-box-model-and-layout-basics.md), [025 Display, Visibility, and Flow](025-display-visibility-and-flow.md), [026 Positioning and Stacking Context](026-positioning-and-stacking-context.md), [027 Typography on the Web](027-typography-on-the-web.md), [028 Colors, Backgrounds, and Gradients](028-colors-backgrounds-and-gradients.md), [029 Borders, Shadows, and Visual Effects](029-borders-shadows-and-visual-effects.md), [030 Modern CSS Features and Functions](030-modern-css-features-and-functions.md)

### Module 4: Layout, Motion, and Responsive Interfaces

Teach the layout algorithms and adaptive design decisions that turn CSS primitives into resilient user interfaces.

[031 Flexbox](031-flexbox.md), [032 CSS Grid](032-css-grid.md), [033 Floats and Legacy Layout](033-floats-and-legacy-layout.md), [034 Overflow, Scrolling, and Scroll Behavior](034-overflow-scrolling-and-scroll-behavior.md), [035 Responsive Design](035-responsive-design.md), [036 Media Queries](036-media-queries.md), [037 Container Queries](037-container-queries.md), [038 Responsive Images](038-responsive-images.md), [039 Transforms, Transitions, and Animations](039-transforms-transitions-and-animations.md), [040 Design Systems and Tokens](040-design-systems-and-tokens.md)

### Module 5: JavaScript Language Foundations

Build fluency with the language that powers the browser and most frontend tooling stacks.

[041 JavaScript Fundamentals](041-javascript-fundamentals.md), [042 Data Types and Values](042-data-types-and-values.md), [043 Variables, Scope, and Hoisting](043-variables-scope-and-hoisting.md), [044 Operators, Expressions, and Control Flow](044-operators-expressions-and-control-flow.md), [045 Functions and Abstractions](045-functions-and-abstractions.md), [046 Objects, Prototypes, and Classes](046-objects-prototypes-and-classes.md), [047 Arrays, Strings, and Collections](047-arrays-strings-and-collections.md), [048 Time, Dates, and Internationalization](048-time-dates-and-internationalization.md), [049 Error Handling and Defensive Programming](049-error-handling-and-defensive-programming.md), [050 Modules, Packages, and the JavaScript Ecosystem](050-modules-packages-and-the-javascript-ecosystem.md)

### Module 6: JavaScript Internals

Reveal what the JavaScript engine is actually doing so the student can reason about correctness, memory, and runtime behavior.

[051 Execution Context and the JavaScript Runtime](051-execution-context-and-the-javascript-runtime.md), [052 Call Stack, Stack Frames, and Recursion](052-call-stack-stack-frames-and-recursion.md), [053 Memory Management in JavaScript](053-memory-management-in-javascript.md), [054 Garbage Collection](054-garbage-collection.md), [055 Closures and Lexical Environments](055-closures-and-lexical-environments.md), [056 this Binding and Object Invocation](056-this-binding-and-object-invocation.md), [057 Prototype Chain and Object Delegation](057-prototype-chain-and-object-delegation.md), [058 Iterators, Generators, and Iteration Protocols](058-iterators-generators-and-iteration-protocols.md), [059 Functional Programming in JavaScript](059-functional-programming-in-javascript.md), [060 Object-Oriented Design in JavaScript](060-object-oriented-design-in-javascript.md)

### Module 7: The Browser Runtime and Core Web APIs

Connect the language runtime to the DOM, the event system, storage, history, and the network APIs used every day.

[061 Event Loop and Task Queues](061-event-loop-and-task-queues.md), [062 Concurrency, Parallelism, and the Browser](062-concurrency-parallelism-and-the-browser.md), [063 Callbacks, Promises, and Async Await](063-callbacks-promises-and-async-await.md), [064 Fetch, Streams, and Networking APIs](064-fetch-streams-and-networking-apis.md), [065 DOM Fundamentals](065-dom-fundamentals.md), [066 DOM Manipulation and Traversal](066-dom-manipulation-and-traversal.md), [067 Events, Propagation, and Delegation](067-events-propagation-and-delegation.md), [068 Browser Storage, Cookies, and IndexedDB](068-browser-storage-cookies-and-indexeddb.md), [069 History, Navigation, and the URL API](069-history-navigation-and-the-url-api.md), [070 Browser APIs and Capabilities](070-browser-apis-and-capabilities.md)

### Module 8: Advanced Browser Platform Features

Teach the capabilities that make the browser a serious application platform rather than a passive document viewer.

[071 Canvas and SVG](071-canvas-and-svg.md), [072 Clipboard, Drag and Drop, and File APIs](072-clipboard-drag-and-drop-and-file-apis.md), [073 Web Workers and Background Processing](073-web-workers-and-background-processing.md), [074 Service Workers and Offline Architectures](074-service-workers-and-offline-architectures.md), [075 Progressive Web Apps](075-progressive-web-apps.md), [076 Web Components, Custom Elements, and Shadow DOM](076-web-components-custom-elements-and-shadow-dom.md), [077 Observers: Intersection, Mutation, and Resize](077-observers-intersection-mutation-and-resize.md), [078 Notifications, Permissions, and Device APIs](078-notifications-permissions-and-device-apis.md), [079 WebAssembly for Frontend Engineers](079-webassembly-for-frontend-engineers.md), [080 Browser Internals and Process Architecture](080-browser-internals-and-process-architecture.md)

### Module 9: TypeScript and Frontend Tooling

Explain the development machinery that turns source code into dependable browser bundles and safer codebases.

[081 TypeScript Fundamentals](081-typescript-fundamentals.md), [082 Types and Type Inference](082-types-and-type-inference.md), [083 Generics, Utility Types, and Advanced Types](083-generics-utility-types-and-advanced-types.md), [084 Build Tools and Development Servers](084-build-tools-and-development-servers.md), [085 Package Managers: npm, pnpm, and Yarn](085-package-managers-npm-pnpm-and-yarn.md), [086 Module Bundlers: Webpack, Rollup, and ESBuild](086-module-bundlers-webpack-rollup-and-esbuild.md), [087 Transpilers, Compilers, and Babel](087-transpilers-compilers-and-babel.md), [088 Linters, Formatters, and Static Analysis](088-linters-formatters-and-static-analysis.md), [089 Environment Variables, Configuration, and Secrets](089-environment-variables-configuration-and-secrets.md), [090 Debugging and Browser DevTools](090-debugging-and-browser-devtools.md)

### Module 10: Version Control, Collaboration, and Testing

Build the engineering habits that make teams fast, safe, and trustworthy.

[091 Git Fundamentals](091-git-fundamentals.md), [092 Branching, Merging, and Rebasing](092-branching-merging-and-rebasing.md), [093 GitHub Collaboration and Open Source Workflows](093-github-collaboration-and-open-source-workflows.md), [094 Testing Fundamentals](094-testing-fundamentals.md), [095 Unit Testing](095-unit-testing.md), [096 Integration Testing](096-integration-testing.md), [097 End-to-End Testing](097-end-to-end-testing.md), [098 Test-Driven Development](098-test-driven-development.md), [099 Accessibility and Visual Testing](099-accessibility-and-visual-testing.md), [100 Performance Testing and Profiling](100-performance-testing-and-profiling.md)

### Module 11: Performance, Rendering, and Discoverability

Teach how pixels get to the screen quickly and how applications stay observable, searchable, and resilient.

[101 Performance Fundamentals](101-performance-fundamentals.md), [102 Critical Rendering Path](102-critical-rendering-path.md), [103 Rendering Pipeline, Layout, Paint, and Compositing](103-rendering-pipeline-layout-paint-and-compositing.md), [104 Reflow, Repaint, and Layout Thrashing](104-reflow-repaint-and-layout-thrashing.md), [105 Code Splitting, Lazy Loading, and Prioritization](105-code-splitting-lazy-loading-and-prioritization.md), [106 Image, Font, and Asset Optimization](106-image-font-and-asset-optimization.md), [107 Caching, Compression, and CDNs](107-caching-compression-and-cdns.md), [108 Web Performance Metrics and Core Web Vitals](108-web-performance-metrics-and-core-web-vitals.md), [109 SEO, Metadata, and Structured Data](109-seo-metadata-and-structured-data.md), [110 Observability, Monitoring, and Logging for Frontends](110-observability-monitoring-and-logging-for-frontends.md)

### Module 12: Security, Identity, and Privacy

Teach the threat models and defensive practices needed to ship web software responsibly.

[111 Web Security Fundamentals](111-web-security-fundamentals.md), [112 Same-Origin Policy, CORS, and CSP](112-same-origin-policy-cors-and-csp.md), [113 Cross-Site Scripting and Content Injection](113-cross-site-scripting-and-content-injection.md), [114 CSRF, Clickjacking, and UI Redressing](114-csrf-clickjacking-and-ui-redressing.md), [115 Authentication and Session Management](115-authentication-and-session-management.md), [116 Authorization and Access Control](116-authorization-and-access-control.md), [117 JWT, OAuth, and OpenID Connect](117-jwt-oauth-and-openid-connect.md), [118 Secure Storage, Privacy, and Compliance](118-secure-storage-privacy-and-compliance.md), [119 Threat Modeling and Secure Coding](119-threat-modeling-and-secure-coding.md), [120 Browser Security Architecture](120-browser-security-architecture.md)

### Module 13: Design, UX, Accessibility, and Content

Expand beyond implementation to the human factors that make products understandable, inclusive, and trustworthy.

[121 Design Fundamentals for Engineers](121-design-fundamentals-for-engineers.md), [122 UI Principles and Visual Hierarchy](122-ui-principles-and-visual-hierarchy.md), [123 UX Research, Information Architecture, and Content](123-ux-research-information-architecture-and-content.md), [124 Color Theory and Contrast](124-color-theory-and-contrast.md), [125 Typography Principles and Readability](125-typography-principles-and-readability.md), [126 Layout Composition and Spacing Systems](126-layout-composition-and-spacing-systems.md), [127 Component Design and API Design](127-component-design-and-api-design.md), [128 Accessibility Engineering and Inclusive Design](128-accessibility-engineering-and-inclusive-design.md), [129 Localization, Internationalization, and BiDi](129-localization-internationalization-and-bidi.md), [130 Design Systems Governance and Documentation](130-design-systems-governance-and-documentation.md)

### Module 14: Frontend Architecture and State

Move from components to systems by teaching rendering strategies, state boundaries, and maintainable frontend structures.

[131 State Management Principles](131-state-management-principles.md), [132 Client-Side Routing and Navigation Architecture](132-client-side-routing-and-navigation-architecture.md), [133 Rendering Strategies: CSR, SSR, SSG, and ISR](133-rendering-strategies-csr-ssr-ssg-and-isr.md), [134 Hydration, Resumability, and Islands](134-hydration-resumability-and-islands.md), [135 Reactivity Models, Virtual DOM, and Signals](135-reactivity-models-virtual-dom-and-signals.md), [136 Framework Architecture and Trade-offs](136-framework-architecture-and-trade-offs.md), [137 Component-Driven Development](137-component-driven-development.md), [138 Micro Frontends and Federated UI](138-micro-frontends-and-federated-ui.md), [139 Frontend Architecture Patterns](139-frontend-architecture-patterns.md), [140 Clean Code, Refactoring, and Maintainability](140-clean-code-refactoring-and-maintainability.md)

### Module 15: Modern Frameworks

Teach popular framework mental models while comparing how different systems manage state, rendering, styling, and data.

[141 React Fundamentals](141-react-fundamentals.md), [142 React State, Effects, and Data Flow](142-react-state-effects-and-data-flow.md), [143 React Rendering, Reconciliation, and Performance](143-react-rendering-reconciliation-and-performance.md), [144 Next.js and Full-Stack React](144-next-js-and-full-stack-react.md), [145 Vue Fundamentals](145-vue-fundamentals.md), [146 Angular Fundamentals](146-angular-fundamentals.md), [147 Svelte and Compiler-Driven UI](147-svelte-and-compiler-driven-ui.md), [148 State Libraries and Server State](148-state-libraries-and-server-state.md), [149 Styling Strategies in Modern Frameworks](149-styling-strategies-in-modern-frameworks.md), [150 Frontend Testing in Framework Applications](150-frontend-testing-in-framework-applications.md)

### Module 16: Data, Delivery, and Production Operations

Connect frontend applications to APIs, real-time systems, deployment workflows, and operational maturity.

[151 API Design for Frontend Consumers](151-api-design-for-frontend-consumers.md), [152 REST, GraphQL, and RPC from the Client](152-rest-graphql-and-rpc-from-the-client.md), [153 Real-Time Systems, WebSockets, SSE, and Streaming](153-real-time-systems-websockets-sse-and-streaming.md), [154 Data Fetching, Caching, and Synchronization](154-data-fetching-caching-and-synchronization.md), [155 Forms, Mutations, and Optimistic UI](155-forms-mutations-and-optimistic-ui.md), [156 Edge Computing, CDNs, and Distributed Frontend Delivery](156-edge-computing-cdns-and-distributed-frontend-delivery.md), [157 Deployment Environments and Release Management](157-deployment-environments-and-release-management.md), [158 CI CD for Frontend Applications](158-ci-cd-for-frontend-applications.md), [159 Feature Flags, Experimentation, and Rollouts](159-feature-flags-experimentation-and-rollouts.md), [160 Incidents, Debugging Production, and Postmortems](160-incidents-debugging-production-and-postmortems.md)

### Module 17: Computer Science, Scale, and System Design

Develop the deeper analytical toolkit needed for complex applications and senior-level architecture work.

[161 Data Structures for UI Engineers](161-data-structures-for-ui-engineers.md), [162 Algorithms and Complexity](162-algorithms-and-complexity.md), [163 Compiler and Parser Basics](163-compiler-and-parser-basics.md), [164 Databases, Data Modeling, and Client Storage](164-databases-data-modeling-and-client-storage.md), [165 Scalability, Reliability, and Resilience](165-scalability-reliability-and-resilience.md), [166 System Design for Frontend Engineers](166-system-design-for-frontend-engineers.md), [167 Distributed Systems for Product Engineers](167-distributed-systems-for-product-engineers.md), [168 Browser-Based Graphics and Rendering Architectures](168-browser-based-graphics-and-rendering-architectures.md), [169 AI Integration in Frontend Products](169-ai-integration-in-frontend-products.md), [170 Technical Communication and Leadership](170-technical-communication-and-leadership.md)

### Module 18: Professional Practice and the Future of the Web

Prepare the learner to lead projects, communicate decisions, ship sustainably, and keep pace with change.

[171 Software Engineering Best Practices](171-software-engineering-best-practices.md), [172 Code Reviews, Mentoring, and Teamwork](172-code-reviews-mentoring-and-teamwork.md), [173 Documentation, ADRs, and RFCs](173-documentation-adrs-and-rfcs.md), [174 Versioning, Release Trains, and Change Management](174-versioning-release-trains-and-change-management.md), [175 Product Thinking and Experimentation](175-product-thinking-and-experimentation.md), [176 Business Metrics, Analytics, and Decision Making](176-business-metrics-analytics-and-decision-making.md), [177 Career Growth and Staff-Level Impact](177-career-growth-and-staff-level-impact.md), [178 Capstone System Design Studio](178-capstone-system-design-studio.md), [179 Open Source Contribution and Community Practice](179-open-source-contribution-and-community-practice.md), [180 Emerging Web Standards](180-emerging-web-standards.md)

## Milestones

- Milestone 1, apprentice foundation: complete modules 1 to 4 and build a fully semantic, responsive, accessible multi-page site without frameworks.
- Milestone 2, language fluency: complete modules 5 to 7 and build a vanilla JavaScript application with persistent storage and network data.
- Milestone 3, platform depth: complete modules 8 to 10 and ship a tested TypeScript application with service-worker support and CI.
- Milestone 4, production quality: complete modules 11 to 13 and perform measurable performance, SEO, security, and accessibility improvements.
- Milestone 5, architecture maturity: complete modules 14 to 16 and design a production-ready framework application with safe deployments.
- Milestone 6, senior breadth: complete module 17 and defend system-design choices using data structures, complexity, and reliability trade-offs.
- Milestone 7, architect practice: complete module 18 and deliver the capstone with ADRs, rollout strategy, and future-facing standards awareness.

## Recommended Projects

- Project 1: a personal site built with semantic HTML, modern CSS, and no framework.
- Project 2: a keyboard-accessible budgeting tool in vanilla JavaScript with local persistence.
- Project 3: a PWA note-taking or habit-tracking app with offline support and background sync patterns.
- Project 4: a TypeScript dashboard that consumes an external API and includes unit, integration, and end-to-end tests.
- Project 5: a framework-based commerce or content app using SSR, caching, and performance budgets.
- Project 6: a design-system package with documented tokens, components, accessibility guarantees, and visual tests.
- Project 7: the final capstone, a production-style frontend system with experimentation, observability, and deployment automation.

## Final Capstone Roadmap

1. Phase 1: choose a domain with enough complexity to require routing, state, accessibility, performance, and security decisions.
2. Phase 2: write an architecture brief, performance budget, accessibility goals, and threat model before implementation.
3. Phase 3: build a progressively enhanced MVP with semantic HTML, resilient CSS, and a documented data model.
4. Phase 4: evolve the MVP into a typed, tested framework application with CI, observability, and staged releases.
5. Phase 5: run performance, accessibility, and security audits; fix issues; and document trade-offs in ADRs.
6. Phase 6: present the system as if you were handing it to a senior engineering team for long-term ownership.

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
