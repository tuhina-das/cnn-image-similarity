"use client";
import Image from "next/image";
import Link from "next/link";
import React from "react";
import { useState } from "react";
import ProgressBar from "./ProgressBar";

export default function Home() {
  // Constant containing all images used
  const images = [
    { src: "/images/galaxywolf.jpg", alt: "Galaxy Wolf Art" },
    { src: "/images/black.jpg", alt: "Black" },
    {
      src: "/images/galaxywolf_hoodie_closeup.png",
      alt: "Galaxy Wolf Hoodie (Closeup)",
    },
    { src: "/images/galaxywolf_hoodie.jpg", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/gemmakeith_stolen.png", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/gemmakeith.png", alt: "Galaxy Wolf Hoodie" },
    {
      src: "/images/indigochild_altcolors.png",
      alt: "Galaxy Wolf Hoodie",
    },
    { src: "/images/indigochild_closeup.png", alt: "Galaxy Wolf Hoodie" },
    {
      src: "/images/indigochild_stolen_closeup.png",
      alt: "Galaxy Wolf Hoodie",
    },
    { src: "/images/indigochild_stolen.jpg", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/patchwork.jpg", alt: "Galaxy Wolf Hoodie" },
    {
      src: "/images/petitepastels_stolen.png",
      alt: "Galaxy Wolf Hoodie",
    },
    { src: "/images/petitepastels.png", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/saintrem.jpeg", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/sleepburger.jpg", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/starrynight.webp", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/tiinamenzel.png", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/tiinamenzel_stolen.png", alt: "Galaxy Wolf Hoodie" },
    { src: "/images/white.jpg", alt: "Galaxy Wolf Hoodie" },
  ];

  const [activeImages, setActiveImages] = useState<string[]>([]);
  const [message, setMessage] = useState<string>("");

  function handleClick(src: string) {
    console.log("Image clicked: " + src);
    if (activeImages.length < 2) {
      console.log("Before " + activeImages);
      setActiveImages((activeImages) => [...activeImages, src]);
      console.log("After " + activeImages);
    } else {
      console.log("Two images already: " + activeImages);
      console.log("Removing the first image...");
      const newActiveImages = [...activeImages];
      newActiveImages.shift();
      newActiveImages.push(src);
      setActiveImages(newActiveImages);
    }
  }

  function submitInfo() {
    fetch("http://127.0.0.1:5000/api/app", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        string1: activeImages[0],
        string2: activeImages[1],
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        const data_rounded = Math.ceil(data.response * 100);
        console.log("Response from Flask:", data_rounded); // debug
        if (data_rounded >= 90) {
          setMessage("These images are definitely similar");
        } else if (data_rounded >= 80) {
          setMessage("These images are likely similar");
        } else if (data_rounded >= 70) {
          setMessage("These images are sort of similar");
        } else {
          setMessage("These images aren't really similar");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-3xl my-[2vh]">
        Detect The Percentage of Similarity Between Two Images
      </h1>
      <h2 className="pt-[2vh] w-[40vw] text-center">
        How similar are two images? Using cosine similarity and a bit of machine
        learning, we can actually measure the relative similarity in appearance
        between two images. This is helpful in several ways -- namely, to teach
        computers to identify dupes of different items. Select two images and
        give it a try!
      </h2>
      <h1 className="text-3xl my-[2vh] text-sky-400">{message}</h1>
      <button
        className="border-none bg-sky-400 p-3 mt-[2vh] mb-[3vh] rounded-lg text-black"
        onClick={() => submitInfo()}
      >
        Check Similarity
      </button>
      <div className="grid grid-cols-4 gap-x-3 items-center">
        {images.map((image) => (
          <div key={image.src} onClick={() => handleClick(image.src)}>
            <Image
              src={image.src}
              alt={image.alt}
              style={{
                border: activeImages.includes(image.src)
                  ? "6px solid #39FF14"
                  : "6px solid white",
              }}
              width={200}
              height={200}
            />
          </div>
        ))}
      </div>
      <h2 className="pt-[4vh]">
        An Original Work project by Tuhina Das, ISM 2 (Topic: Software
        Development)
      </h2>
    </main>
  );
}
