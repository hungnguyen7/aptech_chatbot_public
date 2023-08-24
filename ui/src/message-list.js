import React from 'react';
import MessageItem from './message-item';
export default class MessageList extends React.Component{
    render(){
        return(
            <div>
                {this.props.messages.map(item=>{
                    return(
                        <MessageItem key={item.id} position={item.userName === this.props.user.name?'right':'left'} message={item}/>
                    )
                })}
            </div>
        )
    }
}