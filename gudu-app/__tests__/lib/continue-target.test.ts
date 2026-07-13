import { selectContinueTarget } from "@/lib/continue-target";

describe("lib/continue-target", () => {
  const baseLessons = [
    {
      lessonId: "backend:1",
      courseId: "backend",
      courseSlug: "backend",
      lessonTitle: "Lesson 1",
      moduleTitle: "Phase 1",
      orderIndex: 1,
      status: "unlocked" as const,
      lastOpenedAt: null,
      scrollPercent: 0,
    },
    {
      lessonId: "backend:2",
      courseId: "backend",
      courseSlug: "backend",
      lessonTitle: "Lesson 2",
      moduleTitle: "Phase 1",
      orderIndex: 2,
      status: "locked" as const,
      lastOpenedAt: null,
      scrollPercent: 0,
    },
  ];

  it("prefers the most recently opened in-progress lesson", () => {
    const target = selectContinueTarget([
      {
        ...baseLessons[0],
        status: "in_progress",
        lastOpenedAt: 10,
      },
      {
        ...baseLessons[1],
        status: "in_progress",
        lastOpenedAt: 20,
      },
    ]);

    expect(target?.lessonId).toBe("backend:2");
    expect(target?.reason).toBe("resume");
  });

  it("falls back to the next unlocked lesson", () => {
    const target = selectContinueTarget(baseLessons);

    expect(target?.lessonId).toBe("backend:1");
    expect(target?.reason).toBe("next_unlocked");
  });

  it("falls back to the first completed lesson when nothing is unlocked", () => {
    const target = selectContinueTarget([
      {
        ...baseLessons[0],
        status: "completed",
      },
      {
        ...baseLessons[1],
        status: "completed",
      },
    ]);

    expect(target?.lessonId).toBe("backend:1");
    expect(target?.reason).toBe("course_start");
  });
});
