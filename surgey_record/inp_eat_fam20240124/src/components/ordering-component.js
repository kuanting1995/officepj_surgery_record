import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; //引入bootstrape
import "bootstrap/dist/js/bootstrap.bundle.min.js"; //引入JS
import OrderDateCard from "./card/orderDate-card";
import OrderMealContentCard from "./card/orderMealContent-card";
import OrderComfirmDetailsCard from "./card/ordercConfirmDetails-card";
import OrderRecordCard from "./card/record-card";

const buttonStyle = {
  backgroundColor: "#1976D2", // 你想要的颜色
  color: "white", // 文字颜色
};

const OrderingComponent = () => {
  const [data, setData] = useState("");
  const [showComponent, setShowComponent] = useState(false);

  const handleConfirmMeal = () => {
    console.log("clicked");
    setShowComponent(true);
  };
  return (
    <>
      <div className="container">
        <div className="">
          <div className="row align-items-center">
            <div className="col-lg-6 mx-auto">
              {/*-- 訂餐紀錄區 --*/}
              <h2 className="text-center my-4">-- 訂餐紀錄 --</h2>
              {/* 訂餐紀錄卡片 */}
              {/* {!data && <h3>尚未點餐..</h3>} */}
              {!data ? (
                <h6 className="text-center">尚未有訂餐紀錄..</h6>
              ) : (
                <OrderRecordCard />
              )}

              {/* --開始訂餐區-- */}
              <h2 className="text-center my-4">-- 開始訂餐 --</h2>
              {/* 日期選擇卡片 */}
              <OrderDateCard />

              {/* 餐點選擇卡片 */}
              <OrderMealContentCard
                showComponent={showComponent}
                setShowComponent={setShowComponent}
              />
              <div className="text-center">
                {" "}
                <button
                  style={buttonStyle}
                  className="btn btn-block btn-lg"
                  onClick={handleConfirmMeal}
                >
                  下一步
                </button>
              </div>

              {/* 下單明細確認卡片 */}
              {showComponent && <OrderComfirmDetailsCard />}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default OrderingComponent;
