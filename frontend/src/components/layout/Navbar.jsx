import { NavLink } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

const privateLinks = [
  { label: "Dashboard", to: "/dashboard" },
  { label: "Resume", to: "/resume" },
  { label: "Generate Interview", to: "/generate-interview" },
  { label: "History", to: "/history" },
];

const publicLinks = [
  { label: "Login", to: "/login" },
  { label: "Signup", to: "/signup" },
];

function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header className="navbar">
      <NavLink className="navbar__brand" to={isAuthenticated ? "/dashboard" : "/login"}>
        InterviewAI
      </NavLink>

      <nav className="navbar__links" aria-label="Main navigation">
        {isAuthenticated ? (
          <>
            <div className="navbar__group">
              {privateLinks.map((item) => (
                <NavLink key={item.to} className="navbar__link" to={item.to}>
                  {item.label}
                </NavLink>
              ))}
            </div>

            <div className="navbar__group navbar__group--auth">
              <button className="button button--secondary" onClick={logout}>
                Logout
              </button>
            </div>
          </>
        ) : (
          <div className="navbar__group navbar__group--auth">
            {publicLinks.map((item) => (
              <NavLink key={item.to} className="navbar__link" to={item.to}>
                {item.label}
              </NavLink>
            ))}
          </div>
        )}
      </nav>
    </header>
  );
}

export default Navbar;