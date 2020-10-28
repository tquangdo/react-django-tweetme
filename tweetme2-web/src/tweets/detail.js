import React, { useState } from 'react'
import { ActionBtn } from './buttons'
import {
    UserDisplay,
    UserPicture
} from '../profiles'

export function ParentTweet(props) {
    const { tweetOParentTweet, retweeterOParentTweet } = props
    return tweetOParentTweet.parent ? <Tweet isRetweet retweeter={retweeterOParentTweet} hideActions className={' '} tweet={tweetOParentTweet.parent} /> : null
}
export function Tweet(props) {
    const { tweet, didRetweet, isHidden, className, isRetweet, retweeter } = props
    const { user } = tweet
    const [actionTweet, setActionTweet] = useState(tweet ? tweet : null)
    let classNameVar = className ? className : 'col-10 mx-auto col-md-6'
    classNameVar = (isRetweet) ? `${classNameVar} p-2 border rounded` : classNameVar
    const path = window.location.pathname
    const match = path.match(/tweets\/(?<tweetid>\d+)/)
    const urlTweetId = match ? match.groups.tweetid : -1
    const isDetail = (`${tweet.id}` === `${urlTweetId}`)
    const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/tweets/${tweet.id}`
    }
    const handlePerformAction = (newActionTweet, status) => {
        if (status === 200) {
            setActionTweet(newActionTweet)
        } else if (status === 201) {
            if (didRetweet) {
                didRetweet(newActionTweet)
            }
        }
    }

    return <div className={classNameVar}>
        {isRetweet && <div className='mb-2'>
            <span className='small text-muted'>Retweet via <UserDisplay userOUserDisplay={retweeter} /></span>
        </div>}
        <div className='d-flex'>
            <div className=''>
                <UserPicture userOUserPicture={user} />
            </div>
            <div className='col-11'>
                <div>
                    <p>
                        <UserDisplay isFullName userOUserDisplay={user} />
                    </p>
                    <p>{tweet.content}</p>
                    <ParentTweet tweetOParentTweet={tweet} retweeterOParentTweet={user} />
                </div>
                <div className='btn btn-group px-0'>
                    {actionTweet && !isHidden && <React.Fragment>
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{ type: "like", display: "Likes" }} />
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{ type: "unlike", display: "Unlike" }} />
                        <ActionBtn tweet={actionTweet} didPerformAction={handlePerformAction} action={{ type: "retweet", display: "Retweet" }} />
                    </React.Fragment>
                    }
                    {isDetail ? null : <button className='btn btn-outline-primary btn-sm' onClick={handleLink}>View</button>}
                </div>
            </div>
        </div>
    </div>
}