import React from 'react';
import './App.css';
import $ from 'jquery';
import _map from 'lodash/map';
import io from 'socket.io-client';
import MessageList from './message-list';
import Input from './input';
class App extends React.Component{
  constructor(props){
    super(props);
    this.state={
      messages: [{
        // Message Id
        id: 0,
        message: 'Xin chào, tôi có thể giúp gì cho bạn?',
        //Who sent mes
        userName: 'bot_uttered'
      }],
      user: {
        //Store socketId
        id: '',
        //Store username. E.g: user_uttered
        name: ''
      }
    }
    this.socket = null;
    this.sendNewMessage = this.sendNewMessage.bind(this);
  }

  componentDidMount(){
    //Change your link here
    this.socket = io('ws://localhost:5005');
    this.socket.on('connect', ()=>{
      console.log(this.socket.id + ' connected')
      this.setState({
        user:{
          id: this.socket.id,
          name: 'user_uttered'
        }
      })
      this.socket.emit('session_request',{
        session_id: this.state.user.id
      })
    })
    this.socket.on('bot_uttered', response=>{
      if(response.text)
        this.newMessage(response.text, 'bot_uttered')
    })
  }
  
  newMessage(msg, userOrBot){
    const messages = this.state.messages;
    let ids = _map(messages, 'id'); //Lấy tất cả Id mes bỏ vào một array
    let max = Math.max(...ids);
    messages.push({
      id: max+1,
      message: msg,
      userName: userOrBot
    })
    // https://stackoverflow.com/questions/32783869/what-does-selector0-mean-in-jquery/43133473
    let objMessage = $('.msger-chat');
    // https://javascript.info/size-and-scroll
    if(objMessage[0].scrollHeight - objMessage[0].scrollTop === objMessage[0].clientHeight){
      this.setState({
        messages
      })
      objMessage.animate({ //cuộn tới cuối
        scrollTop: objMessage.prop('scrollHeight')
      }, 300)
    }
    else{
      this.setState({
        messages
      })
      // Kéo xuống dưới cùng khi user gửi tin nhắn
      if(this.state.user.name==='user_uttered'){
        objMessage.animate({
          scrollTop: objMessage.prop('scrollHeight')
        }, 300)
      }
    }
  }

  sendNewMessage(msg){
    if(msg.value){
      this.socket.emit('user_uttered', {
        message: msg.value,
        session_id: this.state.user.id
      });
    this.newMessage(msg.value, 'user_uttered')
      document.getElementById('input-field').value = '';
    }
  }

  render(){
    return(
      <section className='msger'>
        <header className="msger-header">
          <div className="msger-header-title">
              <p className="fas fa-comment-alt">Aptech Chatbot</p>
          </div>
          <div className="msger-header-options">
            <small><i className="fas fa-cog">Can Tho University</i></small>
          </div>
        </header>
        <main className="msger-chat">
            <MessageList user={this.state.user} messages={this.state.messages}/>
        </main>
        <Input sendMessage={this.sendNewMessage}/>
      </section>
    )
  }
}
export default App;
