import { registerRoot, Composition } from "remotion";
import { FakoContentTemplate } from "./Composition";

const RemotionRoot = () => {
  return (
    <Composition
      id="FakoTemplate"
      component={FakoContentTemplate}
      durationInFrames={420}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        meta: {
          track: "preview",
          branding: {
            primaryColor: "#D4AF37",
            backgroundColor: "#0A0A0A",
            fontFamily: "Impact",
          },
        },
        timeline: [
          {
            start: 0,
            end: 5,
            text: "PREVIEW MODE",
            uiMockup: "",
            animation: "scaleUp",
          },
        ],
      }}
    />
  );
};

registerRoot(RemotionRoot);
