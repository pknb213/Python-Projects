import React from 'react';
import {Img} from './img_card';
import {SText, PText, HText} from './text';
import logo from './neuromeka.svg';
import neuromeka from './group-25.svg';
import arr from './arr.svg';
import cs_icon from './cs_icon.svg';
import forums_icon from './forums_icon.svg';
import docs_icon from './docs_icon.svg';
import mail_icon from './mail_icon.svg';
import './img_card.css'
import './layout.css'

function Layout() {
    return (
        <div className="layout">
            <div className='top'>
                <Img id='logo' src={logo} href={'./#'}/>
            </div>
            <div className='head'>
                <div className='header_title'>
                    <SText id='header1' text='Smart & Connected!'/>
                </div>
                <div className='header_title2'>
                    <Img id='header2' src={neuromeka} />
                </div>
                <div className='header_body'>
                    <SText id='header3' text='협동로봇 기술의 선구자'/>
                </div>
                <div className='header_body2'>
                    <SText id='header4' text='협동로봇 중심의 RasS(Robot as a Service) 플랫폼 비즈니스 생태게, 축적된 로봇 기술을 공유하여 생산성 향상에 기여하고자 합니다.'/>
                </div>
                <div className='header_footer'>
                    <PText id='header5' text='Neuromeka Robot Line Up'/>
                    <Img id='arr' src={arr}/>
                </div>
            </div>
            <div className='middle'>
                <div className='body1'>
                    <HText id='body_title' text='Support'/>
                    <div className='row'>
                        <div className='cs_box'>
                            <Img id='cs_img' src={cs_icon}/>
                            <HText id='cs_title' text='CS'/>
                            <HText id='cs_text' text='send email'/>
                        </div>
                        <div className='col_bar'></div>
                        <div className='forums_box'>
                            <Img id='forums_img' src={forums_icon}/>
                            <PText id='forums_title' text='Forums'/>
                            <PText id='forums_text' text='open forums site'/>
                        </div>
                        <div className='col_bar'></div>
                        <div className='docs_box'>
                            <Img id='docs_img' src={docs_icon}/>
                            <PText id='docs_title' text='Docs'/>
                            <PText id='docs_text' text='neuromeka docs'/>
                        </div>
                    </div>
                </div>
                <div className='row_bar'></div>
                <div className='body2'>
                    <PText id='body_title2' text='Purchase Inquiry'/>
                    <div className='box'>
                        <Img id='mail_img' src={mail_icon}/>
                        <PText id='body_text' text='Sales@neuromeka.com'/>
                    </div>
                    <PText id='body_text2' text='구매를 원하시는 고객님께서는 오른쪽 버튼을 통해 메일을 보내주세요.'/>
                </div>
            </div>
            <div className='row_bar'></div>
            <div className='footer'>
                <SText id='footer_text' text='(주)뉴로메카 /  대표 박종훈 / 사업자 등록번호 132-86-13766 / FAX 070-4791-3103 / 구매문의 : sales@neuromeka.com'/>
                <br/>
                <SText id='footer_text2' text='[본&nbsp;&nbsp;&nbsp;&nbsp;사]  서울시 성동구 연무장5가길 7 성수역 현대테라스타워  W동 15층'/>
                <PText id='footer_text3' text='© 2019 Neuromeka. All rights reserved.'/>
            </div>
        </div>
    );
}

export default Layout;