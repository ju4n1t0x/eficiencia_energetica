import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';

const NavBar: React.FC = () => {
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
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
