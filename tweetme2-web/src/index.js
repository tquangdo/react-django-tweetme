import React from 'react'
import ReactDOM from 'react-dom'
import { FeedComponent, TweetsComponent, TweetDetailComponent } from './tweets'
import { ProfileBadgeComponent } from './profiles'
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
const tweetFeedEl = document.getElementById("tweetme2-feed")
if (tweetFeedEl) {
  ReactDOM.render(
    e(FeedComponent, tweetFeedEl.dataset), tweetFeedEl);
}
const tweetDetailElements = document.querySelectorAll(".tweetme2-detail")
tweetDetailElements.forEach(container => {
  ReactDOM.render(
    e(TweetDetailComponent, container.dataset),
    container)
})
const userProfileBadgeElements = document.querySelectorAll(".tweetme2-profile-badge")
userProfileBadgeElements.forEach(container => {
  ReactDOM.render(
    e(ProfileBadgeComponent, container.dataset),
    container)
})