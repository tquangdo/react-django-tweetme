import React from 'react'
import ReactDOM from 'react-dom'
import { TweetsComponent, TweetDetailComponent } from './tweets'
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
const tweetDetailElements = document.querySelectorAll(".tweetme2-detail")
tweetDetailElements.forEach(container => {
  ReactDOM.render(
    e(TweetDetailComponent, container.dataset),
    container)
})