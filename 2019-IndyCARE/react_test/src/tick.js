import React from 'react';
import './index.css';

class Clock extends React.Component {
    constructor(props) {
        super(props);
        this.state = {date: new Date()}
    }

    // *** Life Cycle Method ***
    // Componet의 출력물이 DOM에 Rendering 된 후에 실행됩니다.
    componentDidMount() {
        this.timerID = setInterval(
            () => this.tick(),
            1000
        );
    }

    componentWillMount() {
        clearInterval(this.timerID);
    }

    /*  State 주의 사항
    1) 직접 State를 수정하지 마세요.
       유일하게 this.state를 지정할 수 있는 공간은 Constructor.
        ex) this.state.comment = "Hello"; is Wrong , this.setState({comment: "Hello"}); is Correct
    2) State Update는 비동기적일 수 있다. (Asynchronism)
       성능을 위해 setState() 호출을 한번에 처리할 수 있기 때문.
       this.props, this.state가 비동기로 업데이트 될 수 있다.
       ex) this.setState({
                counter: this.state.counter + this.props.increment }); is Wrong.
           this.setState((state, props) => ({
                counter: state.counter + props.increment })); is Correct
    3) State Update는 병합됩니다.
       setState()를 호출할 때 React는 제공한 객체를 현재 state로 병합합니다.
       ex) constructor(props){
            super(props);
            this.state = {
                posts : [],
                comments: []
            };
          }

      별도의 setState를 통해 변수를 독립적으로 업데이트 할 수 있습니다.
      ex) componetDidMount({
              fetchposts().then(response => {
                this.setState({
                    posts: response.posts
                });
              });
              fetchComments().then(response => {
                this.setState({
                    comments: response.comments
                };
              });
         }
    */

    tick() {
        this.setState({
            date: new Date()
        });
    }

    render() {
        return (
            <div>
                <h1>It is {this.state.date.toLocaleDateString()}.</h1>
                <h2>{this.state.date.getHours()}:{this.state.date.getMinutes()}:{this.state.date.getSeconds()}</h2>
            </div>
        );
    }
}

function Timer() {
    return (<Clock/>);
}

export default Timer;