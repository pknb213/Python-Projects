import React from 'react';
import {Img, ImgOnly} from "./Image";
import IndyCareLogo from "../../resources/List/img-logo.svg";
import TextLogo from "../../resources/List/logo-indycare.svg";
import ProfileImg from "../../resources/List/img_profile.svg";
import DropdownMenu from "../../resources/List/icon-dropdown-menu.svg";
import UserIcon from "../../resources/List/icon-user.svg";
import CompanyIcon from "../../resources/List/icon-company.svg";
import HomepageLogo from "../../resources/List/neuromeka.svg";
import "./SideNavigator.css";

class SideNavigator extends React.Component {
    // constructor(props) {
    //     super(props);
    //
    // }

    render() {
        return (
            <div className="side_nav">
                <div className="brand_logo">
                    <a href="https://www.neuromeka.com/">
                        <ImgOnly src={IndyCareLogo} alt="indycare_logo"/>
                        <div>
                            <ImgOnly src={TextLogo} alt="indycare_text_logo"/>
                        </div>
                    </a>
                </div>
                <div>
                    <div className="user_info">
                        <Img src={ProfileImg} alt="profile_img"/>
                        <div className="user_name">
                            <span>admin</span>
                        </div>
                        <div className="user_roll">
                            <span>admin</span>
                        </div>
                        <div className="profile_menu">
                            <Img src={DropdownMenu} href="/" alt="dropdown_menu"/>
                        </div>
                    </div>

                    <nav className="nav_menu">
                        <ul className="sub_menu">
                            <li className="sub" hidden>
                                <Img src={UserIcon} alt="User_icon" href="/" text="User"/>
                                <ul>
                                    <li>
                                        <a href="/">User<br/>List</a>
                                    </li>
                                    <li>
                                        <a href="/">User<br/>Register</a>
                                    </li>
                                </ul>
                            </li>
                            <li className="sub">
                                <Img src={CompanyIcon} alt="Company_icon" href="/" text="Robots"/>
                                <ul hidden>
                                    <li>
                                        <a href="/">Company<br/>List</a>
                                    </li>
                                    <li>
                                        <a href="/">Company<br/>Register</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </nav>
                    <div className="side_footer">
                        <Img src={HomepageLogo} href="/" alt="homepage_logo" text="HOME"/>
                    </div>
                </div>
            </div>
        );
    }
}

export default SideNavigator;