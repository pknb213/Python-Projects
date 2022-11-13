import React from 'react';
import './img_card.css'

function ImgCard() {
    return (
        <div className="row">
            <ImgDiv />
            <ImgDiv />
            <ImgDiv />
        </div>
    );
}

function ImgDiv() {
    return (
        <div className="imgDiv">
            <Img />
        </div>
    );
}

function Img(props) {
    return (
        <a href={props.href}>
          <img className={props.id} src={props.src} alt={props.alt} srcSet={props.srcset} />
        </a>
    );
}

export {ImgCard, ImgDiv, Img};

