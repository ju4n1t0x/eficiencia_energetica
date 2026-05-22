import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; {currentYear} Eficiencia Energética. Todos los derechos reservados al <strong>Grupo 34</strong></p>
      </div>
    </footer>
  );
};

export default Footer;