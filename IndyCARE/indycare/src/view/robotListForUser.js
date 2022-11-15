import React from 'react';
import SideNavigator from "../components/Public/SideNavigator";
import TopMenu from "../components/Public/TopMenu";
import HeaderTitle from "../components/Public/HeaderTitle";
import DataTable from "../components/Public/DataTable";
import "./robotListForUser.css";

const RobotListForUser = () => {
    return (
        <div id="wrapper">
            <SideNavigator/>
            <div className="contents_wrap clear">
                <div className="header_wrap">
                    <div className="header_top">
                        <TopMenu/>
                        <HeaderTitle title="ROBOT LIST" breadcrumb="ROBOT LIST"/>
                    </div>
                    <div className="list_contents_wrap">
                        <DataTable/>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RobotListForUser;