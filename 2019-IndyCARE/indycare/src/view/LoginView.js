import React from 'react';
import '../app/App.css';
import {Img} from '../components/Public/Image';
import {HText, PText} from "../components/Public/Text";
import logoIcon from '../resources/img-logo.svg';
import logo from '../resources/logo-indycare.svg';
import Login from "../components/Login/Login";

function LoginView() {
    return (
        <div className="Layout">
            <div className="LoginBox">
                <div className="LeftBox">
                    <div className="LeftContainer">
                        <div className="Title">
                            <Img id='LogoIcon' src={logoIcon}/>
                            <Img id='Logo' src={logo}/>
                        </div>
                        <div className="Explain">
                            <HText text="Login to your account"/>
                        </div>
                        <Login/>
                    </div>
                </div>
                <div className="RightBox">
                    <div className="ImageBox"/>
                    <div className="CopyRight">
                        <PText id="CopyRight" text="COPYRIGHT ⓒ 2019 Neuromeka ALL RIGHTS RESERVED."/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginView;