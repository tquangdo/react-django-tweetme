import React, { useEffect, useState } from 'react'
import { apiTweetList } from './lookup'
import { Tweet } from './detail'

export function TweetsList(props) {
    //~~~~~~ STATE cha
    const [tweetsInit, setTweetsInit] = useState([]) //init tweet
    const [tweets, setTweets] = useState([])
    const [isTweetsDidSet, setTweetsDidSet] = useState(false)
    useEffect(() => {
        const final = [...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length) {
            setTweets(final) //final tweet
        }
    }, [props.newTweets, tweets, tweetsInit])

    useEffect(() => {
        if (isTweetsDidSet === false) {
            const handleTweetListLookup = (response, status) => {
                if (status === 200) {
                    setTweetsInit(response) //init tweet
                    setTweetsDidSet(true)
                } else {
                    alert("There was an error")
                }
            }
            //nếu ko có "isTweetsDidSet" thì sẽ là vòng lặp vô hạn apiTweetList(handleTweetListLookup) dẫn đến gọi API từ Django vô hạn > console python nhảy liên tục!!!
            apiTweetList(props.username, handleTweetListLookup) //call API giống Axios: "http://localhost:8000/api/tweets/"
        }
    }, [tweetsInit, isTweetsDidSet, setTweetsDidSet, props.username])
    const handleDidRetweet = (newTweet) => {
        const updateTweetsInit = [...tweetsInit]
        updateTweetsInit.unshift(newTweet)
        setTweetsInit(updateTweetsInit)
        const updateFinalTweets = [...tweets]
        updateFinalTweets.unshift(tweets)
        setTweets(updateFinalTweets)
    }
    return tweets.map((item, index) => {
        return <Tweet
            tweet={item}
            didRetweet={handleDidRetweet}
            className='my-5 py-5 border bg-white text-dark'
            key={`${index}-{item.id}`} />
    })
}