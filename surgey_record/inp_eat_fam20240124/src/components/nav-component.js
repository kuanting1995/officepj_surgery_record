import { useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; //引入bootstrape
import "bootstrap/dist/js/bootstrap.bundle.min.js"; //引入JS
import { Link } from "react-router-dom";
import AuthService from "/home/dev/work/inp_eat_fam_file/inp_eat_fam20240124/src/service/auth.service.js";

const NavComponent = ({ currentUser, setCurrentUser }) => {
  const handleLogout = () => {
    AuthService.logout(); // 清空 storage
    window.alert("登出成功!現在您會被導向到首頁。");
    setCurrentUser(null);
  };
  return (
    <div>
      <nav>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <div
            className="container-fluid text-white"
            style={{ backgroundColor: "#1976D2" }}
          >
            {/* 以下的修改是新增 d-lg-none class，表示在大於 lg（大型）的螢幕上隱藏，只在小螢幕上顯示 */}
            <span className="fs-5 d-lg-none">住院線上訂餐(家屬飲食) </span>
            {currentUser && (
              <span className="text-align-center d-lg-none">
                {currentUser.PAT_NAME}家屬,您好!
              </span>
            )}
            <button
              className="navbar-toggler navbar-light"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>

            <div
              className="collapse navbar-collapse justify-content-between text-white py-2"
              id="navbarNav"
              style={{ backgroundColor: "#1976D2" }}
            >
              <span className="fs-5 d-none d-lg-flex">
                住院線上訂餐(家屬飲食)
              </span>
              {currentUser && (
                <span className="text-align-center">
                  {currentUser.PAT_NAME}家屬,您好!
                </span>
              )}
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link active text-white" to="/"></Link>
                </li>

                {!currentUser && (
                  <li className="nav-item">
                    <Link className="nav-link text-white" to="/register"></Link>
                  </li>
                )}
                {!currentUser && (
                  <li className="nav-item">
                    <Link className="nav-link text-white" to="/">
                      登入
                    </Link>
                  </li>
                )}
                {currentUser && (
                  <li className="nav-item">
                    <Link className="nav-link text-white" to="/profile">
                      歷史訂單
                    </Link>
                  </li>
                )}
                {currentUser && (
                  <li className="nav-item">
                    <Link
                      onClick={handleLogout}
                      className="nav-link text-white"
                      to="/"
                    >
                      登出
                    </Link>
                  </li>
                )}
              </ul>
            </div>
          </div>
        </nav>
      </nav>
    </div>
  );
};

export default NavComponent;
