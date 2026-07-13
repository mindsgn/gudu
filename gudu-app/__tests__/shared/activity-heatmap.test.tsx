import renderer, { act } from "react-test-renderer";
import { ActivityHeatmap } from "@/shared/ui/organisms/activity-heatmap";

describe("shared/ui/organisms/activity-heatmap", () => {
  it("renders one cell per requested day", async () => {
    let tree!: renderer.ReactTestRenderer;

    await act(async () => {
      tree = renderer.create(
        <ActivityHeatmap
          activity={[
            { activityDate: "2026-07-12", pointsEarned: 10 },
            { activityDate: "2026-07-13", pointsEarned: 20 },
          ]}
          days={14}
        />,
      );
    });

    const cells = tree.root.findAll(
      (node) =>
        typeof node.props.testID === "string" &&
        node.props.testID.startsWith("heatmap-cell-"),
    );
    const uniqueCellIds = new Set(cells.map((node) => node.props.testID));

    expect(uniqueCellIds.size).toBe(14);
  });
});
