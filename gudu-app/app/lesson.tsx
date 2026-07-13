import { StyleSheet, View, Text } from "react-native";
import { useRouter } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import { useFocusEffect } from "expo-router";
import * as Haptics from "expo-haptics";
import { AnimatedScrollProgress } from "@/shared/ui/micro-interactions/animated-scroll-progress";
import { useSharedValue } from "react-native-reanimated";
import { CircularProgress } from "@/shared/ui/organisms/circular-progress";
import { SymbolView } from "expo-symbols";
import { EnrichedMarkdownText } from "react-native-enriched-markdown";
import { content } from "@/constants/backend";

const STORY = {
  title: "HTTP Protocol",
  author: "James Scott",
  date: "August 03, 2023",
  content: ``,
};

export default function Backend() {
  const router = useRouter();
  const [isComplete, setComplete] = useState<boolean>();

  const progress = useSharedValue<number>(0);

  useFocusEffect(
    useCallback(() => {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);

      return () => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Soft);
      };
    }, []),
  );

  useEffect(() => {
    if (isComplete) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setTimeout(() => {
        router.replace("/complete");
      }, 500);
    }
  }, [isComplete]);

  return (
    <View style={styles.container}>
      <AnimatedScrollProgress
        fabWidth={280}
        fabHeight={56}
        fabBottomOffset={50}
        fabBackgroundColor="#151515"
        fabEndBackgroundColor="#fff"
        fabBorderRadius={28}
        showFabOnScroll
        fabAppearScrollOffset={50}
        onScrollProgressChange={(_value) => {
          progress.value = _value;
          if (_value == 100 && !isComplete) {
            setComplete(true);
          }
        }}
        renderInitialContent={() => (
          <View style={styles.fabContent}>
            <View style={styles.fabTextContent}>
              <Text style={[styles.fabTitle]}>{STORY.title}</Text>
              <Text style={[styles.fabSubtitle]}>Chapter 1</Text>
            </View>
            <View
              style={{
                position: "absolute",
                left: 200,
              }}
            >
              <CircularProgress
                progress={progress}
                size={36}
                renderIcon={() => (
                  <SymbolView
                    name="arrow.forward.circle.fill"
                    tintColor={"#fff"}
                    size={30}
                    resizeMode="scaleAspectFit"
                  />
                )}
                strokeWidth={3}
                backgroundColor="#333"
              />
            </View>
          </View>
        )}
        renderEndContent={() => (
          <>
            <View
              style={{
                flexDirection: "row",
                alignItems: "center",
                flex: 1,
              }}
            >
              <View>
                <Text style={[{ color: "#000", fontSize: 18 }]}>
                  Well done!
                </Text>
                <Text style={[{ color: "#3d3d3d", fontSize: 12 }]}>
                  Let's move on.
                </Text>
              </View>
              <View
                style={{
                  position: "absolute",
                  left: 200,
                }}
              >
                <SymbolView
                  name="book.fill"
                  size={36}
                  style={{
                    marginRight: 10,
                  }}
                  resizeMode="scaleAspectFit"
                  tintColor="#000"
                />
              </View>
            </View>
          </>
        )}
      >
        <View style={styles.content}>
          <Text style={[styles.title]}>{STORY.title}</Text>

          <View style={styles.divider} />
          <View
            style={{
              flex: 1,
              paddingBottom: 200,
            }}
          >
            <EnrichedMarkdownText
              markdown={content}
              markdownStyle={{
                paragraph: {
                  color: "#FFF",
                },
                h1: {
                  color: "#FFF",
                },
                h2: {
                  color: "#FFF",
                },
                h3: {
                  color: "#FFF",
                },
                h4: {
                  color: "#FFF",
                },
                h5: {
                  color: "#FFF",
                },
                h6: {
                  color: "#FFF",
                },
                strong: {
                  color: "#FFF",
                },
                em: {
                  color: "#FFF",
                },
                strikethrough: {
                  color: "#FFF",
                },
                underline: {
                  color: "#FFF",
                },
                link: {
                  color: "#FFF",
                },
                code: {
                  color: "#000",
                },
                codeBlock: {},
                blockquote: {
                  backgroundColor: "#1D2430",
                  color: "#fff",
                },
                list: {
                  color: "#FFF",
                },
                image: {},
                inlineImage: {},
                taskList: {},
                math: {
                  color: "#FFF",
                },
                inlineMath: {
                  color: "#FFF",
                },
                spoiler: {
                  color: "#FFF",
                },
                superscript: {
                  color: "#FFF",
                },
                subscript: {
                  color: "#FFF",
                },
                highlight: {
                  color: "#FFF",
                },
              }}
            />
          </View>
        </View>
      </AnimatedScrollProgress>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "black",
    color: "white",
  },
  content: {
    paddingHorizontal: 24,
    paddingTop: 70,
    paddingBottom: 140,
  },
  badge: {
    alignSelf: "flex-start",
    backgroundColor: "#1a1a1a",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    marginBottom: 16,
  },
  badgeText: {
    fontSize: 12,
    color: "#555",
    fontWeight: "600",
  },
  title: {
    fontSize: 36,
    fontWeight: "700",
    color: "#fff",
    marginBottom: 24,
  },
  authorRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#1a1a1a",
    justifyContent: "center",
    alignItems: "center",
  },
  author: {
    fontSize: 15,
    color: "#fff",
    fontWeight: "500",
  },
  date: {
    fontSize: 13,
    color: "#555",
    marginTop: 2,
  },
  divider: {
    height: 1,
    backgroundColor: "#1a1a1a",
    marginVertical: 28,
  },
  body: {
    fontSize: 17,
    color: "#000",
    lineHeight: 28,
  },
  fabContent: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 0,
  },
  fabTextContent: {
    gap: 2,
  },
  fabTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#fff",
  },
  fabSubtitle: {
    fontSize: 12,
    color: "#555",
  },
});
