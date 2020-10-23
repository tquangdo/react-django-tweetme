import React, { useEffect, useState } from 'react'
import {
    loadTweets,
    createTweet
} from '../lookup'

export function TweetsComponent(props) {
    const { className } = props
    const textAreaRef = React.createRef()
    //~~~~~~ STATE cha
    const [newTweets, setNewTweets] = useState([])
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        let tempNewTweets = [...newTweets]
        // change this to a server side call
        // tempNewTweets.unshift({
        //     content: newVal,
        //     likes: 0,
        //     id: 12313
        // })
        createTweet(newVal, (response, status) => {
            if (status === 201) {
                tempNewTweets.unshift(response)
            } else {
                console.log(response)
                alert("An error occured please try again")
            }
        })
        setNewTweets(tempNewTweets)
        textAreaRef.current.value = ''
    }
    return <div className={className}>
        <div className='col-12 mb-3'>
            <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' />
                <button type='submit' className='btn btn-primary my-3'>Tạo tweet</button>
            </form>
        </div>
        <TweetsList newTweetsProps={newTweets} />
    </div>
}

export function TweetsList(props) {
    const { newTweetsProps } = props
    //~~~~~~ STATE cha
    const [tweetsInit, setTweetsInit] = useState([]) //init tweet
    const [tweets, setTweets] = useState([])
    const [isTweetsDidSet, setTweetsDidSet] = useState(false)
    useEffect(() => {
        const final = [...newTweetsProps].concat(tweetsInit)
        if (final.length !== tweets.length) {
            setTweets(final) //final tweet
        }
    }, [newTweetsProps, tweets, tweetsInit])
    useEffect(() => {
        if (!isTweetsDidSet) {
            const myCallback = (response, status) => {
                if (status === 200) {
                    setTweetsInit(response) //init tweet
                    setTweetsDidSet(true)
                } else {
                    alert("There was an error")
                }
            }
            //nếu ko có "isTweetsDidSet" thì sẽ là vòng lặp vô hạn loadTweets(myCallback) dẫn đến gọi API từ Django vô hạn > console python nhảy liên tục!!!
            loadTweets(myCallback) //call API giống Axios: "http://localhost:8000/api/tweets/"
        }
    }, [tweetsInit, isTweetsDidSet])

    return (
        <div className="App">
            {tweets.map((item, index) => {
                return <Tweet tweet={item} className='my-1 py-1 border text-dark' key={index} />
            })}
        </div>
    )
}

export function Tweet(props) {
    const { tweet, className } = props
    const classNameVar = className ? className : 'col-10 mx-auto col-md-6'
    return <div className={classNameVar}>
        <p>{tweet.id} - {tweet.content}</p>
        <div className='btn btn-group'>
            <ActionBtn tweetProps={tweet} actionProps={{ type: "like", display: "Likes" }} />
            <ActionBtn tweetProps={tweet} actionProps={{ type: "unlike", display: "Unlike" }} />
            <ActionBtn tweetProps={tweet} actionProps={{ type: "retweet", display: "Retweet" }} />
        </div>
    </div>
}

export function ActionBtn(props) {
    const { tweetProps, actionProps, className } = props
    //phải là tweetProps.likes & tweetProps.isUserLike
    //vì trên đã khai báo là: const [tweets, setTweets] = useState([])
    //~~~~~~ STATE con
    const [likes, setLikes] = useState(tweetProps.likes ? tweetProps.likes : 0)
    const [isUserLike, setUserLike] = useState(tweetProps.isUserLike ? true : false)
    const classNameVar = className ? className : 'btn btn-primary btn-sm'
    const actionDisplay = actionProps.display ? actionProps.display : 'Action'
    const handleClick = event => {
        event.preventDefault()
        if (actionProps.type === 'like') {
            if (isUserLike) {
                setLikes(likes - 1)
                setUserLike(false)
            } else {
                setLikes(likes + 1)
                setUserLike(true)
            }
        }
    }
    const display = (actionProps.type === 'like') ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={classNameVar} onClick={handleClick}>{display}</button>
}