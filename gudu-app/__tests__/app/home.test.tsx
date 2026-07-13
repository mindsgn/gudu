import renderer, { act } from "react-test-renderer";
import Home from "@/app/home";

jest.mock("@/db/learning", () => ({
  getHomeDashboardData: jest.fn(async () => ({
    profile: {
      id: "local-learner",
      totalPoints: 120,
      currentStreak: 3,
      longestStreak: 7,
      lastActiveOn: "2026-07-13",
      createdAt: 1,
      updatedAt: 1,
    },
    activity: [
      { activityDate: "2026-07-12", pointsEarned: 10 },
      { activityDate: "2026-07-13", pointsEarned: 20 },
    ],
    continueTarget: {
      courseId: "backend",
      courseSlug: "backend",
      lessonId: "backend:1",
      lessonTitle: "Lesson 1",
      moduleTitle: "Phase 1",
      orderIndex: 1,
      lastOpenedAt: 10,
      reason: "resume",
    },
    courses: [
      {
        id: "backend",
        slug: "backend",
        title: "Backend Engineering",
        description: "Backend track",
        totalLessons: 105,
        totalModules: 7,
        completedLessons: 2,
        inProgressLessons: 1,
        nextLessonId: "backend:1",
        nextLessonTitle: "Lesson 1",
      },
      {
        id: "frontend",
        slug: "frontend",
        title: "Frontend Engineering",
        description: "Frontend track",
        totalLessons: 180,
        totalModules: 18,
        completedLessons: 0,
        inProgressLessons: 0,
        nextLessonId: "frontend:1",
        nextLessonTitle: "Lesson 1",
      },
    ],
  })),
}));

describe("app/home", () => {
  it("renders the dashboard summary and both course cards", async () => {
    let tree!: renderer.ReactTestRenderer;

    await act(async () => {
      tree = renderer.create(<Home />);
    });

    const courseCards = tree.root.findAll(
      (node: renderer.ReactTestInstance) =>
        typeof node.props.testID === "string" &&
        node.props.testID.startsWith("course-card-"),
    );
    const uniqueCourseCardIds = new Set(
      courseCards.map((node) => node.props.testID),
    );
    const continueButton = tree.root.findByProps({
      testID: "home-continue-button",
    });

    expect(uniqueCourseCardIds.size).toBe(2);
    expect(continueButton).toBeDefined();
  });
});
