function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span className="navbar-seal" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path
              d="M12 2l7 3v6c0 5-3.2 8.7-7 11-3.8-2.3-7-6-7-11V5l7-3z"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinejoin="round"
            />
          </svg>
        </span>
        <div className="navbar-logo">
          Patent<span>Mind</span> AI
        </div>
      </div>

      <div className="navbar-links">
        <a href="#">Home</a>
        <a href="#">Dashboard</a>
        <a href="#">About</a>
      </div>
    </nav>
  );
}

export default Navbar;
