import React, { useState } from "react";
import '../styles/main.css';
import { COLORS } from "../utils/color";
import Sidebar from "./sidebar";
import { auto } from "@popperjs/core";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLightbulb } from '@fortawesome/free-solid-svg-icons';


const SurgeryForm = () => {
  const [selectedButton, setSelectedButton] = useState("術前");

  const handleArticleButtonClick = (button) => {
    setSelectedButton(button);
    console.log(selectedButton); // 注意：由於狀態更新可能是非同步的，這裡可能無法立即顯示新的狀態
  };

  const renderContent = () => {
    switch (selectedButton) {
      case "術前":
        return (
          <div>
            {/* 術前表格內容 */}
            123
          </div>
        );
      case "術後":
        return (
          <div>
            {/* 術後表格內容 */}456
          </div>
        );
      case "其他":
        return (
          <div>
            {/* 術前表格內容 */}789
          </div>
        );
    }
  };

  return <>
  <div style={{ display: "flex", justifyContent: "space-between", height: 'auto', maxHeight: '100vh'}}>
    <div className="sidebar">
        <Sidebar/>
    </div>
    <div className="pt-3 mx-4" style={{ width: '88%'}}>
    <h4 className="text-center" style={{color: COLORS.black}}>手術紀錄</h4>
    <div className="d-flex justify-content-end">
    <button className="crud-btn">查詢</button>
    <button className="crud-btn">新增</button>
    <button className="crud-btn">修改</button>
    <button className="crud-btn">刪除</button>
    </div>
      {/* <!-- 正式FORM --> */}
      <form className="formStyle"  >
              <div
                className="row w-80 py-3"
                style={{ backgroundColor: COLORS.lightgray, color: COLORS.black, fontWeight: 'bold'}}>
              {/* 表格第一區塊 */}
              <div className="col-md-6">
                <div className="row firstrow">
                   {/* <!--第1行-1 --> */}
                 <div className="d-flex justify-content-left col-md-5">
                  <div className="col-3 align-self-center">主刀醫生</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>D0009</option>
                      <option value="1">腫內基金</option>
                      <option value="2">病房差額補助</option>
                      <option value="3">微創手術補助</option>
                      <option value="4">微創手術補助</option>
                      <option value="5">詠珂基金</option>
                      <option value="6">乳癌手術凝合劑專案</option>
                      <option value="7">肝癌藥物基金</option>
                      <option value="8">兒科緊急救助基金</option>
                      <option value="9">其他</option>
                    </select>
                  </div>
                  <div style={{color: COLORS.darkBlue}} className="col-3 align-self-center px-1">陳啟明</div>
                </div>
                {/* <!-- 第1行-2 --> */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="theader col-2 align-self-center">
                    科別
                  </div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>SRG</option>
                      <option value="1">腫內基金</option>
                    </select>
                  </div>
                  <div className="col-5 align-self-center px-1">一般外科</div>
                </div>
                {/* <!-- 第1行-3 --> */}
                <div className="d-flex justify-content-left col-md-3">
                  <div className="theader col-3 align-self-center">
                    索引
                  </div>
                  <div className="flex-fill">
                    <input
                      className="form-control me-2"
                      type="text"
                      name="valueC"
                      placeholder="60001"
                    />
                    <div className="form-text"></div>
                  </div>
                </div>
                </div>
                <div className="row secondrow">
                   {/* <!--第2行-1 --> */}
                 <div className="d-flex justify-content-left col-md-4 ">
                  <div className="col-4  align-self-center">手術日期</div>
                  <div className="flex-fill align-self-center">
                    <input
                      style={{ width: "264" }}
                      name="treatmentStartDate"
                      type="date"
                    />                  
                  </div>
                  </div>
                  {/* <!--第2行-2--> */}
                  <div className="d-flex justify-content-left col-md-3">
                  <div className="theader col-4 align-self-center">
                    手術室
                  </div>
                  <div className="flex-fill align-self-center">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>1</option>
                      <option value="1">2</option>
                    </select>
                  </div>
                  <div style={{color: COLORS.darkBlue}} className="col-4 align-self-center px-1">R1</div>
                  
                </div>
               
                
                {/* <!--第2行-3 --> */}
                
                <div className="d-flex justify-content-left col-md-3">
                  <div className="theader col-3 align-self-center">
                    午別
                  </div>
                  <div className="flex-fill align-self-center">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>0</option>
                      <option value="1">2</option>
                    </select>
                  </div>
                  <div style={{color: COLORS.darkBlue}} className="col-4 align-self-center px-1">上午</div>
                </div>
                <div className="flex-wrap justify-content-left col-md-2">
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"/>
                <label class="form-check-label" for="flexCheckDefault">
                  暫排
                </label>
                </div>
                <div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked/>
                <label class="form-check-label" for="flexCheckChecked">
                 刪除
                </label>
                </div>
                </div>
                </div>
             
               <div className="row thirdrow justify-content-between">
                 {/* <!-- 第3行-1 --> */}
                 <div className="d-flex col-md-5 ">
                  <div className="theader col-3 text-left align-self-center">
                    {" "}
                    病例號碼
                  </div>
                  <div className="col-5">
                    <input
                      className="form-control me-1"
                      type="text"
                      name="name"
                      id="name"
                      placeholder="Q12345678"
                    />
                    <div className="form-text"></div>
                  </div>
                  <div className="col-4">
                    <input
                      className="form-control me-2"
                      type="text"
                      name="name"
                      id="name"
                      placeholder="王小明"
                    />
                    <div className="form-text"></div>
                  </div>
                </div>
                {/* <!-- 第3行-2 --> */}
                <div className="d-flex justify-content-left col-md-2 ">
                  <div className="theader col-4 text-left align-self-center">
                    性別
                  </div>
                  <div>
                    <input
                      className="form-control me-2 mx-1"
                      type="text"
                      name="name"
                      id="name"
                      placeholder="女"
                    />
                    <div className="form-text"></div>
                  </div>
                </div>
                {/* <!-- 第3行-3 --> */}
                <div className="d-flex justify-content-left col-md-2 ">
                  <div className="theader col-4 text-left align-self-center">
                    年齡
                  </div>
                  <div>
                    <input
                      className="form-control me-2 mx-1"
                      type="text"
                      name="name"
                      id="name"
                      placeholder="50"
                    />
                    <div className="form-text"></div>
                  </div>
                </div>
                {/* <!-- 第3行-4 --> */}
                <div className="d-flex justify-content-left col-md-2 ">
                  <div className="theader col-4 text-left align-self-center">
                    身份
                  </div>
                  <div>
                    <input
                      className="form-control me-2 mx-1"
                      type="text"
                      name="name"
                      id="name"
                      placeholder="000"
                    />
                    <div className="form-text"></div>
                  </div>
                </div>
               </div>
                {/* 分頁按鈕 */}
                <div>
                <button type="button" className={`article-btn ${selectedButton === '術前' ? 'selected' : ''}`} onClick={()=>handleArticleButtonClick('術前')} >術前</button>
                <button type="button" className={`article-btn ${selectedButton === '術後' ? 'selected' : ''}`} onClick={()=>handleArticleButtonClick('術後')} >術後</button>
                <button type="button" className={`article-btn ${selectedButton === '其他' ? 'selected' : ''}`} onClick={()=>handleArticleButtonClick('其他')} >其他</button>
                </div>
              
                <div className="row fourthrow pt-3" style={{borderTop: '1px solid #828282'}}>
                     {/* <!-- 第4行-1 --> */}
                     {renderContent()}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-6 align-self-center">預定時間</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>0830</option>
                      <option value="1">腫內基金</option>
                      <option value="2">病房差額補助</option>
                      <option value="3">微創手術補助</option>
                      <option value="4">微創手術補助</option>
                      <option value="5">詠珂基金</option>
                      <option value="6">乳癌手術凝合劑專案</option>
                      <option value="7">肝癌藥物基金</option>
                      <option value="8">兒科緊急救助基金</option>
                      <option value="9">其他</option>
                    </select>
                  </div>
                </div>
                {/* 第4行-2  */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-3 align-self-center">種類</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>住院</option>
                      <option value="1">腫內基金</option>
                      <option value="2">病房差額補助</option>
                      <option value="3">微創手術補助</option>
                      <option value="4">微創手術補助</option>
                      <option value="5">詠珂基金</option>
                      <option value="6">乳癌手術凝合劑專案</option>
                      <option value="7">肝癌藥物基金</option>
                      <option value="8">兒科緊急救助基金</option>
                      <option value="9">其他</option>
                    </select>
                  </div>
                </div>
                 {/* 第4行-3  */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-6 align-self-center">麻醉等級(ASA)</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected></option>
                      <option value="1">腫內基金</option>
                      <option value="2">病房差額補助</option>
                      <option value="3">微創手術補助</option>
                      <option value="4">微創手術補助</option>
                      <option value="5">詠珂基金</option>
                      <option value="6">乳癌手術凝合劑專案</option>
                      <option value="7">肝癌藥物基金</option>
                      <option value="8">兒科緊急救助基金</option>
                      <option value="9">其他</option>
                    </select>
                  </div>
                </div>
                </div>

                <div className="row fifthrow pt-1">
                   {/* <!-- 第5行-1 --> */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-6 align-self-center">預估完成時間</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>0830</option>
                    </select>
                  </div>
                </div>
                {/* 第5行-2  */}
                <div className="d-flex justify-content-left col-md-3">
                  <div className="col-4 align-self-center">床號</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>住院</option>
                      <option value="1">腫內基金</option>
                      <option value="2">病房差額補助</option>
                      <option value="3">微創手術補助</option>
                      <option value="4">微創手術補助</option>
                      <option value="5">詠珂基金</option>
                      <option value="6">乳癌手術凝合劑專案</option>
                      <option value="7">肝癌藥物基金</option>
                      <option value="8">兒科緊急救助基金</option>
                      <option value="9">其他</option>
                    </select>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-3">
                </div>
                </div>

                <div className="row sixthrow pt-1">
                {/* <!-- 第6行-1 --> */}
                 <div className="d-flex justify-content-left col-md-4">
                  <div className="col-6 align-self-center">會診醫生1</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>0830</option>
                    </select>
                  </div>
                </div>
                {/* 第6行-2  */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-4 align-self-center">會診醫生2</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>住院</option>
                      <option value="1">腫內基金</option>
                      <option value="2">病房差額補助</option>
                      <option value="3">微創手術補助</option>
                      <option value="4">微創手術補助</option>
                      <option value="5">詠珂基金</option>
                      <option value="6">乳癌手術凝合劑專案</option>
                      <option value="7">肝癌藥物基金</option>
                      <option value="8">兒科緊急救助基金</option>
                    </select>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-3">
                </div>
                </div>

                <div className="row seventhrow pt-1">
                {/* <!-- 第7行-1 --> */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-6 align-self-center">麻醉方法</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>MA+PVB</option>
                    </select>
                  </div>
                </div>
                {/* 第7行-2  */}
                <div className="d-flex justify-content-left col-md-2">
                  <div className="col-6 align-self-center">轉ICU</div>
                  <input className="col-1 form-control me-2" /><span className="align-self-center">天</span>
                </div>
                <div className="d-flex justify-content-left col-md-3">
                </div>
                </div>
                <div className="row eighthrow py-1">               
                 {/* <!-- 第8行-1 --> */}
                 <div className="d-flex justify-content-left col-md-4">
                  <div className="col-6 align-self-center">手術臥位</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>SUPINE</option>
                    </select>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-4">
                <input className="form-control"/>
                </div>
                <div className="d-flex justify-content-left col-md-4">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"/>
                  <label class="form-check-label pe-2" style={{color: COLORS.darkBlue}} for="flexCheckDefault">
                   需報告否 
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked/>
                  <label class="form-check-label" style={{color: COLORS.darkBlue}} for="flexCheckChecked">
                   完成報告否
                  </label>
                </div>
                </div>
                {/* 第8行-2  */}
                <div className="d-flex justify-content-left col-md-3">
                </div>
                <div className="d-flex justify-content-left col-md-3">
                </div>
                </div>
               {/*FRAME ZONE */}
               <div className="frame-zone pt-2">
                 {/* <!-- 第9行-1 --> */}
                <div className="d-flex justify-content-left col-md-4">
                  <div className="col-5 align-self-center">預估失血量</div>
                  <div className="flex-fill">
                    <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>{"<"}50CC</option>
                    </select>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-3 pt-1">
                </div>
                <div className="d-flex justify-content-left col-md-3">
                </div>
                {/* 第10行-1  */}
                <div className="d-flex justify-content-left col-md-4 pt-1">
                  <div className="col-5 align-self-center">備血</div>
                  <div class="d-flex justify-content-start">
                  <div class="form-check pe-2">
                  <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1"/>
                  <label class="form-check-label" for="flexRadioDefault1">
                    需要
                  </label>
                </div>
                <div class="form-check ">
                  <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked/>
                  <label class="form-check-label" for="flexRadioDefault2">
                   不需要
                  </label>
                </div>
                  </div>
                  
                </div>
                {/* <!-- 第11行 --> */}
                <div className="d-flex justify-content-between align-items-center col-md-12 pt-1">
                  <div className="col-1 align-self-center">血品</div>
                  <div class="col-2 d-flex justify-content-start align-items-center ">
                  <span className="px-1">PRBC</span><input className="form-control"/><span className="ps-1">U</span>
                  </div>
                  <div class="col-2 d-flex justify-content-start align-items-center">
                  <span className="px-1">FFP</span><input className="form-control"/><span className="ps-1">U</span>
                  </div>
                  <div class="col-2 d-flex justify-content-start align-items-center">
                  <span className="px-1">PLT</span><input className="form-control"/><span className="ps-1">U</span>
                  </div>
                  <div class="col-2 d-flex justify-content-start align-items-center">
                  <span className="px-1">PH</span><input className="form-control"/><span className="ps-1">U</span>
                  </div>
                  <div className="mx-1"></div>
                </div>
                {/* <!-- 第12行 --> */}
                <div className="d-flex justify-content-left align-items-center col-md-12 pt-1">
                <div className="col-1 mx-3"></div>
                  <div class="col-2 d-flex justify-content-start align-items-center ">
                  <span className="ps-1 pe-4">WB</span><input className="form-control"/><span className="ps-1">U</span>
                  </div>
                  <div class="col-8 d-flex justify-content-start align-items-center ps-4"><span className="px-2"></span>
                  <span className="col-1">其他</span><input className="form-control"/>
                  </div>
                  <div class="col-2 d-flex justify-content-start align-items-center">
                  </div>
                  <div className="mx-1"></div>
                  </div>
               </div>
               </div>
              
               {/*表格第二區塊  */}
               <div className="col-md-6 px-5">
                {/* {/* article-btn2 */}
                <button className="article-btn2">術前診斷</button>
                <button className="mx-1 article-btn4"><FontAwesomeIcon icon={faLightbulb} style={{color: COLORS.black, backgroundColor: COLORS.Yellow}} />門診診斷</button>
                <button className="article-btn4"><FontAwesomeIcon icon={faLightbulb} style={{color: COLORS.black, backgroundColor: COLORS.Yellow}} />I9轉 I10</button>
  
                 {/* <!-- zone2第1行 --> */}
                 <div className="d-flex justify-content-left col-md-4 align-items-center pt-1">
                  <div className="col-4 align-self-center me-1">術前診斷1</div>
                  <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>SUPINE</option>
                    </select>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>
                  {/* <!-- zone2第2行 --> */}
                  <div className="d-flex justify-content-left col-md-4 align-items-center pt-1">
                  <div className="col-4 align-self-center me-1">術前診斷2</div>
                  <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>SUPINE</option>
                    </select>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>

                 {/* <!-- zone2第3行 --> */}
                 <div className="d-flex justify-content-left col-md-8 align-items-center pt-1">
                  <div className="col-2 align-self-center me-1">*術前診斷</div>
                  <div class="input-group">
                  <textarea class="form-control" aria-label="With textarea"></textarea>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>

                {/* {/* article-btn2*/}
                <button className="article-btn2">術前術式</button>
                 {/* <!-- zone3第1行 --> */}
                 <div className="d-flex justify-content-left col-md-4 align-items-center pt-1">
                  <div className="col-4 align-self-center me-1">預定主術1</div>
                  <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>SUPINE</option>
                    </select>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>
                  {/* <!-- zone3第2行 --> */}
                  <div className="d-flex justify-content-left col-md-4 align-items-center pt-1">
                  <div className="col-4 align-self-center me-1">預訂主術2</div>
                  <select
                      className="form-select"
                      aria-label="Default select example"
                    >
                      <option selected>SUPINE</option>
                    </select>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>

                <div className="row">
                {/* <!-- zone3第3行 1 --> */}
                <div className="d-flex justify-content-left col-md-8 align-items-center pt-1">
                  <div className="col-2 align-self-center me-1">*預訂術法</div>
                  <div class="input-group">
                  <textarea class="form-control" aria-label="With textarea"></textarea>
                  </div>
                </div>

                {/* <!-- zone3第3行 2 --> */}
               <div className="col-md-4 d-flex flex-column justify-content-left my-2 align-items-center">
                <div className="form-check">
                <input className="form-check-input" type="checkbox" value="" id="flexCheckDefault"/>
                <label className="form-check-label" style={{color: COLORS.darkBlue}} htmlFor="flexCheckDefault">
                  術式帶入診療計劃書
                </label>
               </div>
               <div className="form-check">
               <input className="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked/>
               <label className="form-check-label" style={{color: COLORS.Green}} htmlFor="flexCheckChecked">
                達文西手術排程通知
                </label>
              </div>
            </div>
           </div>
                {/* <!-- zone3第4行 --> */}
                <div className="d-flex justify-content-left col-md-8 align-items-center pt-1">
                  <div className="col-2 align-self-center"></div>
                  <div class="">
                  <button className="article-btn4">PVB+TIVA+MMA</button>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>
                {/* <!-- zone3第5行 --> */}
                <div className="d-flex justify-content-left col-md-8 align-items-center pt-1">
                  <div className="col-2 align-self-center">備註</div>
                  <div class="input-group">
                  <textarea class="form-control" aria-label="With textarea"></textarea>
                  </div>
                </div>
                <div className="d-flex justify-content-left col-md-9 align-items-center">
                </div>
               </div>









                {/* submitBTN */}
                <div className="d-flex flex-row-reverse mt-3">
                  <button type="submit" className="btn-submit" >
                    送出
                  </button>
                </div>
              </div>
            </form>
    </div>
  </div>
  </>
};

export default SurgeryForm;
