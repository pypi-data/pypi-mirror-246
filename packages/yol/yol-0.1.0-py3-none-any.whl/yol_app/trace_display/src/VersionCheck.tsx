import React, { useState, useEffect } from "react";
import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";

const VersionCheck: React.FC = () => {
  const [versionInfo, setVersionInfo] = useState({
    current_version: "",
    latest_version: "",
    message: "",
  });

  useEffect(() => {
    fetch("/check-version")
      .then((response) => response.json())
      .then((data) => {
        setVersionInfo(data);
      })
      .catch((error) => console.error("Error checking version:", error));
  }, []);

  if (
    versionInfo.current_version &&
    versionInfo.latest_version !== versionInfo.current_version
  ) {
    return (
      <Alert severity="warning">
        {versionInfo.message} -
        <Button
          color="inherit"
          onClick={() =>
            navigator.clipboard.writeText("pip install --upgrade yol_app")
          }
        >
          Copy Upgrade Command
        </Button>
      </Alert>
    );
  }

  return null;
};

export default VersionCheck;
