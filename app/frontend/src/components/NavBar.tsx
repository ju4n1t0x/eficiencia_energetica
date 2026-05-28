import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';

interface NavBarProps {
  onLogout: () => void;
  isAuthenticated: boolean;
}

const NavBar: React.FC<NavBarProps> = ({ onLogout, isAuthenticated }) => {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <ul className="navbar-links">
          <li>
            <NavLink to="/upload" className={({ isActive }) => `nav-button ${isActive ? 'active' : ''}`}>
              Cargar Dataset
            </NavLink>
          </li>
          <li>
            <NavLink to="/eda" className={({ isActive }) => `nav-button ${isActive ? 'active' : ''}`}>
              Análisis EDA
            </NavLink>
          </li>
          <li>
            <NavLink to="/predict" className={({ isActive }) => `nav-button ${isActive ? 'active' : ''}`}>
              Predicción
            </NavLink>
          </li>
          <li>
            <NavLink to="/docs" className={({ isActive }) => `nav-button ${isActive ? 'active' : ''}`}>
              Documentación
            </NavLink>
          </li>
          {isAuthenticated && (
            <li>
              <button className="nav-button nav-logout" onClick={onLogout}>
                Cerrar Sesión
              </button>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
