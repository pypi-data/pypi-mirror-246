import React from "react";
import Button from "@material-ui/core/Button";
import "./Header.css";
import VersionCheck from "../VersionCheck";

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header__logo">YOL</div>
      <VersionCheck />
      <Button
        variant="contained"
        className="header__feedback"
        href="https://forms.gle/WSyYjaa8B7cYHTuu5"
        target="_blank"
        rel="noopener noreferrer"
      >
        Feedback
      </Button>
    </header>
  );
};

export default Header;
