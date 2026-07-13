#!/usr/bin/env python3
"""
Generate a backend engineering curriculum as a library of markdown chapters.
"""

from __future__ import annotations

import textwrap
import unicodedata
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "backend-engineering"
LESSON_INDEX = ROOT / "lessons" / "backend.md"


@dataclass(frozen=True)
class Topic:
    number: int
    title: str
    filename: str
    phase_number: int
    phase_name: str
    phase_goal: str
    phase_theme: str
    family: str
    prerequisites: tuple[str, ...]
    study_hours: int
    practice_hours: int
    difficulty: int


PHASES = [
    {
        "name": "Computer Foundations",
        "goal": "The learner understands what happens below backend frameworks.",
        "theme": "Build a working model of computers, operating systems, and networks before introducing application frameworks.",
        "foundations": [],
        "topics": [
            ("How Computers Represent Information", "computing"),
            ("Computer Architecture for Backend Engineers", "computing"),
            ("Operating Systems Fundamentals", "computing"),
            ("Processes Threads and Scheduling", "computing"),
            ("Memory Virtual Memory and Storage Hierarchies", "computing"),
            ("Filesystems and Persistent Storage", "computing"),
            ("Command Line Linux and Unix Thinking", "operations"),
            ("Networking Fundamentals", "networking"),
            ("How the Internet Works", "networking"),
            ("DNS and Name Resolution", "networking"),
            ("IP Routing and Packet Delivery", "networking"),
            ("TCP UDP and Transport Trade-offs", "networking"),
            ("TLS Certificates and Secure Transport", "security"),
            ("Sockets Ports and Connection Lifecycles", "networking"),
            ("Time Clocks and Failure in Computer Systems", "distributed"),
        ],
    },
    {
        "name": "Programming Foundations",
        "goal": "The learner can write maintainable software.",
        "theme": "Move from machine awareness into programming models, algorithms, debugging, and code organization.",
        "foundations": [
            "How Computers Represent Information",
            "Processes Threads and Scheduling",
            "Time Clocks and Failure in Computer Systems",
        ],
        "topics": [
            ("Programming Fundamentals and State", "programming"),
            ("Variables Types and Data Representation", "programming"),
            ("Control Flow and Error Handling", "programming"),
            ("Functions Modules and Abstractions", "programming"),
            ("Data Structures in Backend Systems", "programming"),
            ("Algorithms and Complexity for Service Engineers", "programming"),
            ("Recursion Iteration and Traversal", "programming"),
            ("Concurrency Parallelism and Synchronization", "programming"),
            ("Testing Fundamentals for Backend Code", "programming"),
            ("Debugging and Profiling Backend Programs", "programming"),
            ("Version Control and Collaborative Workflows", "programming"),
            ("Object Oriented Design and Composition", "programming"),
            ("Functional Programming and Immutability", "programming"),
            ("Clean Code Refactoring and Maintainability", "programming"),
            ("Compilers Interpreters and Runtime Environments", "programming"),
        ],
    },
    {
        "name": "Backend Development Fundamentals",
        "goal": "The learner can build complete backend applications.",
        "theme": "Introduce servers, protocols, validation, identity, and application structure from first principles.",
        "foundations": [
            "Networking Fundamentals",
            "Concurrency Parallelism and Synchronization",
            "Testing Fundamentals for Backend Code",
        ],
        "topics": [
            ("What a Server Really Is", "backend"),
            ("The Request Response Lifecycle", "backend"),
            ("HTTP Semantics Headers and Methods", "backend"),
            ("REST Resource Modeling and Trade-offs", "backend"),
            ("API Design Contracts and Evolution", "backend"),
            ("Data Serialization and Message Formats", "backend"),
            ("Input Validation and Boundary Defense", "security"),
            ("Authentication Fundamentals", "security"),
            ("Authorization and Access Control", "security"),
            ("Sessions Cookies and Tokens", "security"),
            ("Backend Application Architecture", "backend"),
            ("Routing Middleware and Dependency Injection", "backend"),
            ("Background Jobs and Asynchronous Workflows", "backend"),
            ("File Uploads Media Pipelines and Object Storage", "backend"),
            ("Configuration Secrets and Environment Management", "operations"),
        ],
    },
    {
        "name": "Data Engineering",
        "goal": "The learner understands storing and retrieving data efficiently.",
        "theme": "Teach persistence, modeling, query execution, indexing, caching, and long-term data stewardship.",
        "foundations": [
            "Backend Application Architecture",
            "Data Serialization and Message Formats",
            "Configuration Secrets and Environment Management",
        ],
        "topics": [
            ("Relational Databases and Table Design", "data"),
            ("SQL Queries Filtering and Aggregation", "data"),
            ("Joins Normalization and Schema Modeling", "data"),
            ("Indexes B Trees and Query Performance", "data"),
            ("Transactions ACID and Consistency Guarantees", "data"),
            ("Isolation Levels Locks and MVCC", "data"),
            ("Query Planning Storage Engines and Database Internals", "data"),
            ("Caching Fundamentals and Cache Invalidation", "data"),
            ("Redis and In-Memory Data Systems", "data"),
            ("NoSQL Foundations and Trade-offs", "data"),
            ("Document Databases and Schema Flexibility", "data"),
            ("Key Value Column Family and Time Series Stores", "data"),
            ("Search Indexes and Full Text Retrieval", "data"),
            ("Data Pipelines ETL and Warehousing Basics", "data"),
            ("Backups Restores and Data Lifecycle Management", "data"),
        ],
    },
    {
        "name": "Distributed Systems",
        "goal": "The learner can design large-scale systems.",
        "theme": "Introduce the hard parts of many-node systems: coordination, replication, messaging, resilience, and time.",
        "foundations": [
            "Transactions ACID and Consistency Guarantees",
            "Caching Fundamentals and Cache Invalidation",
            "Time Clocks and Failure in Computer Systems",
        ],
        "topics": [
            ("Scaling Up Scaling Out and Bottlenecks", "distributed"),
            ("Stateless Services and Shared State", "distributed"),
            ("Load Balancing Reverse Proxies and Traffic Steering", "distributed"),
            ("Replication and Read Write Topologies", "distributed"),
            ("Partitioning Sharding and Rebalancing", "distributed"),
            ("Consistency Models and the CAP Lens", "distributed"),
            ("Consensus Leader Election and Coordination", "distributed"),
            ("Messaging Queues and Publish Subscribe", "distributed"),
            ("Event Driven Architecture and Stream Processing", "distributed"),
            ("Distributed Transactions Sagas and Compensation", "distributed"),
            ("Idempotency Retries and Exactly Once Myths", "distributed"),
            ("Service Discovery API Gateways and Service Meshes", "distributed"),
            ("Fault Tolerance Backpressure and Resilience Patterns", "distributed"),
            ("Distributed Caching Coordination and Invalidation", "distributed"),
            ("Time Ordering and Clocks in Distributed Systems", "distributed"),
        ],
    },
    {
        "name": "Production Engineering",
        "goal": "The learner can operate backend systems professionally.",
        "theme": "Teach packaging, deployment, containers, orchestration, observability, and operational recovery.",
        "foundations": [
            "Scaling Up Scaling Out and Bottlenecks",
            "Fault Tolerance Backpressure and Resilience Patterns",
            "Configuration Secrets and Environment Management",
        ],
        "topics": [
            ("Building and Packaging Backend Software", "operations"),
            ("Linux Service Management and Process Supervision", "operations"),
            ("Containers Images and Runtime Isolation", "operations"),
            ("Dockerfiles Registries and Supply Chain Security", "operations"),
            ("Container Networking Storage and Stateful Workloads", "operations"),
            ("Kubernetes Core Concepts", "operations"),
            ("Kubernetes Workloads Services and Ingress", "operations"),
            ("Cloud Fundamentals for Backend Engineers", "operations"),
            ("Infrastructure as Code", "operations"),
            ("CI CD Pipelines and Deployment Strategies", "operations"),
            ("Observability Fundamentals", "operations"),
            ("Logging Metrics and Distributed Tracing", "operations"),
            ("Monitoring Alerting and On Call Practices", "operations"),
            ("Reliability Engineering SLIs SLOs and Error Budgets", "operations"),
            ("Incident Response Postmortems and Disaster Recovery", "operations"),
        ],
    },
    {
        "name": "Expert Backend Engineering",
        "goal": "The learner can design systems used by millions of users.",
        "theme": "Climb from solid implementation into architecture, trade-off communication, platform decisions, and long-term ownership.",
        "foundations": [
            "Backend Application Architecture",
            "Consistency Models and the CAP Lens",
            "Observability Fundamentals",
        ],
        "topics": [
            ("Architecture Patterns for Backend Systems", "architecture"),
            ("Monoliths Modular Monoliths and Microservices", "architecture"),
            ("Domain Driven Design and Bounded Contexts", "architecture"),
            ("Hexagonal Architecture and Dependency Boundaries", "architecture"),
            ("Event Sourcing CQRS and Auditability", "architecture"),
            ("API Gateways BFFs and Aggregation Layers", "architecture"),
            ("Multi Tenancy Data Isolation and SaaS Architecture", "architecture"),
            ("Performance Engineering and Capacity Planning", "architecture"),
            ("Cost Engineering and FinOps for Backend Teams", "architecture"),
            ("Privacy Compliance and Data Governance", "architecture"),
            ("Platform Engineering and Developer Experience", "architecture"),
            ("Migration Strategies and Legacy Modernization", "architecture"),
            ("Large Scale Storage and Compute Trade-offs", "architecture"),
            ("System Design Methodology and Communication", "architecture"),
            ("Technical Leadership Architecture Reviews and Long Term Ownership", "architecture"),
        ],
    },
]


FAMILY_PROFILES = {
    "computing": {
        "domain": "the machine-level environment that hosts backend software",
        "why": "Backend engineers eventually debug CPU saturation, page faults, file descriptor leaks, memory pressure, and syscall behavior, even when they spend most days writing application code.",
        "where": "kernel tuning, performance investigations, container limits, storage debugging, and production incidents that look like application bugs but are really operating-environment bugs",
        "history": "Modern backend systems inherit decades of ideas from time-sharing, Unix processes, virtual memory, and storage hierarchies. Those choices still shape service behavior today.",
        "first_principles": "At the lowest level, backend programs are instructions executing on cores, reading and writing bytes through registers, caches, RAM, disks, and kernel-managed devices.",
        "abstractions": "Frameworks hide syscalls, page tables, scheduler decisions, interrupt handling, and buffer caches.",
        "components": [
            "CPU cores, caches, and branch prediction",
            "Kernel scheduler and system call interface",
            "Memory pages, address spaces, and allocators",
            "Block devices, filesystems, and buffer caches",
            "Process tables, file descriptors, and signals",
        ],
        "metrics": "CPU utilization, load average, context switches, page faults, IOPS, syscall latency, and open file descriptors",
        "tools": ["top", "htop", "vmstat", "iostat", "lsof", "strace"],
        "algorithms": [
            "Scheduling policies decide which runnable work gets CPU time next.",
            "Virtual memory maps process addresses to physical pages on demand.",
            "Buffer-cache policies trade memory usage for disk-read avoidance.",
            "Filesystem journaling trades write amplification for crash recovery.",
        ],
    },
    "networking": {
        "domain": "packets, addressing, transport protocols, and encrypted links between systems",
        "why": "Almost every backend feature eventually becomes a network conversation, so performance, reliability, and security depend on understanding the path those bytes travel.",
        "where": "API calls, database connections, service-to-service traffic, CDN requests, mobile clients, and incident analysis during timeouts or packet loss",
        "history": "The Internet was designed to connect unreliable networks, which is why modern services still inherit layered protocols, best-effort delivery, and strong separation between naming, routing, and transport.",
        "first_principles": "At the lowest level, data is divided into packets or segments, wrapped in protocol headers, transmitted over links, routed across networks, and reassembled by the receiving host.",
        "abstractions": "High-level clients hide retries, handshakes, routing tables, congestion control, socket buffers, and packet capture detail.",
        "components": [
            "Network interfaces, switches, routers, and firewalls",
            "DNS resolvers, routing tables, and ARP or neighbor caches",
            "Transport state such as sequence numbers and acknowledgements",
            "Socket buffers, kernel queues, and application read loops",
            "TLS handshakes, certificates, and key negotiation",
        ],
        "metrics": "RTT, packet loss, jitter, retransmissions, bandwidth, connection counts, handshake time, and tail latency",
        "tools": ["curl", "dig", "traceroute", "ss", "tcpdump", "openssl"],
        "algorithms": [
            "Routing algorithms choose a next hop based on destination prefixes.",
            "Congestion-control algorithms balance throughput against fairness and loss.",
            "DNS caching algorithms reduce lookup cost but introduce staleness trade-offs.",
            "TLS handshake design trades CPU work for confidentiality and integrity.",
        ],
    },
    "programming": {
        "domain": "code, state transitions, algorithms, and runtime behavior inside a backend program",
        "why": "Backend reliability starts with code that is understandable, testable, and predictable under load, failure, and change.",
        "where": "business rules, data transformations, concurrency control, validation layers, test suites, and debugging sessions",
        "history": "Programming practice evolved from machine instructions to high-level languages, modules, testing, and refactoring because large systems became impossible to manage as raw control flow alone.",
        "first_principles": "A program is a set of rules that transform input state into output state. The machine executes those rules through parsing, runtime dispatch, memory allocation, and I/O coordination.",
        "abstractions": "Languages and frameworks hide stack frames, heap allocation, dispatch tables, scheduler behavior, and object layout.",
        "components": [
            "Source files, modules, and runtime entry points",
            "Functions or methods that transform state",
            "Data structures that shape access patterns",
            "Synchronization primitives and memory visibility rules",
            "Tests, profilers, and debuggers for feedback",
        ],
        "metrics": "cyclomatic complexity, mutation rate, test signal quality, allocation rate, lock contention, and profiling hot spots",
        "tools": ["go test", "go tool pprof", "node --inspect", "tsc", "git", "benchmarks"],
        "algorithms": [
            "Choice of data structure determines lookup and update complexity.",
            "Control-flow structure determines how easily humans can reason about correctness.",
            "Synchronization design determines whether concurrency is safe or accidental.",
            "Refactoring is a change in structure that preserves behavior while lowering future cost.",
        ],
    },
    "backend": {
        "domain": "servers, request handling, application boundaries, and asynchronous workflows",
        "why": "This is the layer where user intent becomes durable state changes, external side effects, and business behavior visible to clients.",
        "where": "web APIs, internal services, file-processing pipelines, webhook handlers, admin tools, and background workers",
        "history": "Backend application design grew from CGI scripts and simple RPC calls into layered services with routing, middleware, validation, identity, caching, and async job systems.",
        "first_principles": "A backend receives bytes from a network, parses them into a protocol message, validates intent, executes business logic, performs I/O, and emits a response or background action.",
        "abstractions": "Frameworks hide connection pooling, request parsing, middleware chaining, serialization cost, queue coordination, and cancellation propagation.",
        "components": [
            "Listeners, routers, handlers, and middleware",
            "Validation, authorization, and business-rule layers",
            "Repositories, clients, queues, and storage adapters",
            "Serialization, logging, tracing, and configuration systems",
            "Retry, timeout, and cancellation boundaries",
        ],
        "metrics": "requests per second, p95 latency, error rate, queue depth, timeout rate, and saturation at downstream dependencies",
        "tools": ["curl", "wrk", "OpenAPI", "grpcurl", "Go net/http", "Node runtimes"],
        "algorithms": [
            "Routing tables map protocol or path shapes to execution paths.",
            "Validation logic turns external input into trusted internal data.",
            "Queueing and worker models separate interactive latency from deferred work.",
            "Timeout and retry policies decide when to fail fast versus keep trying.",
        ],
    },
    "security": {
        "domain": "trust boundaries, identity, authorization, transport security, and secret handling",
        "why": "A backend system is trusted with user data and privileged operations, so misunderstanding identity or secrecy turns ordinary bugs into breaches.",
        "where": "login systems, service credentials, TLS endpoints, session stores, policy engines, audit trails, and compliance reviews",
        "history": "Backend security matured as services became public, programmable, and highly interconnected. Identity, confidentiality, and least privilege all grew from repeated failure and attack.",
        "first_principles": "Security begins by asking who controls the input, what authority is being requested, which secrets or identities are involved, and which boundary must reject malicious or accidental misuse.",
        "abstractions": "Auth libraries hide signature verification, session rotation, password hashing, certificate validation, and policy-evaluation details.",
        "components": [
            "Credentials, sessions, tokens, and policy rules",
            "Certificate chains, key stores, and secure channels",
            "Secret stores, rotation workflows, and audit logs",
            "Identity providers, application services, and resource servers",
            "Rate limits, anomaly detection, and incident playbooks",
        ],
        "metrics": "failed login rate, token age, secret rotation age, privilege escalation risk, audit coverage, and incident count",
        "tools": ["openssl", "jwt-cli", "vault", "sso providers", "audit logs", "policy engines"],
        "algorithms": [
            "Cryptographic handshakes establish confidentiality and authenticity.",
            "Token or session verification maps presented identity to trusted claims.",
            "Authorization engines evaluate policy against subject, action, and resource.",
            "Secret-rotation workflows reduce the blast radius of inevitable compromise.",
        ],
    },
    "data": {
        "domain": "persistent state, query execution, indexes, caches, and data lifecycle decisions",
        "why": "Backend systems live or die by how efficiently they store, retrieve, isolate, and recover data under real workload patterns.",
        "where": "OLTP databases, analytics pipelines, caches, search systems, backups, and data migrations",
        "history": "Database design evolved through relational theory, transaction research, storage engines, and eventually many specialized systems tuned for scale, latency, and workload diversity.",
        "first_principles": "Persistent systems turn writes into durable records, organize them for future reads, enforce invariants, and balance correctness against latency, cost, and flexibility.",
        "abstractions": "ORMs and client libraries hide execution plans, lock behavior, cache invalidation, write amplification, and replication lag.",
        "components": [
            "Tables or collections, indexes, and storage engines",
            "Transaction logs, buffer pools, and checkpointing",
            "Query parsers, optimizers, and executors",
            "Replication, backup, and recovery pipelines",
            "Caches, search indexes, and archival storage",
        ],
        "metrics": "p95 query latency, cache hit rate, lock wait time, replication lag, storage growth, and recovery-point objectives",
        "tools": ["psql", "EXPLAIN", "redis-cli", "query analyzers", "backup tools", "migration runners"],
        "algorithms": [
            "B-trees, hash tables, and inverted indexes optimize different access patterns.",
            "Transaction protocols decide when changes become visible and durable.",
            "Query optimizers search among join orders and access paths.",
            "Eviction and invalidation strategies decide whether a cache is helpful or dangerous.",
        ],
    },
    "distributed": {
        "domain": "many-node coordination, failure handling, replication, and network-aware scalability",
        "why": "As soon as a backend has multiple instances, regions, or asynchronous components, local assumptions stop being enough and distributed-systems trade-offs become real.",
        "where": "load-balanced APIs, replicated databases, message brokers, multi-region deployments, and event-driven architectures",
        "history": "Distributed systems became central once services outgrew single machines. The field is shaped by failure, partial connectivity, unreliable clocks, and the need to scale without losing correctness.",
        "first_principles": "Distributed systems are collections of independent computers that communicate by messages, fail independently, and never share a perfectly reliable clock or network.",
        "abstractions": "Cloud platforms and service meshes hide retry storms, split-brain risk, quorum math, duplicate delivery, and consistency lag.",
        "components": [
            "Nodes, replicas, partitions, and coordinators",
            "Load balancers, service discovery, and routing layers",
            "Queues, logs, stream processors, and consumer groups",
            "Quorums, leases, leader-election systems, and heartbeats",
            "Circuit breakers, retry budgets, and backpressure signals",
        ],
        "metrics": "availability, quorum health, replication lag, queue lag, rebalance time, tail latency, and error-budget burn",
        "tools": ["load generators", "tracing", "broker CLIs", "cluster dashboards", "failover drills", "chaos tests"],
        "algorithms": [
            "Consensus algorithms coordinate state under partial failure.",
            "Partitioning algorithms distribute load while trying to avoid hotspots.",
            "Retry, deduplication, and idempotency logic absorb duplicate delivery.",
            "Backpressure strategies prevent fast producers from overwhelming slower consumers.",
        ],
    },
    "operations": {
        "domain": "builds, deployment, runtime management, observability, and incident handling",
        "why": "Production engineering turns code into a service people can depend on. Without it, a correct backend is still not a usable system.",
        "where": "CI systems, container platforms, cloud accounts, dashboards, alerts, release pipelines, and post-incident learning loops",
        "history": "Operational practice grew from manual server administration into infrastructure automation, containers, orchestration, SRE, and continuous delivery as service complexity and release speed increased.",
        "first_principles": "Operating a backend means producing a verified artifact, placing it in a controlled runtime, observing its behavior, and restoring service quickly when assumptions fail.",
        "abstractions": "Managed platforms hide image layers, orchestration loops, rollout state machines, network policies, and telemetry pipelines.",
        "components": [
            "Build pipelines, artifact stores, and release metadata",
            "Processes, containers, schedulers, and service discovery",
            "Secrets, config, policy, and identity infrastructure",
            "Metrics, logs, traces, dashboards, and alerts",
            "Runbooks, rollback tooling, and disaster-recovery plans",
        ],
        "metrics": "deployment frequency, lead time, MTTR, change failure rate, restart counts, memory saturation, and error-budget burn",
        "tools": ["docker", "kubectl", "terraform", "prometheus", "grafana", "ci platforms"],
        "algorithms": [
            "Image-layer construction reduces rebuild time through caching.",
            "Schedulers reconcile desired state against actual state repeatedly.",
            "Rollout strategies trade delivery speed against blast radius.",
            "Alerting and SLO math turn raw telemetry into operational decisions.",
        ],
    },
    "architecture": {
        "domain": "long-lived system structure, team boundaries, trade-offs, and strategic technical direction",
        "why": "Expert backend work is less about a single endpoint and more about shaping systems so they remain understandable, operable, and changeable for years.",
        "where": "system design reviews, platform strategy, service decomposition, migration plans, governance models, and leadership decision-making",
        "history": "Architecture practice grew as software systems lasted longer, teams grew larger, and cost of change became as important as initial delivery speed.",
        "first_principles": "Architecture is applied trade-off management: deciding where responsibilities live, how data flows, how failures are isolated, and how teams can change the system safely.",
        "abstractions": "High-level diagrams hide organizational incentives, migration cost, ownership gaps, and long-term coupling.",
        "components": [
            "Domain boundaries, service boundaries, and team interfaces",
            "Data contracts, event contracts, and policy constraints",
            "Operational guardrails, review processes, and ADRs",
            "Migration paths, compatibility promises, and rollback plans",
            "Performance, cost, and reliability budgets",
        ],
        "metrics": "change lead time, coupling, blast radius, cost per request, cognitive load, and long-term platform adoption",
        "tools": ["ADRs", "RFCs", "sequence diagrams", "load tests", "architecture reviews", "capacity models"],
        "algorithms": [
            "Architectural decomposition tries to localize change and failure.",
            "Capacity planning turns workload assumptions into hardware and cloud decisions.",
            "Compatibility strategies preserve evolution without breaking consumers.",
            "Governance mechanisms trade autonomy against consistency and safety.",
        ],
    },
}


FAMILY_TERMS = {
    "computing": [
        ("Instruction", "A low-level operation executed by the CPU against registers, memory addresses, or control flow."),
        ("System call", "A controlled transition from user space into the kernel so a program can ask the operating system for privileged work."),
        ("Address space", "The virtual memory range a process believes it owns."),
    ],
    "networking": [
        ("Packet", "A unit of network transmission that carries headers plus payload data."),
        ("Protocol", "A shared rule set that lets independent machines interpret bytes in the same way."),
        ("Socket", "The operating-system object that binds application code to network communication."),
    ],
    "programming": [
        ("State", "The collection of values that affect future behavior of a program."),
        ("Invariant", "A property that must remain true if the program is behaving correctly."),
        ("Abstraction", "A boundary that hides detail so humans can reason at the right level."),
    ],
    "backend": [
        ("Handler", "The code path that turns a request into a response or a scheduled side effect."),
        ("Boundary", "The place where external input becomes trusted internal state only after validation."),
        ("Latency", "The time a user or another service waits before seeing the result of a request."),
    ],
    "security": [
        ("Trust boundary", "A point where the system must stop assuming the caller is safe or truthful."),
        ("Least privilege", "The practice of granting only the minimum permissions required."),
        ("Credential", "A secret or proof used to establish identity."),
    ],
    "data": [
        ("Durability", "The guarantee that acknowledged data survives crashes or restarts."),
        ("Index", "An auxiliary structure that speeds reads by pre-organizing lookup paths."),
        ("Consistency", "The degree to which readers observe rules and expectations after writes occur."),
    ],
    "distributed": [
        ("Partial failure", "A state where some components fail while others continue running."),
        ("Quorum", "A minimum subset of participants whose agreement is treated as enough to proceed."),
        ("Backpressure", "A signal that downstream systems cannot safely accept more work at the current rate."),
    ],
    "operations": [
        ("Artifact", "A build output such as a binary, container image, or manifest that can be promoted through environments."),
        ("Rollout", "A controlled release of a new version into a running system."),
        ("Telemetry", "Machine-generated signals about system behavior, such as logs, metrics, and traces."),
    ],
    "architecture": [
        ("Coupling", "The degree to which one part of a system depends on internal details of another."),
        ("Boundary", "A line of ownership, responsibility, or isolation inside a system."),
        ("Trade-off", "A decision that improves one quality at the expense of another."),
    ],
}


KEYWORD_TERMS = {
    "dns": [
        ("Resolver", "The component that asks DNS servers for records and caches the answers."),
        ("TTL", "Time to live, the caching duration attached to a DNS record."),
        ("Authoritative server", "The server responsible for the final answer about a particular zone."),
    ],
    "tcp": [
        ("Handshake", "The setup exchange that establishes transport state before useful application data flows."),
        ("Retransmission", "Resending data when acknowledgements do not arrive in time."),
        ("Flow control", "A mechanism that prevents the sender from overwhelming the receiver."),
    ],
    "udp": [
        ("Datagram", "An independent message sent without built-in delivery guarantees."),
        ("Loss tolerance", "The application-level ability to survive dropped or reordered packets."),
    ],
    "tls": [
        ("Certificate chain", "A linked proof structure that helps a client decide whether to trust the presented identity."),
        ("Session key", "A short-lived symmetric key used after the handshake completes."),
        ("Cipher suite", "The negotiated set of cryptographic algorithms used for the connection."),
    ],
    "socket": [
        ("Listen backlog", "The queue of pending incoming connections waiting to be accepted."),
        ("Ephemeral port", "A temporary local port chosen by the operating system for an outbound connection."),
    ],
    "thread": [
        ("Thread", "A sequence of execution scheduled within the context of a process."),
        ("Context switch", "The scheduler action that pauses one thread and resumes another."),
    ],
    "process": [
        ("Process", "An isolated execution context with its own virtual memory and operating-system resources."),
    ],
    "memory": [
        ("Page", "A fixed-size block used by virtual memory systems for mapping and protection."),
        ("Cache line", "A small chunk of memory transferred between RAM and CPU caches."),
        ("Heap", "The region used for dynamic allocation during a program's lifetime."),
    ],
    "filesystem": [
        ("Inode", "Filesystem metadata describing ownership, permissions, and block pointers for a file."),
        ("Journal", "A write-ahead record that helps recover consistency after crashes."),
        ("fsync", "A request to flush buffered writes to durable storage."),
    ],
    "concurrency": [
        ("Race condition", "A bug caused by behavior depending on timing or interleaving."),
        ("Mutex", "A primitive that allows only one participant into a critical section at a time."),
        ("Deadlock", "A state where participants wait on each other forever."),
    ],
    "testing": [
        ("Test oracle", "The rule that determines whether the observed behavior is correct."),
        ("Fixture", "The setup data or environment a test depends on."),
        ("Flake", "A test that fails nondeterministically without a real behavioral change."),
    ],
    "debugging": [
        ("Breakpoint", "A deliberate pause point used to inspect state during execution."),
        ("Sampling profiler", "A tool that observes stack frames over time to estimate where runtime is spent."),
    ],
    "http": [
        ("Method", "The verb that tells the server the intended semantics of the request."),
        ("Header", "Metadata attached to an HTTP message."),
        ("Status code", "A standardized numeric summary of the outcome of a request."),
    ],
    "rest": [
        ("Resource", "A conceptual entity addressed through a stable identifier."),
        ("Representation", "The transmitted form of a resource at a point in time."),
        ("Idempotency", "The property that repeating a request has the same effect as performing it once."),
    ],
    "api": [
        ("Contract", "A promise about shape, semantics, and compatibility that callers rely on."),
        ("Backward compatibility", "The discipline of evolving behavior without breaking existing consumers."),
        ("Schema", "A formal description of expected data structure and meaning."),
    ],
    "serialization": [
        ("Encoding", "The transformation of in-memory structures into a transmissible byte format."),
        ("Schema evolution", "The ability to change message shapes while keeping old and new readers compatible."),
    ],
    "validation": [
        ("Canonical form", "A normalized representation used internally after input has been checked and cleaned."),
        ("Boundary defense", "The practice of rejecting malformed or dangerous input at system edges."),
    ],
    "authentication": [
        ("Identity proof", "Evidence that the caller is who they claim to be."),
        ("Session", "A server-recognized continuity of identity across multiple requests."),
    ],
    "authorization": [
        ("Principal", "The actor whose permissions are being evaluated."),
        ("Policy", "The rule set that determines what actions are allowed."),
        ("Permission", "An allowed action over a resource under specific conditions."),
    ],
    "token": [
        ("Bearer token", "A credential that grants access to whoever presents it."),
        ("Refresh token", "A longer-lived credential used to obtain new short-lived access tokens."),
    ],
    "database": [
        ("Relation", "A set of tuples described by a fixed attribute schema."),
        ("Primary key", "The attribute or attributes that uniquely identify a row."),
        ("Constraint", "A rule the database enforces to preserve data validity."),
    ],
    "sql": [
        ("Predicate", "A condition used to filter rows."),
        ("Projection", "Selecting the columns or expressions to return."),
        ("Aggregation", "Combining many rows into summary values."),
    ],
    "join": [
        ("Join condition", "The rule that tells the database how to combine rows from multiple relations."),
        ("Cardinality", "The shape and count of matching rows between datasets."),
        ("Normalization", "Organizing schema to reduce redundancy and update anomalies."),
    ],
    "index": [
        ("B-tree", "A balanced tree optimized for disk-friendly ordered lookup."),
        ("Selectivity", "How well a condition narrows the possible result set."),
        ("Covering index", "An index containing enough columns to satisfy a query without extra table reads."),
    ],
    "transaction": [
        ("Atomicity", "All changes in a unit happen together or none happen at all."),
        ("Commit log", "An append-oriented record that captures durable transactional intent."),
        ("Write-ahead logging", "Persisting intent before mutating primary pages so recovery remains possible."),
    ],
    "isolation": [
        ("Snapshot", "A transaction's chosen view of data at a logical point in time."),
        ("Lock", "A coordination mechanism that restricts concurrent access."),
        ("Write skew", "A subtle anomaly where concurrent transactions each preserve local rules but violate a global one."),
    ],
    "cache": [
        ("Cache key", "The deterministic identity used to look up cached data."),
        ("Eviction", "Choosing which cached item to remove when space is needed."),
        ("Staleness", "The gap between cached data and the current source of truth."),
    ],
    "redis": [
        ("In-memory store", "A system optimized for keeping active data in RAM for very low latency."),
        ("Persistence mode", "The strategy a memory-first store uses to survive restarts."),
    ],
    "nosql": [
        ("Denormalization", "Storing repeated data on purpose to optimize reads or distribution."),
        ("Partition key", "The field used to distribute data across nodes."),
    ],
    "document": [
        ("Document", "A self-contained record that can nest related data together."),
        ("Schema drift", "Organic change in record shape when strong schema control is missing."),
    ],
    "search": [
        ("Inverted index", "A structure that maps terms to the documents containing them."),
        ("Tokenization", "Breaking text into searchable terms."),
        ("Ranking", "Ordering results by estimated relevance."),
    ],
    "replication": [
        ("Replica", "A copy of data maintained on another node."),
        ("Replication lag", "The delay between the primary accepting a write and replicas reflecting it."),
        ("Failover", "Promoting or redirecting traffic to a replacement when a node fails."),
    ],
    "sharding": [
        ("Shard key", "The field or function used to split data across partitions."),
        ("Hot partition", "A shard receiving disproportionate traffic compared with peers."),
        ("Rebalancing", "Moving data or traffic to smooth load across shards."),
    ],
    "consistency": [
        ("Linearizability", "A strong guarantee that operations appear to occur in a single global order."),
        ("Eventual consistency", "A weaker guarantee that replicas converge if updates stop."),
    ],
    "consensus": [
        ("Quorum", "The minimum agreeing subset required to make a decision safely."),
        ("Leader election", "The protocol step that decides which node coordinates replicated state."),
        ("Log replication", "Copying ordered commands to peers so they can converge on the same state."),
    ],
    "queue": [
        ("Consumer", "The worker that pulls or receives messages to process."),
        ("Acknowledgement", "The signal that work completed and the broker may discard or advance it."),
        ("Visibility timeout", "A window during which a claimed message should not be delivered elsewhere."),
    ],
    "event": [
        ("Event", "A record that something happened, usually expressed as an immutable fact."),
        ("Projection", "A derived view built from a stream of events."),
        ("Replay", "Reprocessing historical events to rebuild state or compute new outputs."),
    ],
    "idempotency": [
        ("Idempotency key", "A client- or server-generated value used to collapse duplicate attempts into one effect."),
        ("Deduplication", "Detecting and discarding repeated work that represents the same intent."),
    ],
    "container": [
        ("Namespace", "A kernel feature that gives a process a constrained view of system resources."),
        ("cgroup", "A kernel mechanism for accounting and limiting resource usage."),
        ("Image layer", "An immutable filesystem slice reused across container images."),
    ],
    "docker": [
        ("Layer cache", "Reusing unchanged build steps to accelerate repeated image builds."),
        ("Registry", "A service that stores and distributes container images."),
        ("SBOM", "A software bill of materials describing packaged dependencies."),
    ],
    "kubernetes": [
        ("Pod", "The basic scheduling unit that groups one or more tightly related containers."),
        ("Controller", "A loop that continuously drives actual cluster state toward desired state."),
        ("Desired state", "The declarative target the orchestration system tries to maintain."),
    ],
    "cloud": [
        ("Region", "A geographic deployment area containing multiple failure domains."),
        ("Availability zone", "A partially isolated failure domain within a region."),
        ("Managed service", "An externalized building block where the provider runs significant parts of the operational burden."),
    ],
    "observability": [
        ("Log", "A timestamped record of discrete events or state changes."),
        ("Metric", "A numeric measurement captured over time."),
        ("Trace", "A causally linked record of work moving through a distributed request path."),
    ],
    "slo": [
        ("SLI", "A measured indicator of a user-facing property such as latency or availability."),
        ("SLO", "The target range that defines acceptable behavior for an SLI."),
        ("Error budget", "The amount of unreliability a team can spend before reliability work must dominate feature work."),
    ],
    "incident": [
        ("Mitigation", "The action that reduces user harm before the root cause is fully understood."),
        ("Postmortem", "A blameless written explanation of what happened and what will change."),
        ("Runbook", "A prepared set of operational steps for predictable failure modes."),
    ],
    "ddd": [
        ("Bounded context", "A boundary within which a term or model has one consistent meaning."),
        ("Ubiquitous language", "The shared vocabulary used by developers and domain experts."),
        ("Aggregate", "A consistency boundary that groups related state changes together."),
    ],
    "hexagonal": [
        ("Port", "An abstract interface describing what the application needs from the outside world."),
        ("Adapter", "A concrete implementation that satisfies a port using a particular technology."),
        ("Dependency inversion", "Depending on stable abstractions instead of unstable implementation details."),
    ],
    "cqrs": [
        ("Command model", "The write side that enforces business rules and produces durable changes."),
        ("Read model", "The query-optimized projection built for efficient reads."),
        ("Projection lag", "The delay between a write being accepted and a read model reflecting it."),
    ],
    "multi tenancy": [
        ("Tenant", "A customer or organization whose data and behavior must remain isolated."),
        ("Noisy neighbor", "A tenant whose workload harms the experience of others on shared infrastructure."),
        ("Isolation boundary", "The technical layer where per-tenant separation is enforced."),
    ],
    "performance": [
        ("Latency percentile", "A response-time statistic that reflects how slow the tail of the distribution is."),
        ("Throughput", "How much work a system completes per unit of time."),
        ("Saturation", "How fully a resource is being utilized relative to its safe capacity."),
    ],
    "system design": [
        ("Workload", "The shape of requests, reads, writes, fan-out, and traffic variation the system must handle."),
        ("Bottleneck", "The resource or dependency that currently limits system behavior."),
        ("Trade-off", "A design choice that improves some qualities by making others worse."),
    ],
    "leadership": [
        ("Decision record", "A durable explanation of what was chosen, why, and under what assumptions."),
        ("Ownership", "The ongoing responsibility to improve, operate, and evolve a system."),
    ],
}


EXACT_OVERRIDES = {
    "How the Internet Works": {
        "diagram": """\
flowchart LR
    A["Browser or client"] --> B["DNS lookup"]
    B --> C["TCP or QUIC setup"]
    C --> D["TLS handshake"]
    D --> E["Load balancer or edge"]
    E --> F["Application service"]
    F --> G["Database or cache"]
    G --> F
    F --> E
    E --> A
""",
    },
    "DNS and Name Resolution": {
        "diagram": """\
sequenceDiagram
    participant Client
    participant Resolver
    participant Root
    participant TLD
    participant Auth as Authoritative
    Client->>Resolver: Query api.example.com
    Resolver->>Root: Where is .com?
    Root-->>Resolver: Ask .com TLD
    Resolver->>TLD: Where is example.com?
    TLD-->>Resolver: Ask authoritative server
    Resolver->>Auth: A or AAAA for api.example.com?
    Auth-->>Resolver: Final answer plus TTL
    Resolver-->>Client: Cached result
""",
        "example_language": "bash",
        "example_code": """\
dig api.example.com
dig +trace api.example.com
dig api.example.com @1.1.1.1
""",
    },
    "TCP UDP and Transport Trade-offs": {
        "diagram": """\
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: SYN
    Server-->>Client: SYN-ACK
    Client->>Server: ACK
    Client->>Server: Application bytes
    Server-->>Client: ACKs and responses
""",
    },
    "TLS Certificates and Secure Transport": {
        "example_language": "bash",
        "example_code": """\
openssl s_client -connect api.example.com:443 -servername api.example.com
openssl x509 -in server.crt -text -noout
curl -vk https://api.example.com/health
""",
    },
    "What a Server Really Is": {
        "example_language": "go",
        "example_code": """\
package main

import (
    "fmt"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintln(w, "ok")
    })

    log.Fatal(http.ListenAndServe(":8080", nil))
}
""",
    },
    "The Request Response Lifecycle": {
        "diagram": """\
sequenceDiagram
    participant Client
    participant LB as Load Balancer
    participant App as Application
    participant DB as Database
    Client->>LB: HTTP request
    LB->>App: Forwarded request
    App->>App: Parse, validate, authorize
    App->>DB: Query or write
    DB-->>App: Result
    App-->>LB: Serialized response
    LB-->>Client: HTTP response
""",
    },
    "HTTP Semantics Headers and Methods": {
        "example_language": "bash",
        "example_code": """\
curl -i https://api.example.com/orders/123
curl -i -X POST https://api.example.com/orders \\
  -H 'Content-Type: application/json' \\
  -d '{"customerId":"cust_123","amountCents":4500}'
""",
    },
    "Authentication Fundamentals": {
        "example_language": "go",
        "example_code": """\
func verifyPassword(input, storedHash string) error {
    return bcrypt.CompareHashAndPassword([]byte(storedHash), []byte(input))
}
""",
    },
    "Authorization and Access Control": {
        "example_language": "go",
        "example_code": """\
func canReadInvoice(user User, invoice Invoice) bool {
    return user.Role == "admin" || user.AccountID == invoice.AccountID
}
""",
    },
    "Sessions Cookies and Tokens": {
        "example_language": "typescript",
        "example_code": """\
type Session = { userId: string; expiresAt: number };

function isSessionValid(session: Session, now: number): boolean {
  return now < session.expiresAt;
}
""",
    },
    "SQL Queries Filtering and Aggregation": {
        "example_language": "sql",
        "example_code": """\
SELECT customer_id, COUNT(*) AS order_count, SUM(total_cents) AS revenue_cents
FROM orders
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY revenue_cents DESC
LIMIT 20;
""",
    },
    "Indexes B Trees and Query Performance": {
        "example_language": "sql",
        "example_code": """\
CREATE INDEX idx_orders_customer_created_at
ON orders (customer_id, created_at DESC);

EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC
LIMIT 20;
""",
    },
    "Transactions ACID and Consistency Guarantees": {
        "diagram": """\
sequenceDiagram
    participant App
    participant DB
    App->>DB: BEGIN
    App->>DB: debit source account
    App->>DB: credit destination account
    App->>DB: insert audit row
    App->>DB: COMMIT
    DB-->>App: durable success or rollback
""",
    },
    "Isolation Levels Locks and MVCC": {
        "diagram": """\
flowchart LR
    A["Transaction A starts"] --> B["Reads snapshot version 10"]
    C["Transaction B writes version 11"] --> D["Commits"]
    B --> E["Transaction A keeps reading snapshot 10"]
    D --> F["Future transactions see version 11"]
""",
    },
    "Redis and In-Memory Data Systems": {
        "example_language": "bash",
        "example_code": """\
redis-cli SET rate_limit:user_42 1 EX 60 NX
redis-cli INCR checkout:attempts
redis-cli HSET session:abc123 userId 42 scope billing
""",
    },
    "Load Balancing Reverse Proxies and Traffic Steering": {
        "diagram": """\
flowchart LR
    A["Clients"] --> B["Reverse proxy or LB"]
    B --> C["Service instance 1"]
    B --> D["Service instance 2"]
    B --> E["Service instance 3"]
    C --> F["Shared datastore"]
    D --> F
    E --> F
""",
    },
    "Messaging Queues and Publish Subscribe": {
        "diagram": """\
flowchart LR
    A["Producer"] --> B["Queue or broker"]
    B --> C["Consumer group A"]
    B --> D["Consumer group B"]
    C --> E["Database"]
    D --> F["Email or webhook service"]
""",
    },
    "Event Driven Architecture and Stream Processing": {
        "diagram": """\
flowchart LR
    A["Order created event"] --> B["Event log"]
    B --> C["Inventory projection"]
    B --> D["Billing projection"]
    B --> E["Analytics stream job"]
""",
    },
    "Distributed Transactions Sagas and Compensation": {
        "diagram": """\
flowchart LR
    A["Reserve inventory"] --> B["Charge payment"]
    B --> C["Create shipment"]
    C --> D["Success"]
    B -. failure .-> E["Compensate inventory reservation"]
""",
    },
    "Idempotency Retries and Exactly Once Myths": {
        "example_language": "go",
        "example_code": """\
func processPayment(ctx context.Context, key string, request ChargeRequest) error {
    if alreadyProcessed(key) {
        return nil
    }
    if err := chargeCard(ctx, request); err != nil {
        return err
    }
    markProcessed(key)
    return nil
}
""",
    },
    "Kubernetes Core Concepts": {
        "diagram": """\
flowchart LR
    A["Deployment"] --> B["ReplicaSet"]
    B --> C["Pod 1"]
    B --> D["Pod 2"]
    E["Service"] --> C
    E --> D
    F["Node"] --> C
    G["Node"] --> D
""",
        "example_language": "yaml",
        "example_code": """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payments
  template:
    metadata:
      labels:
        app: payments
    spec:
      containers:
        - name: payments
          image: registry.example.com/payments:v1
          ports:
            - containerPort: 8080
""",
    },
    "Kubernetes Workloads Services and Ingress": {
        "example_language": "yaml",
        "example_code": """\
apiVersion: v1
kind: Service
metadata:
  name: payments
spec:
  selector:
    app: payments
  ports:
    - port: 80
      targetPort: 8080
""",
    },
    "Infrastructure as Code": {
        "example_language": "hcl",
        "example_code": """\
resource "aws_s3_bucket" "artifacts" {
  bucket = "gudu-backend-artifacts"
}

resource "aws_iam_role" "deploy" {
  name = "backend-deploy-role"
}
""",
    },
    "CI CD Pipelines and Deployment Strategies": {
        "example_language": "yaml",
        "example_code": """\
steps:
  - run: go test ./...
  - run: docker build -t registry.example.com/payments:${GIT_SHA} .
  - run: kubectl set image deployment/payments payments=registry.example.com/payments:${GIT_SHA}
  - run: kubectl rollout status deployment/payments
""",
    },
    "Logging Metrics and Distributed Tracing": {
        "example_language": "go",
        "example_code": """\
ctx, span := tracer.Start(ctx, "create_order")
defer span.End()

logger.Info("creating order", "customer_id", order.CustomerID)
orderCreateLatency.WithLabelValues("success").Observe(duration.Seconds())
""",
    },
    "Event Sourcing CQRS and Auditability": {
        "diagram": """\
flowchart LR
    A["Command"] --> B["Aggregate"]
    B --> C["Event store"]
    C --> D["Projection worker"]
    D --> E["Read model"]
    E --> F["Query API"]
""",
    },
    "System Design Methodology and Communication": {
        "diagram": """\
flowchart LR
    A["Requirements"] --> B["Workload assumptions"]
    B --> C["High-level design"]
    C --> D["Bottlenecks and failure analysis"]
    D --> E["Capacity and cost model"]
    E --> F["Trade-off summary"]
""",
    },
}


KEYWORD_TOOL_OVERRIDES = {
    "dns": ["dig", "drill", "resolver logs"],
    "tcp": ["ss", "tcpdump", "wireshark"],
    "tls": ["openssl s_client", "certificate transparency logs", "curl -v"],
    "http": ["curl", "httpie", "wrk"],
    "sql": ["psql", "EXPLAIN ANALYZE", "query planner output"],
    "redis": ["redis-cli", "latency doctor", "memory usage"],
    "kubernetes": ["kubectl", "k9s", "kubectl describe"],
    "docker": ["docker build", "docker history", "docker scout"],
    "observability": ["OpenTelemetry", "Prometheus", "Grafana"],
    "incident": ["runbooks", "incident timelines", "alert dashboards"],
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = normalized.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def dedent(text: str) -> str:
    normalized = textwrap.dedent(text).strip()
    lines: list[str] = []
    in_code_block = False
    for raw_line in normalized.splitlines():
        line = raw_line
        if not in_code_block:
            while line.startswith("        "):
                line = line[8:]
        if line.startswith("```"):
            lines.append(line)
            in_code_block = not in_code_block
            continue
        lines.append(line)
    return "\n".join(lines)


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def build_topics() -> list[Topic]:
    topics: list[Topic] = []
    seen_titles: list[str] = []
    number = 1
    for phase_number, phase in enumerate(PHASES, start=1):
        titles = [title for title, _family in phase["topics"]]
        for topic_index, (title, family) in enumerate(phase["topics"]):
            prerequisites: list[str] = []
            if topic_index == 0:
                prerequisites.extend(phase["foundations"])
            else:
                prerequisites.append(titles[topic_index - 1])
                if topic_index >= 2 and titles[topic_index - 2] not in prerequisites:
                    prerequisites.append(titles[topic_index - 2])
                if topic_index >= 4 and phase["foundations"]:
                    prerequisites.append(phase["foundations"][0])
            prerequisites = [item for item in prerequisites if item in seen_titles]
            difficulty = min(10, max(1, phase_number + (topic_index // 3)))
            study_hours = 2 + max(1, difficulty // 2)
            practice_hours = study_hours + 2 + (difficulty // 2)
            topics.append(
                Topic(
                    number=number,
                    title=title,
                    filename=f"{number}-{slugify(title)}.md",
                    phase_number=phase_number,
                    phase_name=phase["name"],
                    phase_goal=phase["goal"],
                    phase_theme=phase["theme"],
                    family=family,
                    prerequisites=tuple(prerequisites),
                    study_hours=study_hours,
                    practice_hours=practice_hours,
                    difficulty=difficulty,
                )
            )
            seen_titles.append(title)
            number += 1
    return topics


def topic_link(title: str, topics_by_title: dict[str, Topic], prefix: str = "") -> str:
    topic = topics_by_title[title]
    return f"[{topic.number}. {topic.title}]({prefix}{topic.filename})"


def link_list(titles: tuple[str, ...] | list[str], topics_by_title: dict[str, Topic], prefix: str = "") -> str:
    if not titles:
        return "None. This chapter can be read from the beginning of the curriculum."
    return ", ".join(topic_link(title, topics_by_title, prefix=prefix) for title in titles)


def next_topic(topic: Topic, topics: list[Topic]) -> Topic | None:
    if topic.number >= len(topics):
        return None
    return topics[topic.number]


def previous_topic(topic: Topic, topics: list[Topic]) -> Topic | None:
    if topic.number == 1:
        return None
    return topics[topic.number - 2]


def matched_terms(title: str) -> list[tuple[str, str]]:
    lower = title.lower()
    terms: list[tuple[str, str]] = []
    for phrase in sorted(KEYWORD_TERMS.keys(), key=len, reverse=True):
        if phrase in lower:
            for pair in KEYWORD_TERMS[phrase]:
                if pair not in terms:
                    terms.append(pair)
    return terms


def topic_subject(topic: Topic) -> str:
    lower = topic.title.lower()
    exact = {
        "how computers represent information": "how numbers, text, booleans, addresses, and instructions become bits and bytes",
        "computer architecture for backend engineers": "how CPUs, caches, memory, and buses cooperate to execute backend code",
        "operating systems fundamentals": "how the kernel turns raw hardware into processes, files, memory, and networking services",
        "processes threads and scheduling": "how execution is isolated, shared, and given CPU time",
        "memory virtual memory and storage hierarchies": "how caches, RAM, pages, disks, and address translation shape performance and correctness",
        "filesystems and persistent storage": "how operating systems turn blocks on disk into durable files, directories, metadata, and recovery behavior",
        "command line linux and unix thinking": "using shell tools and text streams to inspect, compose, and control backend systems",
        "networking fundamentals": "how networked machines exchange packets across layered protocols",
        "how the internet works": "how a request travels through naming, routing, transport, encryption, and application layers",
        "dns and name resolution": "mapping human-readable names to IP addresses through a distributed cached lookup system",
        "ip routing and packet delivery": "moving packets across networks based on addressing and forwarding decisions",
        "tcp udp and transport trade-offs": "choosing between reliable ordered streams and lightweight datagram delivery",
        "tls certificates and secure transport": "authenticating peers and encrypting bytes while they move across untrusted networks",
        "sockets ports and connection lifecycles": "how applications open endpoints, accept connections, and exchange network data",
        "time clocks and failure in computer systems": "why local clocks drift, timestamps lie, and failures distort seemingly simple ordering assumptions",
        "programming fundamentals and state": "modeling input, state transitions, and output as explicit program behavior",
        "variables types and data representation": "storing values in memory with clear meaning, constraints, and runtime representation",
        "control flow and error handling": "making programs choose paths, recover, and fail in controlled ways",
        "functions modules and abstractions": "organizing logic into reusable boundaries with stable interfaces",
        "data structures in backend systems": "choosing in-memory shapes that make reads, writes, and traversal efficient",
        "algorithms and complexity for service engineers": "reasoning about the time and space cost of backend work",
        "recursion iteration and traversal": "walking state or structures step by step, whether through loops or self-reference",
        "concurrency parallelism and synchronization": "coordinating multiple units of work without races, deadlocks, or wasted parallelism",
        "testing fundamentals for backend code": "checking whether backend behavior is correct, repeatable, and safe to change",
        "debugging and profiling backend programs": "finding wrong behavior and locating where runtime time or memory is being spent",
        "version control and collaborative workflows": "tracking code history so teams can change systems safely together",
        "object oriented design and composition": "structuring software around collaborating objects and stable responsibilities",
        "functional programming and immutability": "preferring explicit data transformation and minimizing hidden mutation",
        "clean code refactoring and maintainability": "shaping code so future changes cost less than they otherwise would",
        "compilers interpreters and runtime environments": "how source code becomes executable behavior",
        "what a server really is": "the long-running process that listens for requests and coordinates backend work",
        "the request response lifecycle": "the end-to-end path from incoming bytes to validated business logic and serialized output",
        "http semantics headers and methods": "the meaning of web requests and responses, including verbs, metadata, caching, and status codes",
        "rest resource modeling and trade-offs": "structuring APIs around resources, representations, and stateless interactions",
        "api design contracts and evolution": "shaping backend interfaces so callers can depend on them as the system grows",
        "data serialization and message formats": "turning in-memory structures into wire formats such as JSON, Protobuf, or Avro",
        "input validation and boundary defense": "rejecting malformed, incomplete, or malicious input before it pollutes internal state",
        "authentication fundamentals": "verifying who a caller is before trusting their identity claims",
        "authorization and access control": "deciding what an authenticated principal may do to a resource",
        "sessions cookies and tokens": "maintaining identity and continuity across multiple requests",
        "backend application architecture": "organizing handlers, services, repositories, and cross-cutting concerns into a maintainable system",
        "routing middleware and dependency injection": "directing requests to code paths while composing shared behavior and dependencies cleanly",
        "background jobs and asynchronous workflows": "moving non-interactive work out of the request path without losing reliability",
        "file uploads media pipelines and object storage": "receiving large binary data, processing it, and storing it durably outside the local server",
        "configuration secrets and environment management": "supplying runtime behavior and credentials without hard-coding them into the application",
        "relational databases and table design": "modeling structured business data with relations, keys, and constraints",
        "sql queries filtering and aggregation": "asking relational systems for exact subsets and summaries of data",
        "joins normalization and schema modeling": "representing relationships without unnecessary duplication while preserving useful query paths",
        "indexes b trees and query performance": "using auxiliary data structures, especially B-trees, to trade write cost and storage for faster reads",
        "transactions acid and consistency guarantees": "grouping related data changes into reliable all-or-nothing units",
        "isolation levels locks and mvcc": "allowing concurrent transactions while controlling which anomalies are acceptable",
        "query planning storage engines and database internals": "how databases choose access paths and move data between memory, indexes, and durable pages",
        "caching fundamentals and cache invalidation": "serving repeated reads cheaply while managing staleness risk",
        "redis and in-memory data systems": "using memory-first stores for very low-latency data access and coordination",
        "nosql foundations and trade-offs": "choosing non-relational models when workload, scale, or flexibility makes strict relational structure less attractive",
        "document databases and schema flexibility": "storing self-contained records whose shape can evolve more freely than rows in fixed tables",
        "key value column family and time series stores": "specialized storage models optimized for distribution, sparsity, or append-heavy measurement data",
        "search indexes and full text retrieval": "turning text into searchable structures that support relevance ranking",
        "data pipelines etl and warehousing basics": "moving and reshaping data for analytics, reporting, and downstream processing",
        "backups restores and data lifecycle management": "ensuring data can survive mistakes, corruption, and changing retention needs",
        "scaling up scaling out and bottlenecks": "finding which resource limits growth and deciding whether to add bigger machines or more machines",
        "stateless services and shared state": "separating ephemeral request handling from the durable or shared data a fleet depends on",
        "load balancing reverse proxies and traffic steering": "distributing traffic across multiple service instances safely",
        "replication and read write topologies": "copying data or service state across nodes while choosing where reads and writes happen",
        "partitioning sharding and rebalancing": "splitting data or workload across multiple nodes without losing control of hotspots",
        "consistency models and the cap lens": "choosing what readers and writers may observe during replication and failure",
        "consensus leader election and coordination": "making multiple nodes agree on order or ownership under partial failure",
        "messaging queues and publish subscribe": "decoupling producers and consumers through brokers, queues, and asynchronous delivery",
        "event driven architecture and stream processing": "building systems around immutable events and continuously derived views",
        "distributed transactions sagas and compensation": "coordinating multi-step workflows across services without a single global lock",
        "idempotency retries and exactly once myths": "surviving duplicate attempts and unreliable delivery without doing the same work twice",
        "service discovery api gateways and service meshes": "helping services find each other and applying policy at communication boundaries",
        "fault tolerance backpressure and resilience patterns": "keeping systems alive when dependencies slow down, fail, or overload each other",
        "distributed caching coordination and invalidation": "sharing cached state across many nodes without letting staleness grow unbounded",
        "time ordering and clocks in distributed systems": "reasoning about causality and order when no global clock can be trusted",
        "building and packaging backend software": "turning source code into reproducible deployable artifacts",
        "linux service management and process supervision": "starting, stopping, restarting, and supervising long-running backend processes",
        "containers images and runtime isolation": "packaging processes with dependencies while constraining what they can see and use",
        "dockerfiles registries and supply chain security": "building container images, distributing them, and proving what is inside them",
        "container networking storage and stateful workloads": "making isolated workloads communicate and persist data safely",
        "kubernetes core concepts": "the declarative orchestration model that keeps containers running at the desired count and configuration",
        "kubernetes workloads services and ingress": "exposing workloads, networking them together, and routing external traffic into the cluster",
        "cloud fundamentals for backend engineers": "using rented infrastructure, managed services, and failure domains deliberately",
        "infrastructure as code": "describing infrastructure declaratively so it can be versioned, reviewed, and reproduced",
        "ci cd pipelines and deployment strategies": "moving code to production through automated build, test, promotion, and rollout steps",
        "observability fundamentals": "collecting enough evidence from production to explain system behavior",
        "logging metrics and distributed tracing": "capturing events, measurements, and causal request paths for debugging and operations",
        "monitoring alerting and on call practices": "detecting user-impacting problems and responding to them quickly and sustainably",
        "reliability engineering slis slos and error budgets": "turning user expectations into measurable reliability targets and decision rules",
        "incident response postmortems and disaster recovery": "restoring service under pressure and learning enough to reduce repeat failures",
        "architecture patterns for backend systems": "recurring structural approaches for organizing services, dependencies, and responsibilities",
        "monoliths modular monoliths and microservices": "choosing the right unit of deployment and ownership for a system and team",
        "domain driven design and bounded contexts": "aligning software structure with the language and boundaries of the business domain",
        "hexagonal architecture and dependency boundaries": "placing domain logic at the center and pushing technology details to the edges",
        "event sourcing cqrs and auditability": "modeling state as an append-only history of domain events with separate write and read models",
        "api gateways bffs and aggregation layers": "shaping network-facing entry points that adapt backend complexity for clients",
        "multi tenancy data isolation and saas architecture": "serving many customers from one platform without letting their data or workloads leak into each other",
        "performance engineering and capacity planning": "predicting and improving how a system behaves under real load",
        "cost engineering and finops for backend teams": "making architecture choices with cloud spend and economic efficiency in mind",
        "privacy compliance and data governance": "handling user data according to legal, ethical, and organizational rules",
        "platform engineering and developer experience": "building internal systems that make product teams faster and safer",
        "migration strategies and legacy modernization": "changing critical systems without breaking the business during the transition",
        "large scale storage and compute trade-offs": "choosing how much state, compute, locality, and specialization a workload really needs",
        "system design methodology and communication": "turning ambiguous product requirements into clear, reviewable technical designs",
        "technical leadership architecture reviews and long term ownership": "guiding major technical decisions and staying accountable for their long-term consequences",
    }
    if lower in exact:
        return exact[lower]
    return FAMILY_PROFILES[topic.family]["domain"]


def tool_list(topic: Topic) -> list[str]:
    tools = list(FAMILY_PROFILES[topic.family]["tools"])
    lower = topic.title.lower()
    for phrase, extra_tools in KEYWORD_TOOL_OVERRIDES.items():
        if phrase in lower:
            for tool in extra_tools:
                if tool not in tools:
                    tools.append(tool)
    return tools[:8]


def term_bullets(topic: Topic) -> list[str]:
    terms = matched_terms(topic.title)[:4]
    defaults = FAMILY_TERMS[topic.family]
    for pair in defaults:
        if pair not in terms:
            terms.append(pair)
    return [f"**{term}**: {definition}" for term, definition in terms[:6]]


def mental_model(topic: Topic) -> str:
    profile = FAMILY_PROFILES[topic.family]
    lower = topic.title.lower()
    if topic.family == "computing":
        return f"Treat {topic.title.lower()} as a layered machine model: hardware makes operations possible, the kernel coordinates access, and your process consumes those services with finite resources."
    if topic.family == "networking":
        return f"Treat {topic.title.lower()} as a postal system for bytes: naming finds the destination, routing chooses the path, transport manages delivery trade-offs, and application protocols interpret meaning."
    if topic.family == "programming":
        return f"Treat {topic.title.lower()} as controlled state transformation. Good code makes the allowed transitions obvious and the forbidden ones hard to express."
    if topic.family == "backend":
        return f"Treat {topic.title.lower()} as a production pipeline: a request arrives, boundaries validate it, internal rules execute, side effects happen carefully, and the system explains the result with a stable contract."
    if topic.family == "security":
        return f"Treat {topic.title.lower()} as border control for software. Every boundary asks who the caller is, what they want, what they are allowed to do, and how much harm is possible if you are wrong."
    if topic.family == "data":
        return f"Treat {topic.title.lower()} as durable memory for the business. The design decides which questions are cheap, which invariants are enforced, and which failures become recoverable."
    if topic.family == "distributed":
        return f"Treat {topic.title.lower()} as coordination among independent machines that can be slow, partitioned, duplicated, or wrong about time."
    if topic.family == "operations":
        return f"Treat {topic.title.lower()} as the path from source code to dependable service. The core question is not whether it runs once, but whether it can be shipped, observed, rolled back, and recovered repeatedly."
    return f"Treat {topic.title.lower()} as a design boundary. The main job is to decide which complexity belongs inside the boundary and which complexity must stay visible so teams can reason about it."


def history_note(topic: Topic) -> str:
    profile = FAMILY_PROFILES[topic.family]
    lower = topic.title.lower()
    specific = []
    if "dns" in lower:
        specific.append("DNS exists because humans name services better than they remember numeric addresses, but distributed caches were needed to make global lookup scale.")
    if "tcp" in lower or "udp" in lower:
        specific.append("The Internet's transport layer reflects the tension between reliability and speed: TCP added ordering and retransmission, while UDP left those concerns to the application.")
    if "rest" in lower:
        specific.append("REST emerged from web architecture thinking that prioritized stateless communication, cacheability, and uniform interfaces over custom RPC protocols.")
    if "transaction" in lower or "isolation" in lower:
        specific.append("Database transaction theory grew because data corruption caused by concurrent writes was far more expensive than the bookkeeping needed to prevent it.")
    if "kubernetes" in lower:
        specific.append("Kubernetes reflects the shift from hand-managed servers to declarative reconciliation loops that can manage huge fleets more consistently than humans can.")
    if "event sourcing" in lower or "cqrs" in lower:
        specific.append("Event sourcing and CQRS grew from domains where auditability, replay, and multiple read shapes mattered more than keeping only the latest state snapshot.")
    return " ".join([profile["history"], *specific]).strip()


def why_exists(topic: Topic) -> str:
    lower = topic.title.lower()
    subject = topic_subject(topic)
    if "cache" in lower:
        return "It exists because reading the original source of truth for every request is often too slow or too expensive."
    if "transaction" in lower:
        return "It exists because applications need a way to group related state changes so partial success does not corrupt the business."
    if "authentication" in lower or "authorization" in lower:
        return "It exists because systems need a precise way to distinguish identity from permission and to make those checks repeatable."
    if "load balancing" in lower:
        return "It exists because no single machine should be the only path to serving all traffic once availability and scale start to matter."
    if "observability" in lower:
        return "It exists because operating production systems without evidence turns debugging into guessing."
    return f"It exists because backend systems need a repeatable, understandable way to reason about {subject} without relying on folklore or fragile one-off code."


def problems_solved(topic: Topic) -> list[str]:
    lower = topic.title.lower()
    problems = [
        f"Turns {topic.title.lower()} from a vague concept into something engineers can measure, debug, and review.",
        "Creates shared language across implementation, operations, and system design.",
        "Reduces accidental complexity by making boundaries, state, and failure modes explicit.",
    ]
    if "http" in lower or "api" in lower or "server" in lower:
        problems.append("Helps teams design interfaces that clients can depend on without constant coordinated releases.")
    if "data" in lower or topic.family == "data":
        problems.append("Protects correctness and latency when data volume, concurrency, and retention increase.")
    if topic.family == "distributed":
        problems.append("Makes partial failure and duplicate work survivable instead of catastrophic.")
    return problems[:5]


def first_principles_steps(topic: Topic) -> list[str]:
    lower = topic.title.lower()
    if topic.family == "computing":
        return [
            "Input or configuration becomes bytes in memory or on disk.",
            "The CPU executes instructions that manipulate registers, caches, and memory addresses.",
            "Whenever privileged work is needed, the process crosses into the kernel through a system call.",
            "The kernel schedules access to CPU time, memory pages, files, and devices.",
            "Observed behavior emerges from the interaction between your code, the runtime, the kernel, and the hardware.",
        ]
    if topic.family == "networking":
        return [
            "Application data is encoded into bytes and given to the operating system through a socket API.",
            "The kernel wraps the bytes in transport and network headers, manages buffers, and hands packets to a network interface.",
            "Intermediate devices route or filter the traffic according to protocol rules.",
            "The receiving kernel reassembles, decrypts, and buffers the data for the receiving process.",
            "The application finally interprets the payload according to the higher-level protocol or business rule.",
        ]
    if topic.family == "programming":
        return [
            "Source code is parsed into a form the runtime can execute.",
            "Data structures are allocated and mutated according to control flow.",
            "Function calls create stack activity and possibly heap allocations.",
            "Concurrency primitives or runtimes coordinate independent work.",
            "The result is checked through tests, logs, profilers, or returned values.",
        ]
    if topic.family == "backend":
        return [
            "A client sends protocol bytes to a listening process.",
            "The server accepts the connection, parses the request, and maps it to a route or handler.",
            "Validation and authorization determine whether the request may proceed.",
            "Business logic performs reads, writes, or asynchronous side effects.",
            "The system serializes a response or enqueues follow-up work while emitting telemetry about what happened.",
        ]
    if topic.family == "security":
        return [
            "An untrusted caller presents data, credentials, or claims.",
            "The system validates syntax, verifies proof, and establishes identity or channel trust.",
            "Policy determines whether the requested action is allowed.",
            "Sensitive state changes or secret accesses are logged and constrained.",
            "Failures must deny access safely without leaking unnecessary information to an attacker.",
        ]
    if topic.family == "data":
        return [
            "An application expresses a read or write intent.",
            "The data system parses the request and chooses a plan based on indexes, statistics, and transaction context.",
            "Memory structures and storage pages are read or updated under concurrency-control rules.",
            "Durability mechanisms record enough information to recover after crashes.",
            "Future readers observe the result according to the chosen consistency guarantees.",
        ]
    if topic.family == "distributed":
        return [
            "Independent nodes exchange messages over an unreliable network.",
            "Each node makes decisions with incomplete information about peers and time.",
            "Replication, partitioning, or queuing layers try to maintain progress despite slowness or failure.",
            "Coordination algorithms decide when an operation should count as accepted or complete.",
            "Correctness depends on reasoning about duplicates, retries, lag, ordering, and partial failure rather than only on local code paths.",
        ]
    if topic.family == "operations":
        return [
            "Source code is converted into a build artifact with recorded dependencies and configuration assumptions.",
            "The artifact is placed into a runtime environment with resource limits, networking, secrets, and identity.",
            "An orchestrator or service manager starts and supervises the process.",
            "Telemetry pipelines collect evidence about success, performance, and failure.",
            "Operators or automation compare actual behavior against desired behavior and intervene when they diverge.",
        ]
    return [
        "Requirements become architectural constraints and workload assumptions.",
        "Boundaries are chosen for code, data, and ownership.",
        "Interfaces are defined so independent teams or services can interact safely.",
        "Operational, cost, and migration consequences are considered before implementation choices solidify.",
        "The design is communicated so others can reason about trade-offs instead of copying a diagram blindly.",
    ]


def diagram_for(topic: Topic) -> str:
    exact = EXACT_OVERRIDES.get(topic.title)
    if exact and "diagram" in exact:
        return exact["diagram"].strip()

    if topic.family == "computing":
        return dedent(
            """\
            flowchart LR
                A["Application code"] --> B["Runtime and libraries"]
                B --> C["System calls"]
                C --> D["Kernel"]
                D --> E["CPU and memory"]
                D --> F["Filesystem and disk"]
                D --> G["Network devices"]
            """
        )
    if topic.family == "networking":
        return dedent(
            """\
            flowchart LR
                A["Client process"] --> B["Socket API"]
                B --> C["Kernel networking stack"]
                C --> D["Router or switch path"]
                D --> E["Remote kernel"]
                E --> F["Remote service"]
            """
        )
    if topic.family == "programming":
        return dedent(
            """\
            flowchart LR
                A["Source code"] --> B["Parser or compiler"]
                B --> C["Runtime execution"]
                C --> D["State transitions"]
                D --> E["Tests and telemetry"]
            """
        )
    if topic.family == "backend":
        return dedent(
            """\
            flowchart LR
                A["Client"] --> B["Listener"]
                B --> C["Middleware or boundary checks"]
                C --> D["Business logic"]
                D --> E["Database or queue"]
                D --> F["External service"]
                D --> G["Response serializer"]
                G --> A
            """
        )
    if topic.family == "security":
        return dedent(
            """\
            flowchart LR
                A["Caller"] --> B["Identity or transport proof"]
                B --> C["Verification"]
                C --> D["Policy decision"]
                D --> E["Allowed action"]
                D --> F["Denied action"]
            """
        )
    if topic.family == "data":
        return dedent(
            """\
            flowchart LR
                A["Application query"] --> B["Parser"]
                B --> C["Planner"]
                C --> D["Executor"]
                D --> E["Buffer pool and indexes"]
                E --> F["Storage engine"]
                F --> D
            """
        )
    if topic.family == "distributed":
        return dedent(
            """\
            flowchart LR
                A["Client"] --> B["Traffic entry point"]
                B --> C["Replica 1"]
                B --> D["Replica 2"]
                C --> E["Queue or log"]
                D --> E
                E --> F["Downstream state"]
            """
        )
    if topic.family == "operations":
        return dedent(
            """\
            flowchart LR
                A["Commit"] --> B["CI pipeline"]
                B --> C["Artifact or image"]
                C --> D["Deployment platform"]
                D --> E["Running service"]
                E --> F["Logs metrics traces"]
                F --> G["Alerting and operators"]
            """
        )
    return dedent(
        """\
        flowchart LR
            A["Requirements"] --> B["Boundaries"]
            B --> C["Implementation choices"]
            C --> D["Operational consequences"]
            D --> E["Feedback and redesign"]
        """
    )


def example_for(topic: Topic) -> tuple[str, str]:
    exact = EXACT_OVERRIDES.get(topic.title)
    if exact and "example_language" in exact and "example_code" in exact:
        return exact["example_language"], exact["example_code"].strip()

    if topic.family == "computing":
        return (
            "bash",
            dedent(
                """\
                PID=$(pgrep -f my-service | head -n 1)
                ps -o pid,ppid,stat,%cpu,%mem,command -p "$PID"
                vmstat 1 5
                lsof -p "$PID" | head -n 20
                """
            ),
        )
    if topic.family == "networking":
        return (
            "bash",
            dedent(
                """\
                curl -v https://api.example.com/health
                ss -tnp | grep 443
                tcpdump -n host api.example.com and port 443
                """
            ),
        )
    if topic.family == "programming":
        if "concurrency" in topic.title.lower():
            return (
                "go",
                dedent(
                    """\
                    results := make(chan int, 2)

                    go func() { results <- slowQueryA() }()
                    go func() { results <- slowQueryB() }()

                    total := <-results + <-results
                    fmt.Println(total)
                    """
                ),
            )
        return (
            "typescript",
            dedent(
                """\
                type Account = { id: string; balanceCents: number };

                function debit(account: Account, amountCents: number): Account {
                  if (amountCents <= 0) throw new Error("amount must be positive");
                  if (account.balanceCents < amountCents) throw new Error("insufficient funds");
                  return { ...account, balanceCents: account.balanceCents - amountCents };
                }
                """
            ),
        )
    if topic.family == "backend":
        return (
            "go",
            dedent(
                """\
                func (s *Server) createOrder(w http.ResponseWriter, r *http.Request) {
                    var input CreateOrderRequest
                    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
                        http.Error(w, "invalid request", http.StatusBadRequest)
                        return
                    }

                    order, err := s.service.CreateOrder(r.Context(), input)
                    if err != nil {
                        http.Error(w, err.Error(), http.StatusUnprocessableEntity)
                        return
                    }

                    w.Header().Set("Content-Type", "application/json")
                    json.NewEncoder(w).Encode(order)
                }
                """
            ),
        )
    if topic.family == "security":
        return (
            "go",
            dedent(
                """\
                func RequireRole(next http.Handler, role string) http.Handler {
                    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
                        claims := auth.ClaimsFromContext(r.Context())
                        if claims.Role != role {
                            http.Error(w, "forbidden", http.StatusForbidden)
                            return
                        }
                        next.ServeHTTP(w, r)
                    })
                }
                """
            ),
        )
    if topic.family == "data":
        return (
            "sql",
            dedent(
                """\
                EXPLAIN ANALYZE
                SELECT id, status, created_at
                FROM jobs
                WHERE status = 'pending'
                ORDER BY created_at ASC
                LIMIT 50;
                """
            ),
        )
    if topic.family == "distributed":
        return (
            "go",
            dedent(
                """\
                for attempt := 1; attempt <= 3; attempt++ {
                    err := publish(ctx, message)
                    if err == nil {
                        break
                    }
                    time.Sleep(time.Duration(attempt) * 100 * time.Millisecond)
                }
                """
            ),
        )
    if topic.family == "operations":
        return (
            "bash",
            dedent(
                """\
                docker build -t registry.example.com/payments:${GIT_SHA} .
                kubectl set image deployment/payments payments=registry.example.com/payments:${GIT_SHA}
                kubectl rollout status deployment/payments
                """
            ),
        )
    return (
        "markdown",
        dedent(
            """\
            Context: checkout service
            Constraint: p95 latency under 250ms at 5x traffic
            Decision: keep writes centralized, scale reads horizontally, make failures observable
            """
        ),
    )


def implementation_notes(topic: Topic) -> list[str]:
    profile = FAMILY_PROFILES[topic.family]
    notes = [
        f"Start with a tiny working example so you can observe {topic.title.lower()} directly before you hide it behind frameworks or abstractions.",
        f"Use tools such as {', '.join(tool_list(topic)[:4])} to verify your mental model against reality.",
        "Document assumptions about data shape, timing, permissions, and failure handling right next to the implementation.",
    ]
    if topic.family in {"backend", "security", "data", "distributed", "operations"}:
        notes.append("Instrument the code path early so the example can graduate into production learning rather than staying a toy.")
    return notes


def common_mistakes(topic: Topic) -> list[str]:
    lower = topic.title.lower()
    mistakes = [
        f"Treating {topic.title.lower()} as a vocabulary item instead of a behavior that must be traced end to end.",
        "Assuming the happy path is the common path in production.",
        "Copying a framework pattern without understanding the resource or failure model underneath it.",
        "Ignoring instrumentation until the system is already hard to debug.",
    ]
    if topic.family == "security":
        mistakes.append("Trusting client-supplied identity or authorization data without independent verification.")
    if topic.family == "data":
        mistakes.append("Optimizing schema or indexes for a guessed workload instead of the measured one.")
    if topic.family == "distributed":
        mistakes.append("Pretending retries are free and duplicates cannot happen.")
    if "cache" in lower:
        mistakes.append("Assuming a cache is only a performance optimization and not also a consistency hazard.")
    return mistakes[:5]


def best_practices(topic: Topic) -> list[str]:
    practices = [
        "Model the boundaries explicitly: where input enters, where trust begins, and where state becomes durable.",
        "Prefer clear invariants over clever shortcuts so teammates can reason about correctness quickly.",
        "Measure with production-like workloads before claiming a design is fast or scalable.",
        "Design the unhappy path intentionally: timeouts, cancellation, retries, and rollback matter as much as the happy path.",
        "Keep the implementation teachable; if you cannot explain it from first principles, it is probably too magical.",
    ]
    if topic.family == "operations":
        practices.append("Automate repeated operational steps so safety does not depend on heroics.")
    return practices[:5]


def advanced_points(topic: Topic) -> list[str]:
    lower = topic.title.lower()
    points = [
        "Study which assumptions stop holding once you add concurrency, distribution, or multi-tenant traffic.",
        "Examine the internal data structures or state machines the abstraction hides.",
        "Learn the dominant optimization levers and the failure modes each lever introduces.",
        "Compare the topic's default industry approach with at least one alternative and explain the trade-off clearly.",
    ]
    if "performance" in lower or topic.family in {"data", "distributed", "operations", "architecture"}:
        points.append("Pay special attention to tail behavior, saturation, and second-order effects rather than just average latency.")
    return points[:5]


def production_considerations(topic: Topic) -> list[str]:
    profile = FAMILY_PROFILES[topic.family]
    items = [
        f"Reliability: decide what a safe failure looks like when {topic.title.lower()} goes wrong.",
        f"Monitoring: track {profile['metrics']} so you can see whether the system matches your mental model.",
        "Security: confirm that boundaries are enforced even when input is malicious or infrastructure is misconfigured.",
        "Performance: reason about both average behavior and tail latency under realistic contention.",
        "Failure scenarios: rehearse what happens during partial outages, stale configuration, dependency slowness, or bad deploys.",
    ]
    return items


def interview_points(topic: Topic) -> list[str]:
    lower = topic.title.lower()
    points = [
        f"Interview question: explain {topic.title.lower()} from first principles to a teammate who knows only high-level frameworks.",
        "Senior expectation: move beyond definitions and talk about failure modes, metrics, and trade-offs.",
        "System design angle: explain where this concept sits in a larger request path or data flow.",
        "Trade-off to discuss: what becomes faster, safer, or simpler, and what becomes more expensive or complex?",
    ]
    if topic.family == "distributed":
        points.append("Expect follow-up questions about partial failure, duplicate work, or cross-region behavior.")
    return points[:5]


def exercise_sets(topic: Topic) -> dict[str, list[str]]:
    title = topic.title.lower()
    return {
        "Beginner Exercises": [
            f"Define {title} in your own words without using jargon from the chapter.",
            "Draw the main components and arrows on paper from memory, then compare with the chapter diagram.",
            "Run or rewrite the practical example and change one assumption to see what breaks first.",
        ],
        "Intermediate Exercises": [
            "Add logging or measurements to the example so you can observe internal state transitions.",
            "Create a failure case deliberately and explain which layer is responsible for detecting and handling it.",
            "Compare two possible designs for the same problem and write one paragraph on the trade-offs.",
        ],
        "Advanced Challenges": [
            "Scale the example to production-like traffic, concurrency, or data volume and document the new bottlenecks.",
            "Design a safer or more observable variant of the implementation and justify the added complexity.",
            "List the hidden assumptions in the chapter and explain how they would change in a multi-region or multi-tenant system.",
        ],
        "Real-World Projects": [
            f"Build a small project where {title} is central rather than incidental.",
            "Add monitoring, tests, and a written README that explains the architecture and failure model.",
            "Present the result as if you were handing it to another engineer for production ownership.",
        ],
    }


def summary_lines(topic: Topic, next_item: Topic | None) -> list[str]:
    lines = [
        f"You learned what {topic.title.lower()} is, why backend engineers care about it, and how it behaves below the abstraction layer.",
        "You saw the core vocabulary, internal flow, implementation patterns, failure modes, and production trade-offs.",
    ]
    if next_item:
        lines.append(
            f"The next useful layer is {next_item.title.lower()}, because it builds on the same model and extends it into a larger system concern."
        )
    return lines


def chapter_intro(topic: Topic, topics: list[Topic], topics_by_title: dict[str, Topic]) -> str:
    profile = FAMILY_PROFILES[topic.family]
    prev_item = previous_topic(topic, topics)
    next_item = next_topic(topic, topics)
    prereq_text = link_list(topic.prerequisites, topics_by_title)
    next_text = topic_link(next_item.title, topics_by_title) if next_item else "This is the final chapter in the curriculum."
    prev_text = topic_link(prev_item.title, topics_by_title) if prev_item else "No earlier chapter is required."
    subject = topic_subject(topic)
    return dedent(
        f"""\
        ### What This Topic Is

        {topic.title} is about {subject}. In a backend system, this topic matters because real services are not only business logic; they are also concrete programs and protocols moving through machines, networks, data stores, and operational constraints.

        ### Why Backend Engineers Need It

        {profile['why']} If you understand {topic.title.lower()} only at the framework level, you can build demos. If you understand it from first principles, you can debug outages, choose better trade-offs, and explain your design to other engineers.

        ### Where This Topic Appears in Real-World Systems

        You will see this topic in {profile['where']}. Even small products encounter it early, and large systems eventually make it impossible to ignore.

        ### How This Topic Connects to Previous and Future Topics

        This chapter sits in **Phase {topic.phase_number}: {topic.phase_name}**, whose goal is: {topic.phase_goal}

        It builds on: {prereq_text}

        It is directly reinforced by: {prev_text}

        It prepares you for: {next_text}
        """
    )


def fundamental_concepts(topic: Topic) -> str:
    return dedent(
        f"""\
        ### Core Definitions

        {bullets(term_bullets(topic))}

        ### Terminology

        Use the vocabulary in this chapter precisely. In backend engineering, confusion often starts when teams use the same word to mean protocol behavior, runtime behavior, and business behavior at the same time.

        ### Mental Models

        {mental_model(topic)}

        ### Historical Background

        {history_note(topic)}

        ### Why This Concept Exists

        {why_exists(topic)}

        ### Problems It Solves

        {bullets(problems_solved(topic))}
        """
    )


def first_principles_section(topic: Topic) -> str:
    profile = FAMILY_PROFILES[topic.family]
    steps = first_principles_steps(topic)
    return dedent(
        f"""\
        ### Lowest-Level View

        {profile['first_principles']} When you learn {topic.title.lower()} from first principles, you are learning where the bytes go, who owns the state, and what work the computer must actually perform.

        ### What Happens Internally

        {numbered(steps)}

        ### How the Computer Executes It

        The computer does not understand product features or framework conventions. It understands instructions, memory accesses, protocol bytes, queues, locks, storage pages, and system calls. Every higher-level behavior in this chapter eventually reduces to those lower-level operations plus scheduling and timing.

        ### How Different Layers Interact

        Good backend engineers track how the application layer depends on the runtime, how the runtime depends on the operating system, and how the operating system depends on hardware or network conditions. Bugs often hide in the mismatch between those layers.

        ### What Abstractions Hide from Developers

        {profile['abstractions']} That hidden detail is often exactly where performance regressions, security flaws, or production outages come from.
        """
    )


def architecture_section(topic: Topic) -> str:
    profile = FAMILY_PROFILES[topic.family]
    return dedent(
        f"""\
        ### Internal Components

        {bullets(profile['components'])}

        ### Data Flow and Communication Flow

        Think of {topic.title.lower()} as a flow of state through cooperating components. Each component owns part of the work, and each handoff introduces latency, failure risk, and usually some translation of data or intent.

        ### Important Algorithms and Design Decisions

        {bullets(profile['algorithms'])}

        ### Mermaid Diagram

        ```mermaid
        {diagram_for(topic)}
        ```
        """
    )


def real_world_section(topic: Topic) -> str:
    return dedent(
        f"""\
        ### Small Applications

        In a small application, {topic.title.lower()} often appears in its simplest form: one process, one database, a few endpoints, and limited traffic. This is the best place to learn the shape of the concept before scale adds noise.

        ### Medium Applications

        In a medium-sized system, the same topic becomes a coordination problem. Multiple services, background workers, caches, or environments mean the same decision now affects more people and more failure modes.

        ### Large-Scale Production Systems

        At large scale, {topic.title.lower()} becomes a business concern as well as a technical one. Tail latency, blast radius, recovery speed, cost, and organizational ownership all matter as much as raw correctness.

        ### Web Applications, APIs, Cloud Systems, and Distributed Systems

        - Web applications depend on this topic whenever user actions must become reliable backend work.
        - APIs depend on it to create stable contracts between independent clients and services.
        - Cloud systems depend on it because infrastructure, latency, and failure domains make hidden assumptions visible.
        - Distributed systems depend on it because coordination across boundaries is where easy local reasoning stops working.
        """
    )


def practical_implementation_section(topic: Topic) -> str:
    language, code = example_for(topic)
    return dedent(
        f"""\
        ### Hands-On Example

        ```{language}
        {code}
        ```

        ### Why This Example Matters

        The goal of the example is not to teach a specific framework. It is to give you a concrete artifact you can run, inspect, and extend while keeping the first-principles model visible.

        ### Common Tools

        {bullets([f"`{tool}`" for tool in tool_list(topic)])}

        ### Industry-Standard Approaches

        {bullets(implementation_notes(topic))}
        """
    )


def common_mistakes_section(topic: Topic) -> str:
    return dedent(
        f"""\
        ### Beginner Mistakes

        {bullets(common_mistakes(topic)[:2])}

        ### Incorrect Assumptions

        {bullets(common_mistakes(topic)[2:4])}

        ### Production Mistakes

        {bullets(common_mistakes(topic)[4:] or ["Skipping capacity, failure, or rollback planning until after the first real outage."])}

        ### Security Problems

        {bullets([
            "Forgetting that external input, configuration, and environment state can all be attacker-controlled or simply wrong.",
            "Assuming internal traffic is automatically trustworthy.",
        ])}

        ### Performance Problems

        {bullets([
            "Reasoning from averages only and ignoring tail latency or hotspot behavior.",
            "Adding layers of abstraction without checking what work they introduce underneath.",
        ])}
        """
    )


def best_practices_section(topic: Topic) -> str:
    return dedent(
        f"""\
        ### Industry Standards

        {bullets([
            "Prefer explicit contracts, clear failure behavior, and observable execution over hidden convenience.",
            "Use version control, tests, telemetry, and repeatable environments as part of the normal workflow.",
        ])}

        ### Recommended Approaches

        {bullets(best_practices(topic)[:3])}

        ### Engineering Principles

        {bullets(best_practices(topic)[3:])}

        ### Maintainability Considerations

        Keep the code and architecture legible enough that a new engineer can explain ownership, invariants, and failure paths after reading the relevant module once or twice.
        """
    )


def advanced_concepts_section(topic: Topic) -> str:
    return dedent(
        f"""\
        ### Expert-Level Concepts

        {bullets(advanced_points(topic)[:2])}

        ### Edge Cases

        {bullets([
            "Think about duplicate requests, partial writes, stale reads, retries, and unexpected restarts.",
            "Challenge assumptions about time, ordering, and ownership boundaries.",
        ])}

        ### Internals

        {bullets(advanced_points(topic)[2:3] or ["Inspect the hidden state machines, buffers, or data structures that drive the abstraction."])}

        ### Optimization Techniques

        {bullets([
            "Optimize only after you can identify the real bottleneck with evidence.",
            "Prefer structural wins such as better data shape, fewer round trips, or cleaner ownership before micro-optimizations.",
        ])}

        ### Scaling Considerations

        {bullets(advanced_points(topic)[3:])}
        """
    )


def production_section(topic: Topic) -> str:
    return dedent(
        f"""\
        ### How This Works in Production

        Production changes the meaning of success. It is no longer enough for the code to work once. It must work repeatedly across deploys, noisy neighbors, retries, traffic bursts, and operator mistakes.

        ### Reliability Concerns, Monitoring, Security, Performance, and Failure Scenarios

        {bullets(production_considerations(topic))}
        """
    )


def interview_section(topic: Topic) -> str:
    return dedent(
        f"""\
        ### Common Interview Questions

        {bullets([interview_points(topic)[0]])}

        ### Senior Engineer Expectations

        {bullets([interview_points(topic)[1]])}

        ### System Design Considerations

        {bullets([interview_points(topic)[2]])}

        ### Trade-offs Engineers Must Understand

        {bullets(interview_points(topic)[3:])}
        """
    )


def exercises_section(topic: Topic) -> str:
    sets = exercise_sets(topic)
    return dedent(
        f"""\
        ### Beginner Exercises

        {bullets(sets["Beginner Exercises"])}

        ### Intermediate Exercises

        {bullets(sets["Intermediate Exercises"])}

        ### Advanced Challenges

        {bullets(sets["Advanced Challenges"])}

        ### Real-World Projects

        {bullets(sets["Real-World Projects"])}
        """
    )


def summary_section(topic: Topic, next_item: Topic | None) -> str:
    return dedent(
        f"""\
        ### Key Concepts Learned

        {bullets(summary_lines(topic, next_item)[:2])}

        ### Important Takeaways

        - First principles matter because backend systems fail at the layer you do not understand.
        - Trade-offs matter because every simplification moves cost somewhere else: latency, complexity, flexibility, security, or reliability.
        - Production context matters because the same idea behaves differently under scale, concurrency, and failure.

        ### Connection to Future Topics

        {summary_lines(topic, next_item)[2] if len(summary_lines(topic, next_item)) > 2 else "This chapter closes the formal sequence, so the next step is to revisit earlier chapters with a deeper systems lens."}
        """
    )


def render_topic(topic: Topic, topics: list[Topic], topics_by_title: dict[str, Topic]) -> str:
    next_item = next_topic(topic, topics)
    return f"""# {topic.number}. {topic.title}

- Phase: Phase {topic.phase_number} - {topic.phase_name}
- Phase goal: {topic.phase_goal}
- Estimated study time: {topic.study_hours} hours
- Estimated hands-on practice time: {topic.practice_hours} hours
- Difficulty: {topic.difficulty}/10
- Prerequisites: {link_list(topic.prerequisites, topics_by_title)}
- File name: `{topic.filename}`

## 1. Chapter Introduction

{chapter_intro(topic, topics, topics_by_title)}

## 2. Fundamental Concepts

{fundamental_concepts(topic)}

## 3. First Principles Explanation

{first_principles_section(topic)}

## 4. Architecture and Internals

{architecture_section(topic)}

## 5. Real-World Examples

{real_world_section(topic)}

## 6. Practical Implementation

{practical_implementation_section(topic)}

## 7. Common Mistakes

{common_mistakes_section(topic)}

## 8. Best Practices

{best_practices_section(topic)}

## 9. Advanced Concepts

{advanced_concepts_section(topic)}

## 10. Production Considerations

{production_section(topic)}

## 11. Interview and System Design Perspective

{interview_section(topic)}

## 12. Exercises

{exercises_section(topic)}

## 13. Summary

{summary_section(topic, next_item)}
"""


def render_readme(topics: list[Topic], topics_by_title: dict[str, Topic]) -> str:
    total_study = sum(topic.study_hours for topic in topics)
    total_practice = sum(topic.practice_hours for topic in topics)
    phase_sections = []
    chapter_offset = 0
    for phase_number, phase in enumerate(PHASES, start=1):
        phase_topics = topics[chapter_offset: chapter_offset + len(phase["topics"])]
        chapter_offset += len(phase["topics"])
        links = ", ".join(f"[{topic.number}. {topic.title}]({topic.filename})" for topic in phase_topics)
        phase_sections.append(
            f"### Phase {phase_number}: {phase['name']}\n\nGoal: {phase['goal']}\n\n{phase['theme']}\n\n{links}"
        )

    milestones = [
        "Milestone 1: Explain what happens below backend frameworks and trace a request through the operating system and network.",
        "Milestone 2: Write maintainable code with tests, debugging discipline, and clear abstractions.",
        "Milestone 3: Build complete backend applications with validation, authentication, asynchronous work, and stable APIs.",
        "Milestone 4: Model, query, cache, and recover data with confidence.",
        "Milestone 5: Design replicated, partitioned, resilient distributed systems.",
        "Milestone 6: Package, deploy, observe, and recover backend systems in production.",
        "Milestone 7: Make expert architecture decisions and defend them with trade-offs, metrics, and long-term ownership thinking.",
    ]

    projects = [
        "Project 1: a tiny HTTP service whose request path you can trace with shell tools and logs.",
        "Project 2: a tested backend library that implements business rules with clean module boundaries.",
        "Project 3: a production-style CRUD or workflow API with authentication, validation, background jobs, and observability.",
        "Project 4: a data-heavy service that uses relational modeling, indexing, caching, backups, and search.",
        "Project 5: a distributed service that uses queues, retries, idempotency keys, and replicated data.",
        "Project 6: a containerized service deployed through CI CD with dashboards, alerts, and rollback procedures.",
        "Project 7: a capstone design for a system used by millions of users, complete with architecture notes, capacity model, and migration plan.",
    ]

    capstone = [
        "Choose a realistic product domain with user traffic, asynchronous work, data growth, and clear reliability expectations.",
        "Document the workload, request paths, invariants, threat model, and operational requirements before implementation.",
        "Build the core service with stable APIs, persistent storage, background processing, and instrumentation from day one.",
        "Introduce scale concerns deliberately: caching, queues, replication, sharding, or multi-region behavior where justified.",
        "Package and deploy the system with repeatable automation, observability, and rollback procedures.",
        "Present the final design as if handing it to a senior team that will operate it for years.",
    ]

    return f"""# Backend Engineering Curriculum

## Curriculum Overview

This repository contains a complete backend engineering textbook written in Markdown and organized as a library of standalone chapter files. It starts from first principles and builds toward expert backend engineering judgment across computer foundations, programming, application development, data systems, distributed systems, production engineering, and architecture.

The curriculum contains **{len(topics)} chapters**, each saved as its own Markdown file using the naming pattern `<number>-<topic-name-in-kebab-case>.md`. Every chapter includes the same 13 core sections so learners can build a repeatable study habit while still progressing from beginner to expert.

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

- Total study time: about {total_study} hours
- Total practice time: about {total_practice} hours
- Total guided curriculum time: about {total_study + total_practice} hours
- Recommended pacing: 8 to 12 hours per week, plus project work

## Learning Roadmap

{"\n\n".join(phase_sections)}

## Milestones

{bullets(milestones)}

## Recommended Projects

{bullets(projects)}

## Final Capstone Roadmap

{numbered(capstone)}

## How to Navigate the Files

- Start with [1. How Computers Represent Information](1-how-computers-represent-information.md) if you are new to backend engineering.
- Use the chapter numbers for the intended order; the difficulty increases gradually.
- Use the prerequisites listed in each file when you want to skip around.
- Treat the `backend-engineering/README.md` file as the map and the chapter files as the textbook itself.

## What Completion Should Feel Like

By the end of this curriculum, you should be able to trace requests from the network to the database, write maintainable backend code, model data intentionally, reason about distributed trade-offs, operate production systems safely, and explain architecture decisions in clear engineering language.
"""


def render_lesson_index(topics: list[Topic], topics_by_title: dict[str, Topic]) -> str:
    phase_sections = []
    chapter_offset = 0
    for phase_number, phase in enumerate(PHASES, start=1):
        phase_topics = topics[chapter_offset: chapter_offset + len(phase["topics"])]
        chapter_offset += len(phase["topics"])
        lines = "\n".join(
            f"- [{topic.number}. {topic.title}](../backend-engineering/{topic.filename})" for topic in phase_topics
        )
        phase_sections.append(
            dedent(
                f"""\
                ## Phase {phase_number}: {phase['name']}

                Goal: {phase['goal']}

                {phase['theme']}

                {lines}
                """
            )
        )

    return f"""# Backend Engineering Curriculum Index

This index points to the generated backend engineering textbook in [backend-engineering/README.md](../backend-engineering/README.md).

The curriculum is designed to take a complete beginner from first principles to expert backend engineering judgment. Every chapter is its own Markdown file, and every file includes the same 13 core sections:

1. Chapter Introduction
2. Fundamental Concepts
3. First Principles Explanation
4. Architecture and Internals
5. Real-World Examples
6. Practical Implementation
7. Common Mistakes
8. Best Practices
9. Advanced Concepts
10. Production Considerations
11. Interview and System Design Perspective
12. Exercises
13. Summary

The generated library currently contains **{len(topics)} chapters** using the naming convention `<number>-<topic-name-in-kebab-case>.md`.

## Study Order

{"\n\n".join(phase_sections)}

## Suggested Starting Point

- New learner: [1. How Computers Represent Information](../backend-engineering/1-how-computers-represent-information.md)
- Overview of the full book: [backend-engineering/README.md](../backend-engineering/README.md)
"""


def write_outputs() -> None:
    topics = build_topics()
    assert len(topics) == 105, f"Expected 105 topics, got {len(topics)}"
    topics_by_title = {topic.title: topic for topic in topics}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUTPUT_DIR.glob("[0-9]*-*.md"):
        stale.unlink()

    for topic in topics:
        (OUTPUT_DIR / topic.filename).write_text(
            render_topic(topic, topics, topics_by_title).strip() + "\n",
            encoding="utf-8",
        )

    (OUTPUT_DIR / "README.md").write_text(
        render_readme(topics, topics_by_title).strip() + "\n",
        encoding="utf-8",
    )
    LESSON_INDEX.write_text(
        render_lesson_index(topics, topics_by_title).strip() + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(topics)} backend chapters plus README in {OUTPUT_DIR}")


if __name__ == "__main__":
    write_outputs()
