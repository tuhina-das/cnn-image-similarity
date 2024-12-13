import React, { useEffect, useState } from "react";

const ProgressBar: React.FC = () => {
  const [progress, setProgress] = useState<number>(0); // Progress state (number type)

  // Simulate progress over time
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 100) return prev + 10; // Increase progress by 10 every second
        clearInterval(interval); // Stop when we reach 100
        return 100;
      });
    }, 1000); // Update every 1 second

    return () => clearInterval(interval); // Cleanup on component unmount
  }, []);

  return (
    <div className="relative h-5 rounded-full overflow-hidden bg-gray-300 mt-20 mx-10 w-full">
      <div
        className="absolute top-0 bottom-0 left-0 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
        style={{
          width: `${progress}%`, // Set width based on progress state
          transition: "width 1s ease", // Smooth width transition
        }}
      ></div>
    </div>
  );
};

export default ProgressBar;
