import { useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; //引入bootstrape
import "bootstrap/dist/js/bootstrap.bundle.min.js"; //引入JS
import { NavLink } from 'react-router-dom';
import AuthService from "../service/auth.service.js";
import { COLORS } from '../utils/color.js';
import '../styles/main.css';

const NavComponent = ({ currentUser, setCurrentUser }) => {
  const handleLogout = () => {
    AuthService.logout(); // 清空 storage
    window.alert("登出成功!現在您會被導向到首頁。");
    setCurrentUser(null);
  };

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light no-padding" style={{ borderBottom: `3px solid ${COLORS.darkGray}` }}>
        <div className="container-fluid text-gray no-padding" style={{ backgroundColor: COLORS.white }}>
          <div className="navbar-collapse justify-content-between text-black no-padding" id="navbarNav" style={{ backgroundColor: COLORS.white }}>
            <div className="navbar-nav d-flex flex-row">
              <NavLink className="nav-link text-white" activeClassName="active" to="/"></NavLink>
              {!currentUser && (
                <NavLink 
                to="/home"
                className={({ isActive }) =>
                  isActive ? 'nav_btn nav_btn_active' : 'nav_btn'
                }
                >
                手術室房間分配表
                </NavLink>
              )}
              {!currentUser && (
                <NavLink 
                to="/surgey-form"
                className={({ isActive }) =>
                  isActive ? 'nav_btn nav_btn_active' : 'nav_btn'
                }
                >
                手術紀錄
                </NavLink>
              )}
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default NavComponent;