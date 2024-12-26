import "bootstrap-icons/font/bootstrap-icons.css";
import './Navbar.css'

function Navbar() {

    return (
        <nav className="navbar">
            <ul>
                <li><i className="bi bi-house"></i></li>
                <li><i className="bi bi-plus"></i></li>
                <li><i className="bi bi-card-checklist"></i></li>
                <li><i className="bi bi-person"></i></li>             
            </ul>
        </nav>
    )

}

export default Navbar;