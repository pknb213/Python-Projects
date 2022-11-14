import React from 'react';
import imgIndy7 from '../../resources/Robot/img_productF.png';
import iconCustomer from '../../resources/Robot/icon_server_customer.svg';

function RobotInfoView() {
    return (
        <div className="robot_info">
            <div className="robot_img">
                <img src={imgIndy7} alt="img_indy7"/>
                <div className="model_name">
                    <span>Indy7</span>
                    <button>
                        <img src={iconCustomer} alt="icon_customer"/>
                        <span>고객사정보</span>
                    </button>
                </div>
                <div className="snnumber"/>
            </div>
        </div>
    );
}

export default RobotInfoView;