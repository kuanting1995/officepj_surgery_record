// auth.service.js 扮演服務角色, 處理跟登入有關login, logout
// react中使用axios傳送http request 到伺服器
import axios from "axios";

// post API_URL獲得response：
// {
//     "status": true,
//     "data": [
//         {
//             "INP_NO": "00387464",
//             "CHART_NO": "06778237",
//             "PAT_NAME": "楊O潘",
//             "SEX": "M",
//             "IN_DATE": "20230919",
//             "OUT_DATE": null,
//             "INP_STATUS": "True",
//             "NOW_PAY_KIND1": "000",
//             "NOW_DOC_NO1": "黃國埕",
//             "NOW_DOC_NO2": "侯秀香",
//             "NOW_STATIONNO": "05A",
//             "NOW_BEDNO": "5061",
//             "NOW_HDEPT_CODE": "CMD"
//         }
//     ],
//     "message": ""
// }

const API_URL = "https://ing-test.kfsyscc.org/fast-nutapi/api/PatInpData/";

class AuthService {
  // 登入
  async login(PAT_IDNO, BIRTHDAY) {
    try {
      const response = await axios.post(API_URL, {
        PAT_IDNO,
        BIRTHDAY,
      });

      if (response.data.status) {
        const { CHART_NO, PAT_NAME, INP_STATUS, NOW_STATIONNO } =
          response.data.data[0];
        return { CHART_NO, PAT_NAME, INP_STATUS, NOW_STATIONNO };
      } else {
        throw new Error(response.data.err || "Login failed");
      }
    } catch (error) {
      if (error.response) {
        // 若是伺服器回傳錯誤狀態碼，可以透過 error.response.status 取得
        if (error.response.status === 400) {
          // 這裡可以自行定義處理錯誤的邏輯
          // 例如，顯示伺服器回傳的錯誤訊息
          alert(error.response.data.err || "伺服器發生錯誤");
        } else if (error.response.status === 401) {
          throw new Error("帳號或密碼錯誤");
        } else {
          throw new Error("伺服器發生錯誤");
        }
      } else if (error.message === "Network Error") {
        // 這裡處理網路錯誤
        alert("網路錯誤，請檢查網路連線");
      } else {
        throw error;
      }
    }
  }

  // 登出
  logout() {
    sessionStorage.removeItem("user");
  }

  //獲取session 判斷是否登入
  getCurrentUser() {
    return JSON.parse(sessionStorage.getItem("user"));
  }
}
export default new AuthService();
