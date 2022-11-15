import React from 'react';
import './HeaderTitle.css'

class HeaderTitle extends React.Component{
    // constructor(props) {
    //     super(props);
    //
    // }

    render() {
        return (
            <div className="header_title">
                <h1>{this.props.title}</h1>
                <div className="breadcrumb">
                    <ul>
                        <li><a href="/">HOME</a></li>
                        <li className="on"><a href="/">{this.props.breadcrumb}</a></li>
                    </ul>
                </div>
            </div>
        );
    }

}

export default HeaderTitle;