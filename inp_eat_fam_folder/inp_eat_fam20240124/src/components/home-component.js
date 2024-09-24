import React from "react";
import LoginComponent from "./login-component";


const styles = {
  container: {
    maxWidth: "450px",
    margin: "auto",
  },
  content: {
    textAlign: "center",
    marginTop: "15px",
  },
};

const HomeComponent = () => {
  return (
    <main>
    <div style={styles.container}>
      {/* Info */}
      <div style={styles.content}>
        <h3 style={{ margin: '0px' }}>三餐費用420元</h3>
        <p style={{ marginTop: '5px', marginLeft: '0' }}>
          早餐100元/午餐160元/晚餐160元<br />
          (加點項目費用另計)
        </p>
      </div>
      <div style={styles.content}>
        <h3 style={{ margin: '0px' }}>訂餐/停餐 時間說明</h3>
        <p style={{ marginTop: '5px', marginLeft: '0' }}>
          07:30前：當日早餐開始生效<br />
          11:30前：當日午餐開始生效<br />
          16:30前：當日晚餐開始生效
        </p>
      </div>
      {/* Login 登入區塊 */}
      <LoginComponent/>
    </div>
    </main>
  );
};

export default HomeComponent;
