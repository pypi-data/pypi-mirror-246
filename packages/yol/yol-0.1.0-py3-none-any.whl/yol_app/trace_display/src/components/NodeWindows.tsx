import React, { useContext, useEffect, useState } from "react";
import { TraceGraphContext } from "./TraceGraphContext";
import InputOutputWindow from "./InputOutputWindow";
import CloseIcon from "@mui/icons-material/CloseRounded";
import CodeWindow from "./CodeWindow";

const NodeWindows: React.FC = () => {
  const context = useContext(TraceGraphContext);

  // Local state to force re-render
  const [localWindows, setLocalWindows] = useState(context?.windows);
  const [visibleWindowId, setVisibleWindowId] = useState<
    string | null | undefined
  >(context?.visibleWindowId);
  useEffect(() => {
    if (context) {
      // Update local state when context changes
      setLocalWindows(context.windows);
      setVisibleWindowId(context.visibleWindowId || null);
    }
  }, [context?.windows, context?.visibleWindowId]); // Dependency on context's windows object

  if (!context) {
    throw new Error("NodeWindows must be used within a TraceGraphProvider");
  }

  const { hideWindow } = context;

  return (
    <>
      {localWindows &&
        Object.entries(localWindows).map(([key, windowData]) => {
          if (windowData.visible && key === visibleWindowId) {
            const [node, nodeNumber, windowType] = key.split("-");
            const nodeId = node + "-" + nodeNumber;
            const isInput = windowType === "Input";

            if (windowType === "Output" || windowType === "Input") {
              return (
                windowData.visible && (
                  <InputOutputWindow
                    key={key}
                    type={isInput ? "Input" : "Output"}
                    node={windowData.data}
                    icon={<CloseIcon />}
                    onClose={() =>
                      hideWindow(
                        nodeId.toString(),
                        isInput ? "Input" : "Output",
                        windowData.data
                      )
                    }
                  />
                )
              );
            } else {
              return (
                windowData.visible && (
                  <CodeWindow
                    key={key}
                    type="Code"
                    node={windowData.data}
                    icon={<CloseIcon />}
                    onClose={() =>
                      hideWindow(nodeId.toString(), "Code", windowData.data)
                    }
                  />
                )
              );
            }
          }
        })}
    </>
  );
};

export default NodeWindows;
