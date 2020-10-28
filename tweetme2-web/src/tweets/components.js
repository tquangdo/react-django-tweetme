import React, { useEffect, useState } from 'react'
import { TweetCreate } from './create'
import { Tweet } from './detail'
import { apiTweetDetail } from './lookup'
import { TweetsList } from './list'
import { FeedList } from './feed'

export function FeedComponent(props) {
    return FeedTweetsComponent(props, FeedList)
}

function FeedTweetsComponent(props, ArgFeedTweetsList) {
    //~~~~~~ STATE
    const [newTweets, setNewTweets] = useState([])
    const canTweet = (props.canTweet === "false") ? false : true
    const handleNewTweet = (newTweet) => {
        let tempNewTweets = [...newTweets]
        tempNewTweets.unshift(newTweet)
        setNewTweets(tempNewTweets)
    }

    return <div className={props.className}>
        {canTweet && <TweetCreate handleNewTweet={handleNewTweet} className='col-12 mb-3' />}
        <ArgFeedTweetsList newTweets={newTweets} {...props} />
    </div>
}

export function TweetsComponent(props) {
    return FeedTweetsComponent(props, TweetsList)
}

export function TweetDetailComponent(props) {
    const { tweetId } = props
    //~~~~~~ STATE
    const [didLookup, setDidLookup] = useState(false)
    const [tweet, setTweet] = useState(null)

    const handleBackendLookup = (response, status) => {
        if (status === 200) {
            setTweet(response)
        } else {
            alert("There was an error finding your tweet.")
        }
    }
    useEffect(() => {
        if (!didLookup) {
            apiTweetDetail(tweetId, handleBackendLookup)
            setDidLookup(true)
        }
    }, [tweetId, didLookup, setDidLookup])

    return tweet === null ? null : <Tweet tweet={tweet} className={props.className} />
}

