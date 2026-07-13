import { colors } from "@/constants/index";

describe("constants/index", () => {
  it("exports colors object", () => {
    expect(colors).toBeDefined();
    expect(typeof colors).toBe("object");
  });

  it("has primary color", () => {
    expect(colors.primary).toBe("#000");
  });
});
