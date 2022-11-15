import React from 'react';
import {Img} from "./Image";
import ToggleMenu from "../../resources/List/icon-menu.svg";
import SearchIcon from "../../resources/List/icon_search.svg";
import NotiIcon from "../../resources/List/icon_noti.svg";
import LogoutIcon from "../../resources/List/icon_log_out.svg";
import './TopMenu.css'
// <input type=submit> 태그에서 value를 안넣으면 '제출' string이 출력 됨. 추후에 버튼 CSS 입혀서 만들면 될 듯.

class TopMenu extends React.Component {
    // constructor(props) {
    //     super(props);
    //
    // }

    render() {
        return (
            <div className="top_menu">
                <div className="header_toggle">
                    <Img src={ToggleMenu} alt="side_bar_toggle_menu"/>
                </div>

                <div className="item_wrap">
                    <div className="header_item">
                        <ul>
                            <li className="header_search">
                                <label htmlFor="search">
                                    <Img src={SearchIcon} alt="Search_icon"/>
                                    <input type="text" placeholder="search for..." name="search"/>
                                    <input type="submit" className="blind" value=''/>
                                </label>
                            </li>
                            <li>
                                <a href="http://docs.neuromeka.com/">
                                    <button>문의하기</button>
                                </a>
                            </li>
                            <li>
                                <Img src={NotiIcon} alt="Noti_icon"/>
                            </li>
                            <li>
                                <Img href="/" src={LogoutIcon} alt="Logout_icon" text="Log Out"/>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        );
    }
}

export default TopMenu;