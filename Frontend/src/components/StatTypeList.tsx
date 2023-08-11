interface StatListProps {
  onSelect: (stat: string) => void;
}

function StatList({ onSelect }: StatListProps) {
  const stats = [
    {
      id: "pra",
      text: "On ___, ___ was the ___th player since ___ to score ___ points, grab ___ rebounds and deliver ___ assists.",
    },
    {
      id: "full",
      text: "On ___, ___ was the ___th player since ___ to score ___ points, grab ___ rebounds, deliver ___ assists, block ___ shots and get ___ steals.",
    },
    {
      id: "ef",
      text: "On ___, ___ was the __th player since ___ to score ___ points, grab ___ rebounds, deliver ___ assists, block ___ shots and get ___ steals while shooting over ___ percent from the field.",
    },
    {
      id: "season",
      text: "In the ___ season, ___ was the ___th player since ___ to average ___ points, ___ rebounds, and ___ assists.",
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
