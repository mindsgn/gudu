import { getLocalDateKey, getUpdatedStreak } from "@/lib/streaks";

describe("lib/streaks", () => {
  it("formats a local date key", () => {
    expect(getLocalDateKey(new Date(2026, 6, 13))).toBe("2026-07-13");
  });

  it("starts a new streak when there is no recent activity", () => {
    expect(
      getUpdatedStreak(
        {
          currentStreak: 0,
          longestStreak: 0,
          lastActiveOn: null,
        },
        "2026-07-13",
        false,
      ),
    ).toEqual({
      currentStreak: 1,
      longestStreak: 1,
      lastActiveOn: "2026-07-13",
    });
  });

  it("extends the streak for consecutive days", () => {
    expect(
      getUpdatedStreak(
        {
          currentStreak: 4,
          longestStreak: 4,
          lastActiveOn: "2026-07-12",
        },
        "2026-07-13",
        false,
      ),
    ).toEqual({
      currentStreak: 5,
      longestStreak: 5,
      lastActiveOn: "2026-07-13",
    });
  });

  it("keeps the streak steady when the learner already studied today", () => {
    expect(
      getUpdatedStreak(
        {
          currentStreak: 5,
          longestStreak: 7,
          lastActiveOn: "2026-07-13",
        },
        "2026-07-13",
        true,
      ),
    ).toEqual({
      currentStreak: 5,
      longestStreak: 7,
      lastActiveOn: "2026-07-13",
    });
  });
});
