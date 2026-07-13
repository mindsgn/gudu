import {
  getLessonCompletionPoints,
  LESSON_COMPLETION_POINTS,
} from "@/lib/points";

describe("lib/points", () => {
  it("awards fixed points for a first-time completion", () => {
    expect(getLessonCompletionPoints(false)).toBe(LESSON_COMPLETION_POINTS);
  });

  it("does not award points twice", () => {
    expect(getLessonCompletionPoints(true)).toBe(0);
  });
});
