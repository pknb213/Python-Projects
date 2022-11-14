import React from 'react'
import './text.css'

function SText(props) {
    return (
        <span className={props.id}>
            {props.text}
        </span>
    );
}

function HText(props) {
    return (
        <h1 className={props.id}>
            {props.text}
        </h1>
    );
}

function PText(props) {
    return (
        <p className={props.id}>
            {props.text}
        </p>
    );
}

export {SText, HText, PText}