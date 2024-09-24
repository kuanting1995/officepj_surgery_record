import React from "react";

const OrderRecordCard = () => {
  return (
    <>
      {/* 訂餐紀錄卡片 */}
      <div className="card">
        <div className="card-body">
          <h5 className=" card-title text-center"></h5>
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
        </div>
      </div>
    </>
  );
};

export default OrderRecordCard;
