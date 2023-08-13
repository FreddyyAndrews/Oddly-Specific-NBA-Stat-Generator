interface StatListProps {
  onSelect: (stat: string) => void;
}

function StatList({ onSelect }: StatListProps) {
  const stats = [
    {
      id: "pra",
      text: "Generate game stat (PTS, REB, AST)",
    },
    {
      id: "full",
      text: "Generate game stat (PTS, REB, AST, BLK, STL)",
    },
    {
      id: "ef",
      text: "Generate game stat (PTS, REB, AST, BLK, STL, FG-PCT)",
    },
    {
      id: "season",
      text: "Generate season stat",
    },
  ];

  return (
    <div className="list-group-container">
      <ul className="list-group">
        {stats.map((stat, index) => (
          <li
            key={index}
            className="list-group-item"
            onClick={() => onSelect(stat.id)}
          >
            {stat.text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StatList;
