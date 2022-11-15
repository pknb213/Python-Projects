import React from 'react';

function Img(props) {
    return (
        <a href={props.href}>
            <img className={props.id} src={props.src} alt={props.alt} srcSet={props.srcset}/>
            <span>{props.text}</span>
        </a>
    );
}

function ImgOnly(props) {
    return (
        <div>
            <img className={props.id} src={props.src} alt={props.alt} srcSet={props.srcset}/>
            <span>{props.text}</span>
        </div>
    );
}

export {Img, ImgOnly};