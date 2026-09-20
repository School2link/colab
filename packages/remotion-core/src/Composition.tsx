import {
  getInputProps,
  useCurrentFrame,
  useVideoConfig,
  Audio,
  Img,
  OffthreadVideo,
  staticFile,
  AbsoluteFill,
  interpolate,
  spring,
  Easing,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import "./styles/global.css";

const KenBurnsImage: React.FC<{
  src: string;
  animation: string;
  durationInFrames: number;
}> = ({ src, animation, durationInFrames }) => {
  const frame = useCurrentFrame();

  let scale = 1;
  let translateX = 0;
  let translateY = 0;

  if (animation === "zoomIn") {
    scale = interpolate(frame, [0, durationInFrames], [1.0, 1.25], {
      extrapolateRight: "clamp",
    });
    translateY = interpolate(frame, [0, durationInFrames], [0, -20], {
      extrapolateRight: "clamp",
    });
  } else if (animation === "zoomOut") {
    scale = interpolate(frame, [0, durationInFrames], [1.25, 1.0], {
      extrapolateRight: "clamp",
    });
    translateY = interpolate(frame, [0, durationInFrames], [-20, 0], {
      extrapolateRight: "clamp",
    });
  } else if (animation === "panRight") {
    scale = 1.15;
    translateX = interpolate(frame, [0, durationInFrames], [-30, 30], {
      extrapolateRight: "clamp",
    });
  }

  return (
    <AbsoluteFill>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
        }}
      />
    </AbsoluteFill>
  );
};

const DarkScrim: React.FC<{ variant?: "full" | "bottom" }> = ({
  variant = "full",
}) => {
  if (variant === "bottom") {
    return (
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.5) 40%, transparent 70%)",
        }}
      />
    );
  }
  return (
    <AbsoluteFill
      style={{
        background:
          "linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.6) 50%, rgba(0,0,0,0.8) 100%)",
      }}
    />
  );
};

const AnimatedText: React.FC<{
  text: string;
  color: string;
  fontSize?: number;
  animation?: string;
  fontWeight?: number;
}> = ({ text, color, fontSize = 72, animation = "zoom", fontWeight = 900 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "8px 16px",
        padding: "0 60px",
      }}
    >
      {words.map((word, i) => {
        const stagger = i * 4;

        const enter = spring({
          frame: Math.max(0, frame - stagger),
          fps,
          config:
            animation === "shake"
              ? { damping: 8, stiffness: 200, mass: 0.8 }
              : animation === "cascade"
                ? { damping: 12, stiffness: 150, mass: 0.6 }
                : { damping: 14, stiffness: 120, mass: 0.8 },
        });

        const y = interpolate(enter, [0, 1], [60, 0]);
        const opacity = interpolate(enter, [0, 0.3], [0, 1], {
          extrapolateRight: "clamp",
        });
        const scale = interpolate(enter, [0, 1], [0.5, 1]);

        const shakeX =
          animation === "shake"
            ? interpolate(
                frame,
                [stagger, stagger + 3, stagger + 6, stagger + 9, stagger + 12],
                [0, -8, 8, -4, 0],
                { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
              )
            : 0;

        const isLast = i === words.length - 1;
        const pulseScale =
          animation === "zoom" && isLast
            ? spring({
                frame: Math.max(0, frame - words.length * 4 - 10),
                fps,
                config: { damping: 8, stiffness: 300 },
                from: 1,
                to: 1.15,
              })
            : 1;

        return (
          <span
            key={`${word}-${i}`}
            style={{
              display: "inline-block",
              fontSize,
              fontWeight,
              color: isLast ? color : "#FFFFFF",
              transform: `translateY(${y}px) translateX(${shakeX}px) scale(${scale * pulseScale})`,
              opacity,
              textShadow: isLast
                ? `0 0 40px ${color}60, 0 0 80px ${color}30`
                : "0 4px 20px rgba(0,0,0,0.9), 0 2px 8px rgba(0,0,0,0.8)",
              letterSpacing: "-0.02em",
              lineHeight: 1.1,
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

const ImageScene: React.FC<{
  text: string;
  image: string;
  primaryColor: string;
  kenBurns?: string;
  animation?: string;
  isCTA?: boolean;
}> = ({
  text,
  image,
  primaryColor,
  kenBurns = "zoomIn",
  animation = "zoom",
  isCTA = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const exitStart = durationInFrames - 15;
  const exitOpacity = interpolate(frame, [exitStart, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const exitScale = interpolate(
    frame,
    [exitStart, durationInFrames],
    [1, 0.95],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ opacity: exitOpacity, transform: `scale(${exitScale})` }}>
      <KenBurnsImage
        src={staticFile(image)}
        animation={kenBurns}
        durationInFrames={durationInFrames}
      />

      <DarkScrim variant={isCTA ? "full" : "bottom"} />

      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            maxWidth: "90%",
            marginTop: isCTA ? 0 : "15%",
          }}
        >
          {isCTA && (
            <div
              style={{
                position: "absolute",
                bottom: "30%",
                width: "60%",
                height: 4,
                background: `linear-gradient(90deg, transparent, ${primaryColor}, transparent)`,
                opacity: interpolate(
                  spring({ frame, fps, config: { damping: 200 } }),
                  [0, 1],
                  [0, 0.8]
                ),
              }}
            />
          )}
          <AnimatedText
            text={text}
            color={primaryColor}
            fontSize={isCTA ? 60 : 72}
            animation={animation}
            fontWeight={900}
          />
          {isCTA && (
            <div
              style={{
                marginTop: 28,
                fontSize: 30,
                color: "#FFFFFF",
                opacity: interpolate(frame, [20, 35], [0, 0.8], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                }),
                letterSpacing: "0.15em",
                textTransform: "uppercase",
                textShadow: "0 2px 12px rgba(0,0,0,0.8)",
              }}
            >
              Start Selling Today
            </div>
          )}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const TalkingScene: React.FC<{
  text: string;
  image: string;
  video?: string;
  primaryColor: string;
  animation?: string;
}> = ({ text, image, video, primaryColor, animation = "zoom" }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const exitStart = durationInFrames - 15;
  const exitOpacity = interpolate(frame, [exitStart, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const exitScale = interpolate(
    frame,
    [exitStart, durationInFrames],
    [1, 0.95],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const breathe = interpolate(
    frame,
    [0, durationInFrames * 0.25, durationInFrames * 0.5, durationInFrames * 0.75, durationInFrames],
    [1.0, 1.02, 1.0, 1.015, 1.0],
    { extrapolateRight: "clamp" }
  );

  const subtlePan = interpolate(
    frame,
    [0, durationInFrames],
    [-8, 8],
    { extrapolateRight: "clamp" }
  );

  const subtleY = interpolate(
    frame,
    [0, durationInFrames * 0.5, durationInFrames],
    [0, -4, 0],
    { extrapolateRight: "clamp" }
  );

  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.15], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ opacity: exitOpacity, transform: `scale(${exitScale})` }}>
      <AbsoluteFill>
        {video ? (
          <OffthreadVideo
            src={staticFile(video)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : (
          <Img
            src={staticFile(image)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${scale * breathe}) translate(${subtlePan}px, ${subtleY}px)`,
            }}
          />
        )}
      </AbsoluteFill>

      <DarkScrim variant="bottom" />

      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            maxWidth: "90%",
            marginTop: "15%",
          }}
        >
          <AnimatedText
            text={text}
            color={primaryColor}
            fontSize={72}
            animation={animation}
            fontWeight={900}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const FakoContentTemplate = () => {
  const { meta, timeline = [] } = getInputProps();
  const primaryColor = meta?.branding?.primaryColor || "#D4AF37";

  const scene1Frames = 130;
  const scene2Frames = 157;
  const scene3Frames = 157;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0A0A" }}>
      {meta?.audio?.voiceFile && (
        <Audio src={staticFile(meta.audio.voiceFile)} volume={1.0} />
      )}
      {meta?.audio?.bgMusic && (
        <Audio src={staticFile(meta.audio.bgMusic)} volume={0.15} loop />
      )}

      <TransitionSeries>
        {timeline[0] && (
          <TransitionSeries.Sequence durationInFrames={scene1Frames}>
            {timeline[0].talkScene ? (
              <TalkingScene
                text={timeline[0].text}
                image={timeline[0].image}
                video={timeline[0].video}
                primaryColor={primaryColor}
                animation="zoom"
              />
            ) : (
              <ImageScene
                text={timeline[0].text}
                image={timeline[0].image}
                primaryColor={primaryColor}
                kenBurns={timeline[0].kenBurns || "zoomIn"}
                animation="zoom"
              />
            )}
          </TransitionSeries.Sequence>
        )}

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 12 })}
        />

        {timeline[1] && (
          <TransitionSeries.Sequence durationInFrames={scene2Frames}>
            {timeline[1].talkScene ? (
              <TalkingScene
                text={timeline[1].text}
                image={timeline[1].image}
                video={timeline[1].video}
                primaryColor={primaryColor}
                animation="cascade"
              />
            ) : (
              <ImageScene
                text={timeline[1].text}
                image={timeline[1].image}
                primaryColor={primaryColor}
                kenBurns={timeline[1].kenBurns || "panRight"}
                animation="cascade"
              />
            )}
          </TransitionSeries.Sequence>
        )}

        <TransitionSeries.Transition
          presentation={slide({ direction: "from-bottom" })}
          timing={linearTiming({ durationInFrames: 12 })}
        />

        {timeline[2] && (
          <TransitionSeries.Sequence durationInFrames={scene3Frames}>
            {timeline[2].talkScene ? (
              <TalkingScene
                text={timeline[2].text}
                image={timeline[2].image}
                video={timeline[2].video}
                primaryColor={primaryColor}
                animation="zoom"
              />
            ) : (
              <ImageScene
                text={timeline[2].text}
                image={timeline[2].image}
                primaryColor={primaryColor}
                kenBurns={timeline[2].kenBurns || "zoomOut"}
                animation="zoom"
                isCTA
              />
            )}
          </TransitionSeries.Sequence>
        )}
      </TransitionSeries>

      <div
        style={{
          position: "absolute",
          top: 80,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <span
          style={{
            fontSize: 22,
            letterSpacing: "0.25em",
            color: "#FFFFFF",
            opacity: 0.5,
            textTransform: "uppercase",
            textShadow: "0 2px 10px rgba(0,0,0,0.8)",
          }}
        >
          Fako Online
        </span>
      </div>
    </AbsoluteFill>
  );
};
