import { useEffect, useRef, useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { SymbolView } from "expo-symbols";
import { EnrichedMarkdownText } from "react-native-enriched-markdown";
import { useSharedValue } from "react-native-reanimated";
import { CircularProgress } from "@/shared/ui/organisms/circular-progress";
import { AnimatedScrollProgress } from "@/shared/ui/micro-interactions/animated-scroll-progress";
import {
  completeLesson,
  getLessonScreenData,
  markLessonOpened,
  saveLessonProgress,
  type CompletionResult,
  type LessonScreenData,
} from "@/db/learning";
import { colors } from "@/theme/colors";
import { typography } from "@/theme/typography";
import { Logo } from "@/components/shared/logo";


type ScreenState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; data: LessonScreenData };

export default function LessonScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ lessonId?: string | string[] }>();
  const lessonId = typeof params.lessonId === "string" ? params.lessonId : undefined;
  const [state, setState] = useState<ScreenState>({ status: "loading" });
  const [completing, setCompleting] = useState(false);
  const progress = useSharedValue(0);
  const latestMetricsRef = useRef({ progress: 0, offset: 0 });
  const completionTriggeredRef = useRef(false);
  const progressTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (progressTimeoutRef.current) {
        clearTimeout(progressTimeoutRef.current);
      }

      if (lessonId && !completionTriggeredRef.current) {
        void saveLessonProgress(
          lessonId,
          latestMetricsRef.current.progress,
          latestMetricsRef.current.offset,
        );
      }
    };
  }, [lessonId]);

  useEffect(() => {
    if (!lessonId) {
      setState({
        status: "error",
        message: "No lesson was selected.",
      });
      return;
    }

    let cancelled = false;

    const loadLesson = async () => {
      setState({ status: "loading" });
      completionTriggeredRef.current = false;

      try {
        const data = await getLessonScreenData(lessonId);
        progress.value = data.scrollPercent;
        latestMetricsRef.current = {
          progress: data.scrollPercent,
          offset: data.lastScrollOffset,
        };
        await markLessonOpened(lessonId);

        if (!cancelled) {
          setState({ status: "ready", data });
        }
      } catch (lessonError) {
        if (!cancelled) {
          setState({
            status: "error",
            message:
              lessonError instanceof Error
                ? lessonError.message
                : "Failed to load the lesson.",
          });
        }
      }
    };

    void loadLesson();

    return () => {
      cancelled = true;
    };
  }, [lessonId, progress]);

  const handleCompletion = async () => {
    if (!lessonId || completing) {
      return;
    }

    setCompleting(true);

    try {
      const result = await completeLesson(lessonId);
      routeToCompletion(router, result);
    } catch (completionError) {
      completionTriggeredRef.current = false;
      setState({
        status: "error",
        message:
          completionError instanceof Error
            ? completionError.message
            : "Failed to finish the lesson.",
      });
    } finally {
      setCompleting(false);
    }
  };

  const scheduleProgressSave = (nextProgress: number, nextOffset: number) => {
    if (!lessonId) {
      return;
    }

    latestMetricsRef.current = {
      progress: nextProgress,
      offset: nextOffset,
    };

    if (progressTimeoutRef.current) {
      clearTimeout(progressTimeoutRef.current);
    }

    progressTimeoutRef.current = setTimeout(() => {
      void saveLessonProgress(lessonId, nextProgress, nextOffset);
    }, 350);
  };

  if (state.status === "loading") {
    return (
      <View style={styles.centered}>
        <View style={styles.logoContainer}>
          <Logo speed={5}/>
        </View>
      </View>
    );
  }

  if (state.status === "error") {
    return (
      <View style={styles.centered}>
        <View style={styles.logoContainer}>
          <Logo speed={5} base={colors.danger}/>
        </View>
      </View>
    );
  }

  const { data } = state;

  return (
    <View style={styles.container}>
      <AnimatedScrollProgress
        contentOffset={{ x: 0, y: data.lastScrollOffset }}
        endReachedThreshold={100}
        fabBackgroundColor={colors.surface}
        fabBorderRadius={28}
        fabBottomOffset={42}
        fabEndBackgroundColor={colors.buttonTextBackground}
        fabHeight={60}
        fabWidth={280}
        onScrollMetricsChange={(nextProgress, nextOffset) => {
          progress.value = nextProgress;
          scheduleProgressSave(nextProgress, nextOffset);

          if (nextProgress >= 100 && !completionTriggeredRef.current) {
            completionTriggeredRef.current = true;
            void handleCompletion();
          }
        }}
        renderEndContent={() => (
          <View style={styles.fabCompleteContent}>
            <View>
              <Text style={styles.fabCompleteTitle}>Lesson complete</Text>
              <Text style={styles.fabCompleteSubtitle}>Unlocking what is next</Text>
            </View>
            <SymbolView
              name="checkmark.circle.fill"
              resizeMode="scaleAspectFit"
              size={30}
              tintColor={colors.surface}
            />
          </View>
        )}
        renderInitialContent={() => (
          <View style={styles.fabContent}>
            <View style={styles.fabTextContent}>
              <Text style={styles.fabTitle}>{data.moduleTitle}</Text>
              <Text style={styles.fabSubtitle}>{data.moduleTitle}</Text>
            </View>
            <CircularProgress
              backgroundColor={colors.surface}
              progress={progress}
              progressCircleColor={colors.accent}
              renderIcon={() => (
                <SymbolView
                  name="book.fill"
                  resizeMode="scaleAspectFit"
                  size={18}
                  tintColor={colors.buttonTextBackground}
                />
              )}
              size={38}
              strokeWidth={3}
            />
          </View>
        )}
      >
        <View style={styles.content}>
          <Text style={styles.courseLabel}>{data.courseTitle}</Text>
          <Text style={styles.moduleLabel}>{data.moduleTitle}</Text>
          <Text style={styles.title}>{data.title}</Text>
          <View style={styles.metaRow}>
            {data.estimatedStudyMinutes ? (
              <Text style={styles.metaText}>{data.estimatedStudyMinutes} min study</Text>
            ) : null}
            {data.estimatedPracticeMinutes ? (
              <Text style={styles.metaText}>
                {data.estimatedPracticeMinutes} min practice
              </Text>
            ) : null}
            {data.difficultyLabel ? (
              <Text style={styles.metaText}>{data.difficultyLabel}</Text>
            ) : null}
          </View>
          <EnrichedMarkdownText
            markdown={data.markdown}
            markdownStyle={markdownStyles}
          />
        </View>
      </AnimatedScrollProgress>
    </View>
  );
}

const routeToCompletion = (
  router: ReturnType<typeof useRouter>,
  result: CompletionResult,
) => {
  router.replace({
    pathname: "/complete",
    params: {
      courseSlug: result.courseSlug,
      currentStreak: `${result.currentStreak}`,
      lessonId: result.lessonId,
      lessonTitle: result.lessonTitle,
      nextLessonId: result.nextLessonId ?? "",
      nextLessonTitle: result.nextLessonTitle ?? "",
      pointsEarned: `${result.pointsEarned}`,
      totalPoints: `${result.totalPoints}`,
    },
  });
};

const markdownStyles = {
  paragraph: {
    color: colors.buttonTextBackground,
  },
  h1: {
    color: colors.buttonTextBackground,
  },
  h2: {
    color: colors.buttonTextBackground,
  },
  h3: {
    color: colors.buttonTextBackground,
  },
  h4: {
    color: colors.buttonTextBackground,
  },
  h5: {
    color: colors.buttonTextBackground,
  },
  h6: {
    color: colors.buttonTextBackground,
  },
  strong: {
    color: colors.buttonTextBackground,
  },
  em: {
    color: colors.buttonTextBackground,
  },
  list: {
    color: colors.buttonTextBackground,
  },
  link: {
    color: colors.accent,
  },
  blockquote: {
    backgroundColor: colors.surface,
    color: colors.buttonTextBackground,
  },
  code: {
    color: colors.surface,
  },
  math: {
    color: colors.buttonTextBackground,
  },
};

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
    paddingHorizontal: 16,
  },
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 80,
    paddingBottom: 180,
    gap: 12,
  },
  courseLabel: {
    ...typography.caption,
    color: colors.accent,
    textTransform: "uppercase",
  },
  moduleLabel: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  title: {
    ...typography.title,
    color: colors.buttonTextBackground,
  },
  metaRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8,
    marginBottom: 12,
  },
  metaText: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  fabContent: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  fabTextContent: {
    flex: 1,
    gap: 4,
  },
  fabTitle: {
    ...typography.body,
    color: colors.buttonTextBackground,
    fontWeight: "700",
  },
  fabSubtitle: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  fabCompleteContent: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  fabCompleteTitle: {
    ...typography.body,
    color: colors.surface,
    fontWeight: "700",
  },
  logoContainer: {
    alignItems: "center",
  },
  fabCompleteSubtitle: {
    ...typography.caption,
    color: colors.surface,
  },
});
