import { FaLongArrowAltDown, FaLongArrowAltLeft, FaLongArrowAltRight, FaLongArrowAltUp } from "react-icons/fa";
import React, { useState, useEffect } from "react";

export const ArrowKeys = React.memo(({ value }) => {
  const [keyDown, setKeyDown] = useState({
    up: false,
    down: false,
    left: false,
    right: false,
  });

  const handleKeyPress = (e, isKeyDown) => {
    const directionKeyMap = {
      w: "up",
      a: "left",
      s: "down",
      d: "right",
    };

    if (e.key in directionKeyMap) {
      const direction = directionKeyMap[e.key];
      setKeyDown({ ...keyDown, [direction]: isKeyDown });

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      };

      console.log(`Sending request to http://localhost:5000/${direction}`);
      fetch(`http://localhost:5000/${direction}`, requestOptions)
        .then((response) => {
          if (response.ok) {
            console.log(`Success: ${direction}`);
          } else {
            console.log(`Error: ${direction}`);
          }
        })
        .catch((error) => {
          console.error(`Error: ${error}`);
        });
    }
  };

  useEffect(() => {
    const handleKeyDown = (e) => handleKeyPress(e, true);
    const handleKeyUp = (e) => handleKeyPress(e, false);

    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("keyup", handleKeyUp);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  console.log(`ArrowKeys component rendered with value: ${value}`);

  return (
    <div className="bg">
      {value === "forward" ? (
        <FaLongArrowAltUp className={`controlls ${value} ${keyDown.up && "animate"}`} />
      ) : value === "right" ? (
        <FaLongArrowAltRight className={`controlls ${value} ${keyDown.right && "animateX"}`} />
      ) : value === "left" ? (
        <FaLongArrowAltLeft className={`controlls ${value} ${keyDown.left && "animateX"}`} />
      ) : (
        <FaLongArrowAltDown className={`controlls ${value} ${keyDown.down && "animate"}`} />
      )}
    </div>
  );
});
