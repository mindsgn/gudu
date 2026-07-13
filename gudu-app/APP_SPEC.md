# App Specification

## Purpose

Gudu is a local-first mobile learning app for backend and frontend engineering. Learners move through structured curricula, read markdown lessons, and build momentum with points, streaks, progress unlocks, and recent activity.

## Platforms

- iOS (primary)
- Android

## Framework

Expo SDK 56 + React Native 0.85.3

## Core Features

1. **Curriculum Dashboard** — Home screen with total score, streaks, activity heatmap, continue CTA, and both engineering tracks
2. **Course Progression** — Backend and frontend courses grouped into ordered phases/modules with locked, unlocked, in-progress, and completed lessons
3. **Markdown Lesson Reader** — Local markdown rendering with scroll progress and reading-position restore
4. **Completion Flow** — First-time completion awards points, updates streak/activity, unlocks the next lesson, and routes to a summary screen

## User Journeys

### First Launch
Splash bootstraps SQLite + curriculum seed > Home dashboard > Course selection

### Continue Learning
Home continue button > Most recent in-progress lesson or next unlocked lesson > Completion summary

### Course Navigation
Home > Course screen > Ordered lesson list > Lesson reader > Completion > Home or next lesson

## Business Rules

- All curriculum content is bundled locally and seeded into SQLite
- Two courses ship in V0.0.1: Backend Engineering and Frontend Engineering
- Lessons unlock strictly in order inside each course
- The first lesson in each course is unlocked by default
- A lesson awards points only once on first completion
- Streaks advance when at least one lesson is completed on a calendar day
- The home score is lifetime total points

## Target Users

- Backend developers who want a structured first-principles path
- Frontend developers who want a browser-to-architecture learning journey
- Self-directed learners who want an offline-friendly study experience
