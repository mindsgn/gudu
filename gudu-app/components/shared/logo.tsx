import { colors } from "@/theme/colors";
import Block from "@/shared/ui/organisms/block";

interface LogoProps {
  background?: string
  base?: string
  borderRadius?: number
  borderWidth?: number
  glow?: string
  height?: number
  speed?: number
  width?: number
}

export const Logo = ({
  background= colors.background,
  base= colors.primaryMuted,
  borderRadius= 16,
  borderWidth= 5,
  glow= colors.accent,
  height= 72,
  speed= 2,
  width= 72,
}: LogoProps) => {

  return (
    <Block
      background={background}
      base={base}
      borderRadius={borderRadius}
      borderWidth={borderWidth}
      glow={glow}
      height={height}
      speed={speed}
      width={width}
    />
  );
};
