from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
BACKEND_INDEX_PATH = ROOT / "lessons" / "backend.md"
FRONTEND_INDEX_PATH = ROOT / "lessons" / "frontend.md"
BACKEND_README_PATH = ROOT / "backend-engineering" / "README.md"
FRONTEND_README_PATH = ROOT / "frontend-engineering" / "README.md"
OUTPUT_PATH = ROOT / "gudu-app" / "constants" / "curriculum.ts"

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BACKEND_PHASE_PATTERN = re.compile(r"^##\s+(Phase\s+\d+:\s+.+)$")
FRONTEND_MODULE_PATTERN = re.compile(r"^###\s+(Module\s+\d+:\s+.+)$")


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "item"


def parse_duration_minutes(raw_value: str | None) -> int | None:
    if not raw_value:
        return None

    total_minutes = 0.0
    for amount, unit in re.findall(
        r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|minutes?|mins?)",
        raw_value.lower(),
    ):
        value = float(amount)
        if unit.startswith("hour") or unit.startswith("hr"):
            total_minutes += value * 60
        else:
            total_minutes += value

    if total_minutes <= 0:
        return None

    return int(total_minutes)


def split_csv_like(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []

    cleaned = re.sub(LINK_PATTERN, lambda match: match.group(1), raw_value)
    cleaned = cleaned.replace(" and ", ", ")
    cleaned = cleaned.replace("None.", "")
    cleaned = cleaned.replace("None", "")
    parts = [part.strip(" .") for part in cleaned.split(",")]
    return [part for part in parts if part]


def parse_lesson_metadata(markdown: str) -> dict[str, object]:
    metadata: dict[str, str] = {}

    for line in markdown.splitlines():
        if not line.startswith("- "):
            if metadata:
                break
            continue

        if ":" not in line:
            continue

        key, value = line[2:].split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    estimated_study_minutes = parse_duration_minutes(
        metadata.get("estimated study time")
    )
    estimated_practice_minutes = parse_duration_minutes(
        metadata.get("estimated hands-on practice time")
        or metadata.get("estimated practice time")
    )
    difficulty_label = metadata.get("difficulty") or metadata.get("difficulty rating")
    prerequisites = split_csv_like(metadata.get("prerequisites"))
    unlocked_concepts = split_csv_like(
        metadata.get("concepts unlocked after completing it")
    )

    return {
        "estimatedStudyMinutes": estimated_study_minutes,
        "estimatedPracticeMinutes": estimated_practice_minutes,
        "difficultyLabel": difficulty_label,
        "prerequisites": prerequisites,
        "unlockedConcepts": unlocked_concepts,
    }


def build_backend_modules() -> list[dict[str, object]]:
    lines = BACKEND_INDEX_PATH.read_text().splitlines()
    modules: list[dict[str, object]] = []
    current_module: dict[str, object] | None = None

    for line in lines:
        heading_match = BACKEND_PHASE_PATTERN.match(line)
        if heading_match:
            title = heading_match.group(1)
            current_module = {
                "title": title,
                "slug": slugify(title),
                "summary": None,
                "lessons": [],
            }
            modules.append(current_module)
            continue

        if current_module is None:
            continue

        if line.startswith("Goal: "):
            current_module["summary"] = line.replace("Goal: ", "", 1).strip()
            continue

        link_match = re.match(r"^- \[([^\]]+)\]\(([^)]+)\)$", line.strip())
        if not link_match:
            continue

        lesson_title, relative_path = link_match.groups()
        source_path = (BACKEND_INDEX_PATH.parent / relative_path).resolve()
        markdown = source_path.read_text()
        lesson_slug = source_path.stem
        lesson_metadata = parse_lesson_metadata(markdown)
        lessons = current_module["lessons"]
        assert isinstance(lessons, list)
        lessons.append(
            {
                "slug": lesson_slug,
                "title": lesson_title,
                "sourcePath": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                "markdown": markdown,
                **lesson_metadata,
            }
        )

    return modules


def extract_frontend_module_links(lines: list[str], start_index: int) -> tuple[str | None, list[tuple[str, str]], int]:
    summary: str | None = None
    collected_links: list[tuple[str, str]] = []
    index = start_index + 1

    while index < len(lines):
        line = lines[index]

        if line.startswith("### "):
            break

        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        if summary is None:
            summary = stripped
            index += 1
            continue

        links = LINK_PATTERN.findall(stripped)
        if links:
            collected_links.extend(links)

        index += 1

    return summary, collected_links, index


def build_frontend_modules() -> list[dict[str, object]]:
    lines = FRONTEND_README_PATH.read_text().splitlines()
    modules: list[dict[str, object]] = []
    index = 0

    while index < len(lines):
        heading_match = FRONTEND_MODULE_PATTERN.match(lines[index])
        if not heading_match:
            index += 1
            continue

        title = heading_match.group(1)
        summary, links, index = extract_frontend_module_links(lines, index)
        module = {
            "title": title,
            "slug": slugify(title),
            "summary": summary,
            "lessons": [],
        }

        lessons = module["lessons"]
        assert isinstance(lessons, list)

        for lesson_title, relative_path in links:
            source_path = (FRONTEND_README_PATH.parent / relative_path).resolve()
            markdown = source_path.read_text()
            lesson_slug = source_path.stem
            lesson_metadata = parse_lesson_metadata(markdown)
            lessons.append(
                {
                    "slug": lesson_slug,
                    "title": lesson_title,
                    "sourcePath": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                    "markdown": markdown,
                    **lesson_metadata,
                }
            )

        modules.append(module)

    return modules


def flatten_paths(course_modules: Iterable[dict[str, object]]) -> list[Path]:
    paths: list[Path] = [BACKEND_INDEX_PATH, FRONTEND_README_PATH, BACKEND_README_PATH, FRONTEND_README_PATH]
    for module in course_modules:
        lessons = module["lessons"]
        assert isinstance(lessons, list)
        for lesson in lessons:
            source_path = ROOT / str(lesson["sourcePath"])
            paths.append(source_path)
    return paths


def build_curriculum_seed() -> dict[str, object]:
    backend_modules = build_backend_modules()
    frontend_modules = build_frontend_modules()

    course_configs = [
        {
            "id": "backend",
            "slug": "backend",
            "title": "Backend Engineering",
            "description": "Trace systems from machine fundamentals to production-ready backend architecture.",
            "sourceIndexPath": "lessons/backend.md",
            "sortOrder": 1,
            "modules": backend_modules,
        },
        {
            "id": "frontend",
            "slug": "frontend",
            "title": "Frontend Engineering",
            "description": "Learn the browser stack from first principles through modern frontend architecture.",
            "sourceIndexPath": "lessons/frontend.md",
            "sortOrder": 2,
            "modules": frontend_modules,
        },
    ]

    seed_courses: list[dict[str, object]] = []
    hashed_paths = flatten_paths(backend_modules) + flatten_paths(frontend_modules)
    seen_paths: set[Path] = set()
    digest = hashlib.sha256()

    for path in hashed_paths:
        if path in seen_paths:
            continue
        seen_paths.add(path)
        digest.update(path.read_bytes())

    for course_config in course_configs:
        order_index = 1
        module_payloads: list[dict[str, object]] = []
        modules = course_config["modules"]
        assert isinstance(modules, list)

        for module_index, module in enumerate(modules, start=1):
            module_id = f"{course_config['id']}:{module['slug']}"
            lesson_payloads: list[dict[str, object]] = []
            lessons = module["lessons"]
            assert isinstance(lessons, list)

            for lesson in lessons:
                lesson_id = f"{course_config['id']}:{lesson['slug']}"
                lesson_payloads.append(
                    {
                        "id": lesson_id,
                        "courseId": course_config["id"],
                        "moduleId": module_id,
                        "slug": lesson["slug"],
                        "title": lesson["title"],
                        "sourcePath": lesson["sourcePath"],
                        "orderIndex": order_index,
                        "estimatedStudyMinutes": lesson["estimatedStudyMinutes"],
                        "estimatedPracticeMinutes": lesson["estimatedPracticeMinutes"],
                        "difficultyLabel": lesson["difficultyLabel"],
                        "prerequisites": lesson["prerequisites"],
                        "unlockedConcepts": lesson["unlockedConcepts"],
                        "markdown": lesson["markdown"],
                    }
                )
                order_index += 1

            module_payloads.append(
                {
                    "id": module_id,
                    "courseId": course_config["id"],
                    "slug": module["slug"],
                    "title": module["title"],
                    "summary": module["summary"],
                    "sortOrder": module_index,
                    "lessons": lesson_payloads,
                }
            )

        total_lessons = sum(len(module["lessons"]) for module in module_payloads)
        seed_courses.append(
            {
                "id": course_config["id"],
                "slug": course_config["slug"],
                "title": course_config["title"],
                "description": course_config["description"],
                "sourceIndexPath": course_config["sourceIndexPath"],
                "totalLessons": total_lessons,
                "totalModules": len(module_payloads),
                "sortOrder": course_config["sortOrder"],
                "modules": module_payloads,
            }
        )

    return {
        "version": digest.hexdigest()[:16],
        "generatedAt": "repo-build",
        "courses": seed_courses,
    }


def render_frontend_index(seed: dict[str, object]) -> str:
    courses = seed["courses"]
    assert isinstance(courses, list)
    frontend_course = next(
        course for course in courses if course["slug"] == "frontend"
    )
    modules = frontend_course["modules"]
    assert isinstance(modules, list)

    lines = [
        "# Frontend Engineering Curriculum Index",
        "",
        "This index points to the generated frontend engineering textbook in [frontend-engineering/README.md](../frontend-engineering/README.md).",
        "",
        "The curriculum is designed to take a learner from computer and network fundamentals through browser internals, modern frontend architecture, delivery, and long-term engineering judgment.",
        "",
        "The generated library currently contains **180 chapters** using the naming convention `<number>-<topic-name-in-kebab-case>.md`.",
        "",
        "## Study Order",
        "",
    ]

    for module in modules:
        lines.append(f"## {module['title']}")
        lines.append("")
        summary = module["summary"]
        if summary:
            lines.append(str(summary))
            lines.append("")
        lessons = module["lessons"]
        assert isinstance(lessons, list)
        for lesson in lessons:
            source_path = Path(str(lesson["sourcePath"]))
            relative_path = "../" + source_path.as_posix()
            lines.append(f"- [{lesson['title']}]({relative_path})")
        lines.append("")

    lines.extend(
        [
            "## Suggested Starting Point",
            "",
            "- New learner: [001 Computer Science for Frontend Engineers](../frontend-engineering/001-computer-science-for-frontend-engineers.md)",
            "- Overview of the full book: [frontend-engineering/README.md](../frontend-engineering/README.md)",
            "",
        ]
    )

    return "\n".join(lines)


def write_typescript_seed(seed: dict[str, object]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    seed_json = json.dumps(seed, indent=2, ensure_ascii=False)
    content = "\n".join(
        [
            'import type { CurriculumSeed } from "@/@types";',
            "",
            f"export const curriculumSeed: CurriculumSeed = {seed_json};",
            "",
            "export const curriculumVersion = curriculumSeed.version;",
        ]
    )
    OUTPUT_PATH.write_text(content)


def main() -> None:
    seed = build_curriculum_seed()
    write_typescript_seed(seed)
    FRONTEND_INDEX_PATH.write_text(render_frontend_index(seed))


if __name__ == "__main__":
    main()
