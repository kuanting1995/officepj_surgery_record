import { useState, useContext, useEffect } from 'react'
import { useNavigate, NavLink } from 'react-router-dom'
import '../styles/memberPage.css'
import '../styles/memberPagefornav.css'
import{ COLORS } from '../utils/color'


function Sidebar(props) {
  
  return (
    <>
        <div className='sidebar-nav-group' style={{backgroundColor:COLORS.lightgray,height:'100vh'}}>
        <NavLink
            to="/home"
            className={({ isActive }) =>
              isActive ? 'sidebar_btn  sidebar_btn_active' : 'sidebar_btn'
            }
          >
            手術室房間分配表
          </NavLink>
          <NavLink
            to="/surgey-form"
            className={({ isActive, isPending }) =>
              isActive ? 'sidebar_btn sidebar_btn_active' : 'sidebar_btn'
            }
          >
            手術紀錄
          </NavLink>
          <NavLink
            to="/articles/member/postEd"
            className={({ isActive }) =>
              isActive ? 'sidebar_btn  sidebar_btn_active' : 'sidebar_btn'
            }
          >
            
          </NavLink>
          <NavLink
            to="/member_page/membercoupon_list"
            className={({ isActive }) =>
              isActive ? 'sidebar_btn  sidebar_btn_active' : 'sidebar_btn'
            }
          >
            
          </NavLink>
          <NavLink
          
            to="/products"
            className={({ isActive }) =>
              isActive ? 'sidebar_btn  sidebar_btn_active' : 'sidebar_btn'
            }
          >
  
          </NavLink>
          <NavLink
            to="/member_page/membercomment_list/li"
            className={({ isActive }) =>
              isActive ? 'sidebar_btn  sidebar_btn_active' : 'sidebar_btn'
            }
          >
            
          </NavLink>
        
        </div>
    </>
  )
}

export default Sidebar
