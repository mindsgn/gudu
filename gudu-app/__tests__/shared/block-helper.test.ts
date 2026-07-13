import { hexToRgb } from "@/shared/ui/organisms/block/helper";

describe("shared/ui/organisms/block/helper", () => {
  describe("hexToRgb", () => {
    it("converts 6-digit hex to RGB", () => {
      const result = hexToRgb("#FF0000");
      expect(result).toEqual([1, 0, 0]);
    });

    it("converts 6-digit hex without hash", () => {
      const result = hexToRgb("00FF00");
      expect(result).toEqual([0, 1, 0]);
    });

    it("converts 3-digit hex to RGB", () => {
      const result = hexToRgb("#F00");
      expect(result).toEqual([1, 0, 0]);
    });

    it("converts 3-digit hex without hash", () => {
      const result = hexToRgb("0F0");
      expect(result).toEqual([0, 1, 0]);
    });

    it("converts black", () => {
      const result = hexToRgb("#000000");
      expect(result).toEqual([0, 0, 0]);
    });

    it("converts white", () => {
      const result = hexToRgb("#FFFFFF");
      expect(result).toEqual([1, 1, 1]);
    });

    it("converts a mid-range color", () => {
      const result = hexToRgb("#333340");
      const [r, g, b] = result;
      expect(r).toBeCloseTo(51 / 255, 5);
      expect(g).toBeCloseTo(51 / 255, 5);
      expect(b).toBeCloseTo(64 / 255, 5);
    });

    it("preserves the generic type parameter", () => {
      const result = hexToRgb<"#16A34A">("#16A34A");
      expect(result).toHaveLength(3);
      result.forEach((component) => {
        expect(component).toBeGreaterThanOrEqual(0);
        expect(component).toBeLessThanOrEqual(1);
      });
    });
  });
});
