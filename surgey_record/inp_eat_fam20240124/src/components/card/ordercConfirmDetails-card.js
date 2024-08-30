import React from "react";

const buttonStyle = {
  backgroundColor: "#1976D2", // 你想要的颜色
  color: "white", // 文字颜色
};

const OrderComfirmDetailsCard = () => {
  return (
    <>
      {/* 下單明細確認卡片 */}
      <div className="card">
        <div className="card-body">
          <h5 className=" card-title text-center"> 請確認餐點 </h5>

          {/* confirm order details */}
          <table className="table table-striped">
            <thead>
              <tr>
                <th scope="col">日期</th>
                <th scope="col">時間</th>
                <th scope="col">項目</th>
                <th scope="col">價格</th>
                <th scope="col">編輯</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">20240120</th>
                <td>早餐</td>
                <td>稀飯</td>
                <td>＄60</td>
                <td>
                  <button className="btn btn-secondary">修改</button>
                  <button className="btn btn-danger">刪除</button>
                </td>
              </tr>
              <tr>
                <th scope="row">20240120</th>
                <td>午餐</td>
                <td>雞腿飯</td>
                <td>＄100</td>
                <td>
                  <button className="btn btn-secondary">修改</button>
                  <button className="btn btn-danger">刪除</button>
                </td>
              </tr>
              <tr>
                <th scope="row">20240120</th>
                <td>晚餐</td>
                <td>招牌飯</td>
                <td>＄90</td>
                <td>
                  <button className="btn btn-secondary">修改</button>
                  <button className="btn btn-danger">刪除</button>
                </td>
              </tr>
            </tbody>
          </table>

          {/* ----- */}
          <hr />

          {/* order total */}
          <div className="d-flex justify-content-center align-items-center">
            <label className="mx-1">總計金額：$</label>
            <input type="text" />
          </div>
        </div>
        {/* 送出訂單btn */}
        <div className="text-center my-4">
          <button style={buttonStyle} className="btn btn-block btn-lg">
            <span>送出訂單</span>
          </button>
        </div>
      </div>
    </>
  );
};

export default OrderComfirmDetailsCard;
