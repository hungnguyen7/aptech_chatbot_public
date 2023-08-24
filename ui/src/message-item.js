import React from 'react';
export default class MessageItem extends React.Component{
    shouldComponentUpdate(nextProps, nextState) {
        if(nextProps.message.message===this.props.message.message) return false
        return true;
    }
    render(){
        let date = new Date();
        return(
            <div className={`msg ${this.props.position}-msg`}>
                <div className="msg-img" style={this.props.position === 'right'?{backgroundImage: "url(https://image.flaticon.com/icons/png/512/560/560216.png)"}:{backgroundImage:"url(https://cdn-icons-png.flaticon.com/512/4233/4233830.png)"}}></div>
                <div className='msg-bubble'>
                    <div className='msg-info'>
                        <div className="msg-info-name">{this.props.message.userName}</div>
                        <div className="msg-info-time">{`${date.getHours()}:${('0'+date.getMinutes()).slice(-2)}`}</div>
                    </div>
                    <div className='msg-text'>{this.props.message.message}</div>
                </div>
            </div>
        )
    }
}