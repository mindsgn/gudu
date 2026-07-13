# Backend Engineering Curriculum

## Curriculum Overview

This repository contains a complete backend engineering textbook written in Markdown and organized as a library of standalone chapter files. It starts from first principles and builds toward expert backend engineering judgment across computer foundations, programming, application development, data systems, distributed systems, production engineering, and architecture.

The curriculum contains **105 chapters**, each saved as its own Markdown file using the naming pattern `<number>-<topic-name-in-kebab-case>.md`. Every chapter includes the same 13 core sections so learners can build a repeatable study habit while still progressing from beginner to expert.

## Learning Philosophy

- Explain the why before the how.
- Start from the machine and the network, not from frameworks.
- Connect code, data, infrastructure, and operations as parts of one system.
- Teach trade-offs, not only recipes.
- Treat production reality as part of the subject, not an optional appendix.

## How to Study This Textbook

1. Read the chapter introduction and diagram first, then pause and predict how the system works before reading the rest.
2. Run or rewrite the practical examples instead of only reading them.
3. Complete at least the beginner and intermediate exercises in each phase.
4. Keep notes on invariants, failure modes, and trade-offs.
5. Revisit earlier chapters after later phases, because deeper topics will strengthen your first-principles understanding.

## Estimated Effort

- Total study time: about 501 hours
- Total practice time: about 999 hours
- Total guided curriculum time: about 1500 hours
- Recommended pacing: 8 to 12 hours per week, plus project work

## Learning Roadmap

### Phase 1: Computer Foundations

Goal: The learner understands what happens below backend frameworks.

Build a working model of computers, operating systems, and networks before introducing application frameworks.

[1. How Computers Represent Information](1-how-computers-represent-information.md), [2. Computer Architecture for Backend Engineers](2-computer-architecture-for-backend-engineers.md), [3. Operating Systems Fundamentals](3-operating-systems-fundamentals.md), [4. Processes Threads and Scheduling](4-processes-threads-and-scheduling.md), [5. Memory Virtual Memory and Storage Hierarchies](5-memory-virtual-memory-and-storage-hierarchies.md), [6. Filesystems and Persistent Storage](6-filesystems-and-persistent-storage.md), [7. Command Line Linux and Unix Thinking](7-command-line-linux-and-unix-thinking.md), [8. Networking Fundamentals](8-networking-fundamentals.md), [9. How the Internet Works](9-how-the-internet-works.md), [10. DNS and Name Resolution](10-dns-and-name-resolution.md), [11. IP Routing and Packet Delivery](11-ip-routing-and-packet-delivery.md), [12. TCP UDP and Transport Trade-offs](12-tcp-udp-and-transport-trade-offs.md), [13. TLS Certificates and Secure Transport](13-tls-certificates-and-secure-transport.md), [14. Sockets Ports and Connection Lifecycles](14-sockets-ports-and-connection-lifecycles.md), [15. Time Clocks and Failure in Computer Systems](15-time-clocks-and-failure-in-computer-systems.md)

### Phase 2: Programming Foundations

Goal: The learner can write maintainable software.

Move from machine awareness into programming models, algorithms, debugging, and code organization.

[16. Programming Fundamentals and State](16-programming-fundamentals-and-state.md), [17. Variables Types and Data Representation](17-variables-types-and-data-representation.md), [18. Control Flow and Error Handling](18-control-flow-and-error-handling.md), [19. Functions Modules and Abstractions](19-functions-modules-and-abstractions.md), [20. Data Structures in Backend Systems](20-data-structures-in-backend-systems.md), [21. Algorithms and Complexity for Service Engineers](21-algorithms-and-complexity-for-service-engineers.md), [22. Recursion Iteration and Traversal](22-recursion-iteration-and-traversal.md), [23. Concurrency Parallelism and Synchronization](23-concurrency-parallelism-and-synchronization.md), [24. Testing Fundamentals for Backend Code](24-testing-fundamentals-for-backend-code.md), [25. Debugging and Profiling Backend Programs](25-debugging-and-profiling-backend-programs.md), [26. Version Control and Collaborative Workflows](26-version-control-and-collaborative-workflows.md), [27. Object Oriented Design and Composition](27-object-oriented-design-and-composition.md), [28. Functional Programming and Immutability](28-functional-programming-and-immutability.md), [29. Clean Code Refactoring and Maintainability](29-clean-code-refactoring-and-maintainability.md), [30. Compilers Interpreters and Runtime Environments](30-compilers-interpreters-and-runtime-environments.md)

### Phase 3: Backend Development Fundamentals

Goal: The learner can build complete backend applications.

Introduce servers, protocols, validation, identity, and application structure from first principles.

[31. What a Server Really Is](31-what-a-server-really-is.md), [32. The Request Response Lifecycle](32-the-request-response-lifecycle.md), [33. HTTP Semantics Headers and Methods](33-http-semantics-headers-and-methods.md), [34. REST Resource Modeling and Trade-offs](34-rest-resource-modeling-and-trade-offs.md), [35. API Design Contracts and Evolution](35-api-design-contracts-and-evolution.md), [36. Data Serialization and Message Formats](36-data-serialization-and-message-formats.md), [37. Input Validation and Boundary Defense](37-input-validation-and-boundary-defense.md), [38. Authentication Fundamentals](38-authentication-fundamentals.md), [39. Authorization and Access Control](39-authorization-and-access-control.md), [40. Sessions Cookies and Tokens](40-sessions-cookies-and-tokens.md), [41. Backend Application Architecture](41-backend-application-architecture.md), [42. Routing Middleware and Dependency Injection](42-routing-middleware-and-dependency-injection.md), [43. Background Jobs and Asynchronous Workflows](43-background-jobs-and-asynchronous-workflows.md), [44. File Uploads Media Pipelines and Object Storage](44-file-uploads-media-pipelines-and-object-storage.md), [45. Configuration Secrets and Environment Management](45-configuration-secrets-and-environment-management.md)

### Phase 4: Data Engineering

Goal: The learner understands storing and retrieving data efficiently.

Teach persistence, modeling, query execution, indexing, caching, and long-term data stewardship.

[46. Relational Databases and Table Design](46-relational-databases-and-table-design.md), [47. SQL Queries Filtering and Aggregation](47-sql-queries-filtering-and-aggregation.md), [48. Joins Normalization and Schema Modeling](48-joins-normalization-and-schema-modeling.md), [49. Indexes B Trees and Query Performance](49-indexes-b-trees-and-query-performance.md), [50. Transactions ACID and Consistency Guarantees](50-transactions-acid-and-consistency-guarantees.md), [51. Isolation Levels Locks and MVCC](51-isolation-levels-locks-and-mvcc.md), [52. Query Planning Storage Engines and Database Internals](52-query-planning-storage-engines-and-database-internals.md), [53. Caching Fundamentals and Cache Invalidation](53-caching-fundamentals-and-cache-invalidation.md), [54. Redis and In-Memory Data Systems](54-redis-and-in-memory-data-systems.md), [55. NoSQL Foundations and Trade-offs](55-nosql-foundations-and-trade-offs.md), [56. Document Databases and Schema Flexibility](56-document-databases-and-schema-flexibility.md), [57. Key Value Column Family and Time Series Stores](57-key-value-column-family-and-time-series-stores.md), [58. Search Indexes and Full Text Retrieval](58-search-indexes-and-full-text-retrieval.md), [59. Data Pipelines ETL and Warehousing Basics](59-data-pipelines-etl-and-warehousing-basics.md), [60. Backups Restores and Data Lifecycle Management](60-backups-restores-and-data-lifecycle-management.md)

### Phase 5: Distributed Systems

Goal: The learner can design large-scale systems.

Introduce the hard parts of many-node systems: coordination, replication, messaging, resilience, and time.

[61. Scaling Up Scaling Out and Bottlenecks](61-scaling-up-scaling-out-and-bottlenecks.md), [62. Stateless Services and Shared State](62-stateless-services-and-shared-state.md), [63. Load Balancing Reverse Proxies and Traffic Steering](63-load-balancing-reverse-proxies-and-traffic-steering.md), [64. Replication and Read Write Topologies](64-replication-and-read-write-topologies.md), [65. Partitioning Sharding and Rebalancing](65-partitioning-sharding-and-rebalancing.md), [66. Consistency Models and the CAP Lens](66-consistency-models-and-the-cap-lens.md), [67. Consensus Leader Election and Coordination](67-consensus-leader-election-and-coordination.md), [68. Messaging Queues and Publish Subscribe](68-messaging-queues-and-publish-subscribe.md), [69. Event Driven Architecture and Stream Processing](69-event-driven-architecture-and-stream-processing.md), [70. Distributed Transactions Sagas and Compensation](70-distributed-transactions-sagas-and-compensation.md), [71. Idempotency Retries and Exactly Once Myths](71-idempotency-retries-and-exactly-once-myths.md), [72. Service Discovery API Gateways and Service Meshes](72-service-discovery-api-gateways-and-service-meshes.md), [73. Fault Tolerance Backpressure and Resilience Patterns](73-fault-tolerance-backpressure-and-resilience-patterns.md), [74. Distributed Caching Coordination and Invalidation](74-distributed-caching-coordination-and-invalidation.md), [75. Time Ordering and Clocks in Distributed Systems](75-time-ordering-and-clocks-in-distributed-systems.md)

### Phase 6: Production Engineering

Goal: The learner can operate backend systems professionally.

Teach packaging, deployment, containers, orchestration, observability, and operational recovery.

[76. Building and Packaging Backend Software](76-building-and-packaging-backend-software.md), [77. Linux Service Management and Process Supervision](77-linux-service-management-and-process-supervision.md), [78. Containers Images and Runtime Isolation](78-containers-images-and-runtime-isolation.md), [79. Dockerfiles Registries and Supply Chain Security](79-dockerfiles-registries-and-supply-chain-security.md), [80. Container Networking Storage and Stateful Workloads](80-container-networking-storage-and-stateful-workloads.md), [81. Kubernetes Core Concepts](81-kubernetes-core-concepts.md), [82. Kubernetes Workloads Services and Ingress](82-kubernetes-workloads-services-and-ingress.md), [83. Cloud Fundamentals for Backend Engineers](83-cloud-fundamentals-for-backend-engineers.md), [84. Infrastructure as Code](84-infrastructure-as-code.md), [85. CI CD Pipelines and Deployment Strategies](85-ci-cd-pipelines-and-deployment-strategies.md), [86. Observability Fundamentals](86-observability-fundamentals.md), [87. Logging Metrics and Distributed Tracing](87-logging-metrics-and-distributed-tracing.md), [88. Monitoring Alerting and On Call Practices](88-monitoring-alerting-and-on-call-practices.md), [89. Reliability Engineering SLIs SLOs and Error Budgets](89-reliability-engineering-slis-slos-and-error-budgets.md), [90. Incident Response Postmortems and Disaster Recovery](90-incident-response-postmortems-and-disaster-recovery.md)

### Phase 7: Expert Backend Engineering

Goal: The learner can design systems used by millions of users.

Climb from solid implementation into architecture, trade-off communication, platform decisions, and long-term ownership.

[91. Architecture Patterns for Backend Systems](91-architecture-patterns-for-backend-systems.md), [92. Monoliths Modular Monoliths and Microservices](92-monoliths-modular-monoliths-and-microservices.md), [93. Domain Driven Design and Bounded Contexts](93-domain-driven-design-and-bounded-contexts.md), [94. Hexagonal Architecture and Dependency Boundaries](94-hexagonal-architecture-and-dependency-boundaries.md), [95. Event Sourcing CQRS and Auditability](95-event-sourcing-cqrs-and-auditability.md), [96. API Gateways BFFs and Aggregation Layers](96-api-gateways-bffs-and-aggregation-layers.md), [97. Multi Tenancy Data Isolation and SaaS Architecture](97-multi-tenancy-data-isolation-and-saas-architecture.md), [98. Performance Engineering and Capacity Planning](98-performance-engineering-and-capacity-planning.md), [99. Cost Engineering and FinOps for Backend Teams](99-cost-engineering-and-finops-for-backend-teams.md), [100. Privacy Compliance and Data Governance](100-privacy-compliance-and-data-governance.md), [101. Platform Engineering and Developer Experience](101-platform-engineering-and-developer-experience.md), [102. Migration Strategies and Legacy Modernization](102-migration-strategies-and-legacy-modernization.md), [103. Large Scale Storage and Compute Trade-offs](103-large-scale-storage-and-compute-trade-offs.md), [104. System Design Methodology and Communication](104-system-design-methodology-and-communication.md), [105. Technical Leadership Architecture Reviews and Long Term Ownership](105-technical-leadership-architecture-reviews-and-long-term-ownership.md)

## Milestones

- Milestone 1: Explain what happens below backend frameworks and trace a request through the operating system and network.
- Milestone 2: Write maintainable code with tests, debugging discipline, and clear abstractions.
- Milestone 3: Build complete backend applications with validation, authentication, asynchronous work, and stable APIs.
- Milestone 4: Model, query, cache, and recover data with confidence.
- Milestone 5: Design replicated, partitioned, resilient distributed systems.
- Milestone 6: Package, deploy, observe, and recover backend systems in production.
- Milestone 7: Make expert architecture decisions and defend them with trade-offs, metrics, and long-term ownership thinking.

## Recommended Projects

- Project 1: a tiny HTTP service whose request path you can trace with shell tools and logs.
- Project 2: a tested backend library that implements business rules with clean module boundaries.
- Project 3: a production-style CRUD or workflow API with authentication, validation, background jobs, and observability.
- Project 4: a data-heavy service that uses relational modeling, indexing, caching, backups, and search.
- Project 5: a distributed service that uses queues, retries, idempotency keys, and replicated data.
- Project 6: a containerized service deployed through CI CD with dashboards, alerts, and rollback procedures.
- Project 7: a capstone design for a system used by millions of users, complete with architecture notes, capacity model, and migration plan.

## Final Capstone Roadmap

1. Choose a realistic product domain with user traffic, asynchronous work, data growth, and clear reliability expectations.
2. Document the workload, request paths, invariants, threat model, and operational requirements before implementation.
3. Build the core service with stable APIs, persistent storage, background processing, and instrumentation from day one.
4. Introduce scale concerns deliberately: caching, queues, replication, sharding, or multi-region behavior where justified.
5. Package and deploy the system with repeatable automation, observability, and rollback procedures.
6. Present the final design as if handing it to a senior team that will operate it for years.

## How to Navigate the Files

- Start with [1. How Computers Represent Information](1-how-computers-represent-information.md) if you are new to backend engineering.
- Use the chapter numbers for the intended order; the difficulty increases gradually.
- Use the prerequisites listed in each file when you want to skip around.
- Treat the `backend-engineering/README.md` file as the map and the chapter files as the textbook itself.

## What Completion Should Feel Like

By the end of this curriculum, you should be able to trace requests from the network to the database, write maintainable backend code, model data intentionally, reason about distributed trade-offs, operate production systems safely, and explain architecture decisions in clear engineering language.
