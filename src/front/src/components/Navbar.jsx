import { Link } from "react-router-dom";

export const Navbar = () => {
  return (
    <nav className="navbar navbar-dark bg-dark px-4">
      <Link className="navbar-brand" to="/">
        Alenya
      </Link>

      <div className="d-flex gap-3">
        <Link className="btn btn-outline-light" to="/login">
          Login
        </Link>

        <Link className="btn btn-primary" to="/register">
          Register
        </Link>
      </div>
    </nav>
  );
};