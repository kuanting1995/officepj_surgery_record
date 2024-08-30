import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; //引入bootstrape
import "bootstrap/dist/js/bootstrap.bundle.min.js"; //引入JS
import { useNavigate } from "react-router-dom";
import AuthService from "/home/dev/work/inp_eat_fam_file/inp_eat_fam20240124/src/service/auth.service.js";

// css
const buttonStyle = {
  backgroundColor: "#1976D2", // 你想要的颜色
  color: "white", // 文字颜色
};

const LoginComponent = ({ currentUser, setCurrentUser }) => {
  // 使用navigate
  const nagivate = useNavigate();

  let [patID, setPatId] = useState("");
  let [patBirthday, setpatBirthday] = useState("");
  const [patIDError, setPatIDError] = useState("");
  const [patBirthdayError, setPatBirthdayError] = useState("");
  const [alert, setAlert] = useState({ message: "", type: "", show: false });
  const handlePatID = (e) => {
    setPatId(e.target.value);
  };
  const handlePatBirthday = (e) => {
    setpatBirthday(e.target.value);
  };

  const handleLogin = async (event) => {
    try {
      event.preventDefault();

      setPatIDError("");
      setPatBirthdayError("");

      let isPass = true;

      if (patID.length === 0) {
        isPass = false;
        setPatIDError("請輸入身分證");
      } else if (!/^[A-Z]/.test(patID)) {
        isPass = false;
        setPatIDError("第一個英文字請大寫");
      } else if (!/^[A-Z][0-9]{9}$/.test(patID)) {
        isPass = false;
        setPatIDError("請輸入有效的身分證");
      }

      if (!/^[0-9]{8}$/.test(patBirthday)) {
        isPass = false;
        setPatBirthdayError("請輸入有效生日");
      }

      if (isPass) {
        let response = await AuthService.login(patID, patBirthday);
        sessionStorage.setItem("user", JSON.stringify(response));
        showAlert("登入成功! 進入訂餐...", "success");
        nagivate("/ordering");
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
      showAlert("身份證或生日輸入錯誤，或此非住院中病人。", "danger");
    }
  };

  const showAlert = (message, type) => {
    setAlert({ message, type, show: true });
    // setTimeout(() => {
    //   setAlert({ message: "", type: "", show: false });
    // }, 5000);
  };
  return (
    <>
      <div style={{ padding: "3rem" }} className="col-md-12">
        {alert.show && (
          <div id="formAlert" className={`alert alert-${alert.type}`}>
            {alert.message}
          </div>
        )}
        <div>
          <div className="form-group">
            <label>病人身份證:</label>
            <input
              placeholder="A123XXXXXX"
              onChange={handlePatID}
              type="text"
              className={`form-control ${patIDError ? "border-danger" : ""}`}
              name="patID"
            />
            <div className="form-text" style={{ color: "red" }}>
              {patIDError}
            </div>
          </div>
          <br />
          <div className="form-group">
            <label>病人生日:</label>
            <input
              placeholder="19800120"
              onChange={handlePatBirthday}
              type="text"
              className={`form-control ${patBirthdayError ? "border-danger" : ""}`} // Add border if there is an error
              name="patBirthday"
            />
            <div className="form-text" style={{ color: "red" }}>
              {patBirthdayError}
            </div>
          </div>
          <br />
          <div className="form-group text-center">
            <button
              onClick={handleLogin}
              style={buttonStyle}
              className="btn btn-block btn-lg"
            >
              <span>開始訂餐</span>
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginComponent;
