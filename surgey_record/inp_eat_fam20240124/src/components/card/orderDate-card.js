import React, { useState, useEffect } from "react";

const OrderDateCard = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [startMeal, setStartMeal] = useState("");
  const [endMeal, setEndMeal] = useState("");
  const [data, setData] = useState([]);
  const meals = ["早餐", "午餐", "晚餐"];


  // 存進api url
  const postData = async (newData) => {
    try {
      const response = await fetch("https://localhost:3002/api/items", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);

      alert("資料已成功送出！");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // 選擇的資料轉為資料表
  const handleConfirmClick = () => {
    console.log("click");
    console.log(startDate, endDate, startMeal, endMeal);
    if (startDate && endDate && startMeal && endMeal) {
      let startMealIndex = meals.indexOf(startMeal);
      let endMealIndex = meals.indexOf(endMeal);
      let start = new Date(startDate);
      let end = new Date(endDate);
      let newData = [];
      let sid = 1;

      for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
        for (let i = startMealIndex; i < meals.length; i++) {
          newData.push({
            sid: sid.toString(),
            date: d.toISOString().split("T")[0].replace(/-/g, ""),
            meal: meals[i],
          });
          sid += 1;
        }
        startMealIndex = 0;
      }

      setData(newData);

      // Post to API
      postData(newData);
    }
  };
  return (
    <>
      {/* 日期卡片 */}
      <div className="card">
        <div className="card-body">
          <h5 className=" card-title text-center">
            選擇訂餐日期{" "}
            <span style={{ color: "gray", fontSize: "smaller" }}>
              {" "}
              {/* (select order time) */}
            </span>
          </h5>
          <div className="mb-3">
            <label className="form-label">
              開始餐點時間{" "}
              <span style={{ color: "gray", fontSize: "smaller" }}>
                {" "}
                {/* (start date) */}
              </span>
            </label>
            <input
              type="date"
              onChange={(e) => setStartDate(e.target.value)}
              className="form-control"
              id="startDate"
              name="startDate"
              required
            />
            <select
              onChange={(e) => setStartMeal(e.target.value)}
              className="form-select"
              aria-label="Default select example"
            >
              {meals.map((meal, index) => (
                <option key={index} value={meal}>
                  {meal}
                </option>
              ))}
            </select>
            <div className="form-text"></div>
          </div>
          <div className="mb-3">
            <label className="form-label">
              結束餐點時間
              <span style={{ color: "gray", fontSize: "smaller" }}>
                {" "}
                {/* (end date) */}
              </span>
            </label>
            <div className="position-relative">
              <input
                type="date"
                onChange={(e) => setEndDate(e.target.value)}
                className="form-control"
                id="endDate"
                name="endDate"
                required
              />
              <select
                onChange={(e) => setEndMeal(e.target.value)}
                className="form-select"
                aria-label="Default select example"
              >
                <option value="">請選擇結束餐點</option>
                {meals.map((meal, index) => (
                  <option key={index} value={meal}>
                    {meal}
                  </option>
                ))}
              </select>
              <div className="form-text"></div>
            </div>
          </div>
          <button type="submit" onClick={handleConfirmClick}>
            確認
          </button>
          <div
            id="formAlert"
            className="alert alert-info"
            style={{ display: "none" }}
          ></div>
        </div>
      </div>
    </>
  );
};

export default OrderDateCard;
