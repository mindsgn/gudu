# App Specification

## Purpose

Gudu is a mobile learning platform for backend and frontend engineering. Users take structured courses broken into bite-sized lessons with progress tracking.

## Platforms

- iOS (primary)
- Android

## Framework

Expo SDK 56 + React Native 0.85.3

## Core Features

1. **Course Catalog** — Browse available courses (backend, frontend)
2. **Lesson Reader** — Read markdown lessons with scroll progress tracking
3. **Progress Tracking** — Complete lessons and track course progress
4. **Completion Flow** — Celebrate lesson completion

## User Journeys

### First Launch
Splash animation > Home screen > Course list

### Learn
Home > Course list > Lesson > Read with scroll progress > Completion

## Business Rules

- All course content stored locally (SQLite)
- Lessons are markdown-rendered with scroll progress
- Completion triggers haptic feedback and navigation

## Target Users

- Backend developers learning through structured lessons
- Frontend developers learning through structured lessons
- Anyone who wants a clean, minimal learning experience
