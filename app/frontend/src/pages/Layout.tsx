import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Footer from "../components/Footer";
import NavBar from "../components/NavBar"
import EdaPage from "./EdaPage"
import CargaPage from "./CargaPage"
import LoginComponent from "../components/LoginComponent"
import './Layout.css'; 

function Layout() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    return (
        <div className="layout">
            <main className="layout-content">
                <header className="page-header">
                    <NavBar />
                </header>
                
                <section className="page-body">
                    <Routes>
                        {/* Redirección por defecto al dashboard */}
                        <Route path="/" element={<Navigate to="/eda" replace />} />
                        <Route path="/eda" element={<EdaPage />} />
                        <Route 
                            path="/upload" 
                            element={
                                isAuthenticated 
                                ? <CargaPage /> 
                                : <LoginComponent onLogin={() => setIsAuthenticated(true)} />
                            } 
                        />
                        
                        {/* Placeholders para las otras rutas */}
                        <Route path="/predict" element={<div className="center"><h1>Próximamente: Predicción</h1></div>} />
                        <Route path="/docs" element={<div className="center"><h1>Próximamente: Documentación</h1></div>} />
                    </Routes>
                </section>
            </main>

            <footer className="layout-footer">
               <Footer/>
            </footer>
        </div>
    )
}

export default Layout