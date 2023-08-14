import React, { useState } from "react";
import StatList from "./components/StatTypeList";
import AnalystDisplay from "./components/AnalystDisplay";
import SocialLinks from "./components/SocialLinks";
import introImage from "/src/assets/intro.png";
import "./App.css";

function App() {
  const [selectedStat, setSelectedStat] = useState<string | null>(null);
  const [showCoverImage, setShowCoverImage] = useState<boolean>(true);
  const [analystData, setAnalystData] = useState<any>(null);

  const handleStatSelect = async (stat: string) => {
    setShowCoverImage(false);
    setSelectedStat(stat);

    let endpoint;
    switch (stat) {
      case "pra":
        endpoint =
          "https://oddly-specific-nba-stat-602f1804cb37.herokuapp.com/api/v1/stat/pra";
        break;
      case "full":
        endpoint =
          "https://oddly-specific-nba-stat-602f1804cb37.herokuapp.com/api/v1/stat/full";
        break;
      case "ef":
        endpoint =
          "https://oddly-specific-nba-stat-602f1804cb37.herokuapp.com/api/v1/stat/ef";
        break;
      case "season":
        endpoint =
          "https://oddly-specific-nba-stat-602f1804cb37.herokuapp.com/api/v1/stat/season";
        break;
      default:
        endpoint =
          "https://oddly-specific-nba-stat-602f1804cb37.herokuapp.com/api/v1/stat/pra";
        break;
    }

    // Make the API call
    try {
      const response = await fetch(endpoint);
      const data = await response.text();
      console.log("Fetched data:", data);
      setAnalystData(data);
      setSelectedStat(stat);
    } catch (error) {
      console.error("An error occurred while fetching data:", error);
    }
  };

  return (
    <div>
      {showCoverImage && (
        <div className="analyst-container">
          <img src={introImage} alt="Intro" className="analyst-image" />
        </div>
      )}
      <StatList onSelect={handleStatSelect} />
      {selectedStat && (
        <AnalystDisplay stat={selectedStat} analystData={analystData} />
      )}
      <SocialLinks />
    </div>
  );
}

export default App;
