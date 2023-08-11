import chrissoRusso from "/src/assets/russo.webp";
import Jefferson from "/src/assets/jefferson.jpg";
import kellerman from "/src/assets/kellerman.webp";
import mikeGreenberg from "/src/assets/greenberg.jpg";
import perkins from "/src/assets/perkins.jpg";
import rachelNichols from "/src/assets/nichols.jpg";
import stephenA from "/src/assets/stephen-A.jpg";

type AnalystDisplayProps = {
  stat: string;
  analystData: any;
};

function AnalystDisplay({ stat }: { stat: string }) {
  const images = [
    chrissoRusso,
    Jefferson,
    kellerman,
    mikeGreenberg,
    perkins,
    rachelNichols,
    stephenA,
  ];

  const randomImage = images[Math.floor(Math.random() * images.length)];

  return (
    <div className="analyst-container">
      <img src={randomImage} alt="Analyst" className="analyst-image" />
      <div className="analyst-text">
        {analystData ? analystData : "Loading..."}
      </div>
    </div>
  );
}

export default AnalystDisplay;
