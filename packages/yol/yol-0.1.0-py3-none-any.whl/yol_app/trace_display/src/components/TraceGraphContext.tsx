import React, { createContext, useState, ReactNode } from "react";
import { FunctionNode } from "./TraceGraph"; // Import your existing FunctionNode type
import { Argument, Return } from "../types"; // Import the types

interface WindowState {
  data: FunctionNode;
  visible: boolean;
}

interface TraceGraphContextProps {
  windows: Record<string, WindowState>;
  visibleWindowId: string | null; // The ID of the currently visible window, or null if none are visible
  showWindow: (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => void;
  hideWindow: (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => void;
}

export const TraceGraphContext = createContext<TraceGraphContextProps | null>(
  null
);

export const TraceGraphProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [windows, setWindows] = useState<Record<string, WindowState>>({});
  const [visibleWindowId, setVisibleWindowId] = useState<string | null>(null);

  const showWindow = (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => {
    const windowId = `${nodeId}-${type}`;
    setWindows((prev) => ({
      ...prev,
      [`${nodeId}-${type}`]: { data, visible: true },
    }));
    setVisibleWindowId(windowId); // Set this window as the visible one
  };

  const hideWindow = (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => {
    setVisibleWindowId(null); // No window is visible
    setWindows((prev) => ({
      ...prev,
      [`${nodeId}-${type}`]: { data, visible: false },
    }));
  };

  return (
    <TraceGraphContext.Provider
      value={{ windows, visibleWindowId, showWindow, hideWindow }}
    >
      {children}
    </TraceGraphContext.Provider>
  );
};
