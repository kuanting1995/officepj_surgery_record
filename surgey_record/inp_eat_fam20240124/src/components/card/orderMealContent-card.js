import { useState, useEffect } from "react";

const buttonStyle = {
  backgroundColor: "#1976D2", // 你想要的颜色
  color: "white", // 文字颜色
};

const OrderMealContentCard = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [foodOptions, setFoodOption] = useState([]);
  const API_URL = "https://ing-test.kfsyscc.org/fast-nutapi/api/foodOptions";

  // 抓取三餐資訊
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(API_URL);
      const data = await response.json();
      setFoodOption(data);
    };
    fetchData();
  }, []);

  // 顯示菜單內容
  const handleShowMenu = (event) => {
    event.preventDefault();
    setShowMenu(!showMenu);
  };

  return (
    <>
      {/* 餐點選擇卡片 */}
      <div className="card">
        <div className="card-body">
          <h5 className=" card-title text-center">
            選擇餐點內容{" "}
            <span style={{ color: "gray", fontSize: "smaller" }}>
              {" "}
              {/* (select order time) */}
            </span>
          </h5>
          <form name="form1" onsubmit="checkForm(event)" novalidate>
            {/* 早餐radio */}
            <div className="mb-3">
              <label htmlFor="lunch" className="form-label">
                早餐
                <span style={{ color: "gray", fontSize: "smaller" }}>
                  {/* (end date) */}
                </span>
              </label>
              <div className="position-relative">
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioLunch"
                    id="lunch1"
                  />
                  <label className="form-check-label" htmlFor="lunch1">
                    稀飯
                  </label>
                </div>
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioLunch"
                    id="lunch2"
                    checked
                  />
                  <label className="form-check-label" htmlFor="lunch2">
                    吐司
                  </label>
                </div>
                <div className="form-text"></div>
              </div>
            </div>
            {/*午餐radio */}
            <div className="mb-3">
              <label htmlFor="lunch" className="form-label">
                午餐
                <span style={{ color: "gray", fontSize: "smaller" }}>
                  {/* (end date) */}
                </span>
              </label>
              <div className="position-relative">
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioLunch"
                    id="lunch1"
                  />
                  <label className="form-check-label" htmlFor="lunch1">
                    雞腿便當
                  </label>
                </div>
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioLunch"
                    id="lunch2"
                    checked
                  />
                  <label className="form-check-label" htmlFor="lunch2">
                    招牌便當
                  </label>
                </div>
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioLunch"
                    id="lunch3"
                  />
                  <label className="form-check-label" htmlFor="lunch3">
                    素食便當
                  </label>
                </div>
                <div id="seepass" className="col">
                  <i
                    id="seepass1"
                    style={{ display: "none", color: "gray" }}
                    className="fa-solid fa-eye"
                  ></i>
                  <i
                    id="seepass2"
                    style={{ display: "none", color: "gray" }}
                    className="fa-solid fa-eye-slash"
                  ></i>
                </div>
                <div className="form-text"></div>
              </div>
            </div>
            {/* 晚餐radio */}
            <div className="mb-3">
              <label htmlFor="dinner" className="form-label">
                晚餐
                <span style={{ color: "gray", fontSize: "smaller" }}>
                  {/* (end date) */}
                </span>
              </label>
              <div className="position-relative">
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioDinner"
                    id="dinner1"
                  />
                  <label className="form-check-label" htmlFor="dinner1">
                    雞腿便當
                  </label>
                </div>
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioDinner"
                    id="dinner2"
                    checked
                  />
                  <label className="form-check-label" htmlFor="dinner2">
                    招牌便當
                  </label>
                </div>
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="radio"
                    name="flexRadioDinner"
                    id="dinner3"
                  />
                  <label className="form-check-label" htmlFor="dinner3">
                    素食便當
                  </label>
                </div>

                <div className="form-text"></div>
              </div>
            </div>

            {/* 查看餐點細節btn */}
            <div className="text-center my-4">
              <button
                className="btn btn-secondary btn-lg"
                onClick={handleShowMenu}
              >
                <span>餐點內容介紹</span>
              </button>
            </div>
            {showMenu && (
              <div>
                <h2>餐點資訊</h2>
                <div className="row">
                  {[...Array(4)].map((_, index) => (
                    <div className="col-6 col-md-3" key={index}>
                      <div className="card">
                        <img
                          src="https://obs.line-scdn.net/0hQqO40GujDl5yTRkzo4VxCVYbDTFBIR1dFntfTCUoNgBfekkJHn4TMAAaV25cfktbTiMVPlFNVGoafB0NSCpDMQA/w644"
                          className="card-img-top"
                          alt="餐點圖片"
                        />
                        <div className="card-body">
                          <p className="card-text">雞腿便當...</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </form>
        </div>
      </div>
    </>
  );
};

export default OrderMealContentCard;
