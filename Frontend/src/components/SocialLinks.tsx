import linkedinLogo from "/src/assets/linkedin-logo.png";
import githubLogo from "/src/assets/github-logo.png";

function SocialLinks() {
  return (
    <div className="social-links">
      <a
        href="https://www.linkedin.com/in/frederick-wilson-andrews/"
        target="_blank"
        rel="noreferrer"
      >
        <img src={linkedinLogo} alt="LinkedIn" />
      </a>
      <a
        href="https://github.com/FreddyyAndrews/Oddly-Specific-NBA-Stat-Generator"
        target="_blank"
        rel="noreferrer"
      >
        <img src={githubLogo} alt="GitHub" />
      </a>
    </div>
  );
}

export default SocialLinks;
