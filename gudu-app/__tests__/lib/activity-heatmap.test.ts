import { buildActivityHeatmap, getHeatmapIntensity } from "@/lib/activity-heatmap";

describe("lib/activity-heatmap", () => {
  it("maps points into intensity buckets", () => {
    expect(getHeatmapIntensity(0, 40)).toBe(0);
    expect(getHeatmapIntensity(10, 40)).toBe(1);
    expect(getHeatmapIntensity(20, 40)).toBe(2);
    expect(getHeatmapIntensity(30, 40)).toBe(3);
    expect(getHeatmapIntensity(40, 40)).toBe(4);
  });

  it("builds a weekly grid in chronological order", () => {
    const cells = buildActivityHeatmap(
      [
        { activityDate: "2026-07-12", pointsEarned: 10 },
        { activityDate: "2026-07-13", pointsEarned: 20 },
      ],
      7,
      new Date(2026, 6, 13),
    );

    expect(cells).toHaveLength(7);
    expect(cells[6]?.activityDate).toBe("2026-07-13");
    expect(cells[5]?.activityDate).toBe("2026-07-12");
  });
});
