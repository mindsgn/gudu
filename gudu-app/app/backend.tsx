import { useEffect } from "react";
import { useRouter } from "expo-router";
import { View } from "react-native";

export default function BackendRedirect() {
  const router = useRouter();

  useEffect(() => {
    router.replace({
      pathname: "/course",
      params: { courseSlug: "backend" },
    });
  }, [router]);

  return <View />;
}
