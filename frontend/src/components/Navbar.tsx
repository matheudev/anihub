import { Fragment } from "react";
import { Link, NavLink } from "react-router-dom";

const Navbar: React.FC = () => {
    const guestLinks = () => (
        <Fragment>
            <NavLink className="nav-link active" to="/login">Login</NavLink>
            <NavLink className="nav-link active" to="/register">Register</NavLink>
        </Fragment>
    );
    return (
        <nav className="navbar navbar-expand-lg bg-body-tertiary">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Navbar</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div className="navbar-nav">
                        <NavLink className="nav-link active" to="/">Home</NavLink>
                    </div>
                    { guestLinks() }
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
