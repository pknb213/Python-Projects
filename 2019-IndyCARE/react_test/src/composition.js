import React from 'react'
import './composition.css'

// 합성 Composition Vs 상속 Inheritance

function FancyBorder(props) {
    return (
        <div className={'FancyBorder FancyBorder-' + props.color}>
            {props.children}
        </div>
    );
}

function Dialog(props) {
    return (
        <FancyBorder color="blue">
            <h1 className="Dialog-title">
                {props.title}
            </h1>
            <p className="Dialog_message">
                {props.message}
            </p>
        </FancyBorder>
    )
}

function WelcomeDialog() {
    return (
        <Dialog title="Welcome" message="Fucking Thanks Man !" />
    );
}

function Contacts() {
  return <div className="Contacts" />;
}

function Chat() {
  return <div className="Chat" />;
}

function SplitPane(props) {
    return (
        <div className="SplitPane">
      <div className="SplitPane-left">
        {props.left}
      </div>
      <div className="SplitPane-right">
        {props.right}
      </div>
    </div>
    );
}

function WelcomeSplit(){
    return (
        <SplitPane
            left={<Contacts/>}
            right={<Chat/>}
        />
    );
}

export {WelcomeDialog, WelcomeSplit};

// Class방식 합성
// function Dialog(props) {
//   return (
//     <FancyBorder color="blue">
//       <h1 className="Dialog-title">
//         {props.title}
//       </h1>
//       <p className="Dialog-message">
//         {props.message}
//       </p>
//       {props.children}
//     </FancyBorder>
//   );
// }
//
// class SignUpDialog extends React.Component {
//   constructor(props) {
//     super(props);
//     this.handleChange = this.handleChange.bind(this);
//     this.handleSignUp = this.handleSignUp.bind(this);
//     this.state = {login: ''};
//   }
//
//   render() {
//     return (
//       <Dialog title="Mars Exploration Program"
//               message="How should we refer to you?">
//         <input value={this.state.login}
//                onChange={this.handleChange} />
//
//         <button onClick={this.handleSignUp}>
//           Sign Me Up!
//         </button>
//       </Dialog>
//     );
//   }
//
//   handleChange(e) {
//     this.setState({login: e.target.value});
//   }
//
//   handleSignUp() {
//     alert(`Welcome aboard, ${this.state.login}!`);
//   }
// }