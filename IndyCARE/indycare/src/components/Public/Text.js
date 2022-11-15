import React from 'react'

function SText(props) {
    return (
        <span className={props.id}>
            {props.text}
        </span>
    );
}

function HText(props) {
    return (
        <h3 className={props.id}>
            {props.text}
        </h3>
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