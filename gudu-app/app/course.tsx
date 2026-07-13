import { useCallback, useState } from "react";
import { Dimensions, StyleSheet, Text, View } from "react-native";
import { useFocusEffect, useLocalSearchParams, useRouter } from "expo-router";
import { FlashList } from "@shopify/flash-list";
import { Button } from "@/components/shared/pressable-card";
import { LessonListItem } from "@/components/shared/lesson-list-item";
import { StatePanel } from "@/components/shared/state-panel";
import {
  getCourseScreenData,
  type CourseScreenData,
  type CourseSection,
} from "@/db/learning";
import { AnimatedHeaderScrollView } from "@/shared/ui/organisms/animated-header-scrollview";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";

type ListItem =
  | {
      type: "module";
      id: string;
      title: string;
      summary: string | null;
    }
  | {
      type: "lesson";
      id: string;
      title: string;
      status: CourseSection["lessons"][number]["status"];
      orderIndex: number;
      estimatedStudyMinutes: number | null;
      difficultyLabel: string | null;
    };

type ScreenState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; data: CourseScreenData };

const flattenSections = (sections: CourseSection[]): ListItem[] => {
  return sections.flatMap((section) => [
    {
      type: "module" as const,
      id: section.id,
      title: section.title,
      summary: section.summary,
    },
    ...section.lessons.map((lesson) => ({
      type: "lesson" as const,
      id: lesson.id,
      title: lesson.title,
      status: lesson.status,
      orderIndex: lesson.orderIndex,
      estimatedStudyMinutes: lesson.estimatedStudyMinutes,
      difficultyLabel: lesson.difficultyLabel,
    })),
  ]);
};

export default function CourseScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ courseSlug?: string | string[] }>();
  const courseSlug =
    typeof params.courseSlug === "string" ? params.courseSlug : undefined;
  const [state, setState] = useState<ScreenState>({ status: "loading" });

  const loadCourse = useCallback(async () => {
    if (!courseSlug) {
      setState({
        status: "error",
        message: "No course was selected.",
      });
      return;
    }

    setState({ status: "loading" });

    try {
      const data = await getCourseScreenData(courseSlug);
      setState({ status: "ready", data });
    } catch (courseError) {
      setState({
        status: "error",
        message:
          courseError instanceof Error
            ? courseError.message
            : "Failed to load the selected course.",
      });
    }
  }, [courseSlug]);

  useFocusEffect(
    useCallback(() => {
      void loadCourse();
    }, [loadCourse]),
  );

  if (state.status === "loading") {
    return (
      <View style={styles.centered}>
        <StatePanel
          message="Loading lessons and unlock state."
          progress
          title="Preparing course"
        />
      </View>
    );
  }

  if (state.status === "error") {
    return (
      <View style={styles.centered}>
        <StatePanel
          actionLabel="Retry"
          message={state.message}
          onAction={() => {
            void loadCourse();
          }}
          title="Course unavailable"
        />
      </View>
    );
  }

  const items = flattenSections(state.data.sections);
  const { course, completedLessons, continueTarget } = state.data;

  return (
    <>
    <AnimatedHeaderScrollView
      largeTitle={course.title}
      subtitle={`${course.totalLessons} lessons across ${course.totalModules} modules`}
    >
      <FlashList
        data={items}
        getItemType={(item) => item.type}
          keyExtractor={(item) => `${item.type}-${item.id}`}
          ListFooterComponent={<View style={ {paddingBottom: 200,}}></View>}
        renderItem={({ item }) => {
          if (item.type === "module") {
            return (
              <View style={styles.moduleHeader}>
                <Text style={styles.moduleTitle}>{item.title}</Text>
                {item.summary ? (
                  <Text style={styles.moduleSummary}>{item.summary}</Text>
                ) : null}
              </View>
            );
          }

          return (
            <View style={styles.lessonItemWrap}>
              <LessonListItem
                difficultyLabel={item.difficultyLabel}
                estimatedStudyMinutes={item.estimatedStudyMinutes}
                onPress={() => {
                  router.push({
                    pathname: "/lesson",
                    params: { lessonId: item.id },
                  });
                }}
                orderIndex={item.orderIndex}
                status={item.status}
                testID={`lesson-row-${item.id}`}
                title={item.title}
              />
            </View>
          );
        }}
        scrollEnabled={false}
      />
      </AnimatedHeaderScrollView>

      {
        continueTarget ?
        <View style={styles.summaryCard}>
          {continueTarget ? (
            <Button
              accessibilityLabel="Continue this course"
              backgroundColor={colors.accent}
              color={colors.surface}
              label={`CONTINUE`}
              onPress={() => {
                router.push({
                  pathname: "/lesson",
                  params: { lessonId: continueTarget.lessonId },
                });
              }}
              width={Dimensions.get("window").width - 56}
            />
          ) : null}
          </View>
          : null
      }
    </>
  );
}

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
    paddingHorizontal: 16,
  },
  summaryCard: {
    position: "absolute",
    bottom: 0,
    backgroundColor: colors.surface,
    borderRadius: 24,
    padding: 20,
    gap: 12,
  },
  summaryTitle: {
    ...typography.body,
    color: colors.buttonTextBackground,
    lineHeight: 22,
  },
  summaryValue: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  moduleHeader: {
    paddingVertical: 12,
    gap: 6,
  },
  moduleTitle: {
    ...typography.subtitle,
    color: colors.buttonTextBackground,
  },
  moduleSummary: {
    ...typography.body,
    color: colors.textSecondary,
    lineHeight: 22,
  },
  lessonItemWrap: {
    marginBottom: 12,
  },
});
