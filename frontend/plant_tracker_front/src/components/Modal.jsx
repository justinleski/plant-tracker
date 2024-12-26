import "bootstrap-icons/font/bootstrap-icons.css";
import { Link } from 'react-router';
import "./Modal.css"

function Modal() {

    return (
        <div className="plant-verify">
            <div>
                <h1>Is this your plant?</h1>
                {/* <h2>${plant_name}</h2> */}
            </div>

            <div className="modal-buttons">
               
                    <i className="bi bi-search"></i>
               
                
                
                    <i className="bi bi-x-lg"></i>
               
            </div>
        </div>
    )
}

export default Modal;