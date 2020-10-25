import React from 'react'
import ReactDOM from 'react-dom'
import { TweetsComponent } from './tweets'
// import App from './App'

// ReactDOM.render(
//   <App />,
//   document.getElementById('root')
// )
const e = React.createElement
const tweetsEl = document.getElementById("tweetme2")
if (tweetsEl) {
  ReactDOM.render(
    e(TweetsComponent, tweetsEl.dataset), tweetsEl)
}