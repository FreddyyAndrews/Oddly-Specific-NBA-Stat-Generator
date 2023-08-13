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

function AnalystDisplay({ stat, analystData }: AnalystDisplayProps) {
  const analysts = [
    { image: chrissoRusso, name: "Mad Dog" },
    { image: Jefferson, name: "Richard Jefferson" },
    { image: kellerman, name: "Max Kellerman" },
    { image: mikeGreenberg, name: "Mike Greenberg" },
    { image: perkins, name: "Kendrick Perkins" },
    { image: rachelNichols, name: "Rachel Nichols" },
    { image: stephenA, name: "Stephen A Smith" },
  ];

  const randomAnalyst = analysts[Math.floor(Math.random() * analysts.length)];

  return (
    <div className="analyst-container">
      <img src={randomAnalyst.image} alt="Analyst" className="analyst-image" />
      <div className="analyst-text">
        {randomAnalyst.name} says: {analystData ? analystData : "Loading..."}
      </div>
    </div>
  );
}

export default AnalystDisplay;
