import React,{useEffect,useState} from "react";
import axios from 'axios';
import data from '../jsondata/data.json';
// import '../styles/main.css';
import '../styles/surgerycalendar.css';
import { COLORS } from "../utils/color";



const SurgeryCalendar = () => {

  /* 獲取醫生排班日曆*/
 
  const [usernames, setUsernames] = useState([]);



  //標題 header_date = ["2024/9/16（一）",...]
  const formatOptions = {year: 'numeric', month: 'numeric', day: 'numeric', weekday: 'narrow'}
  let header_date = Array.from ({length: 5}, (_, i) => {
    let date = new Date();
    date.setDate(date.getDate()+ i);
    let formatteddate = date.toLocaleDateString('zh-TW',formatOptions);
    return formatteddate;
  });
  // console.log('header_date',header_date);

  // 標題 header_room = ["R1"," ","","","R2","","","","R3","","","","R4",....] 寫死
  let header_room = []; 
  for (let i = 1; i <= 10; i++) {
      header_room.push(`R${i}`);
      for (let j = 0; j < 3; j++){
        header_room.push(" ");
      }
    }
  // console.log('header_room',header_room);

  //標題 header_noon = ["AM","AM","PM","PM","AM","AM","PM","PM"....] 寫死
  let header_noon = [];
  for (let i = 0; i < 10; i++){
    header_noon.push("AM","AM","PM","PM");
   }
  // console.log('header_noon',header_noon);

  

  // 1.抓出1個月資料
  const fetchData = async () => {
    let today = new Date();
    let year = today.getFullYear();
    let month = ("0" + (today.getMonth() + 1)).slice(-2);
    let day = ("0" + today.getDate()).slice(-2);

    const response = await axios.post('https://ing-test.kfsyscc.org/fast-oprapi/api/getOPRSch', {
      "DR_CODE": "",
      "BDATE": `${year}${month}${day}`
    });

    let usernamesForWeek = Array.from({ length: 4 }, (_, i) => {
      let date = new Date();
      date.setDate(date.getDate() + i);
      let formatteddate = `${date.getFullYear()}${("0" + (date.getMonth() + 1)).slice(-2)}${("0" + date.getDate()).slice(-2)}`;

      let filteredData = response.data.data.filter((v) => v.REG_DATE === formatteddate);

      let defaultData = Array.from({ length: 10 }, (_, i) => {
        let room = "R" + (i + 1);
        return {
          room: room,
          data: Array.from({ length: 4 }, (_, j) => {
            return {
              noon: j.toString(),
              userName: ""
            };
          })
        };
      });

      filteredData.forEach(item => {
        let roomIndex = defaultData.findIndex(data => data.room === item.ROOM);
        let noonIndex = defaultData[roomIndex].data.findIndex(data => data.noon === item.NOON);
        defaultData[roomIndex].data[noonIndex].userName = item.USER_NAME;
      });

      return defaultData;
    });
  console.log("usernamesForWeek",usernamesForWeek);
  console.log("usernames",usernamesForWeek[0][0]['data'][0]['userName']);
 
  setUsernames(usernamesForWeek);




  };

  useEffect(()=>{
      fetchData();
    },[]);

  
  return (
    <main>
      <div>
      <div className="d-flex flex-column align-items-center justify-content-center pt-3">
        
        {/* button week */}
        <div className="d-flex justify-content-between w-100">
          <button className="btn btn-week" >{"<-"}上週</button>
          <h4 className="text-center" style={{color: COLORS.black}}>手術室房間分配表</h4>
          <button className="btn-week">下週{"->"}</button>
        </div>

           {/* table zone */}
        <table style={{overflow: 'auto', height: '100vh'}} className="table table-bordered table-sm w-100">
          <thead className="thead-sticky">
            <tr>
               <th style={{width:'5%'}}>手術室</th>
               <th style={{width:'5%'}}></th>
              {header_date.map((value, index) => (
                <th style={{width:'10%'}} key={index}>{value}</th>
              ))}
            </tr>
          </thead>
          <tbody>
        
            <tr>
              <td style={{ fontStyle: 'bold' }}>R1</td>
              <td style={{ color: item.noon === 'AM' ? '#B22222' : '#3c763d', fontWeight: 'bold' }}>{item.noon}</td>
              <td><a href="#" className="link-button">{item.userName}</a></td>
                
            </tr>
      </tbody> 
        </table>
      </div>
    </div>
    </main>
    
  );
};

export default SurgeryCalendar;