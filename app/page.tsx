import Image from "next/image";
import Link from "next/link";

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

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Detect The Percentage of Similarity Between Two Images</h1>
      <div className="grid grid-cols-4 gap-x-3 items-center">
        {images.map((image) => (
          <Image
            src={image.src}
            alt={image.alt}
            width={500}
            height={500}
            className="border-4 border-white"
          />
        ))}
      </div>
      {/* <h2>
        An Original Work project by Tuhina Das, ISM 2 (Topic: Software
        Development).
      </h2> */}
    </main>
  );
}
