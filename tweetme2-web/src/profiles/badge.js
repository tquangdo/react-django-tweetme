import React, { useEffect, useState } from 'react'
import { UserDisplay, UserPicture } from './components'
import { apiProfileDetail, apiProfileFollowToggle } from './lookup'
import { DisplayCount } from './utils'

function ProfileBadge(props) {
    const { user, didFollowToggle, isProfileLoading } = props
    let currentVerb = (user && user.is_following) ? "Unfollow" : "Follow"
    currentVerb = isProfileLoading ? "Loading..." : currentVerb
    const handleFollowToggle = (event) => {
        event.preventDefault()
        if (didFollowToggle && !isProfileLoading) {
            // khi localhost:8000/admin đang là "trangia61" mà index.html(React) cũng là "trangia61" thì KO thể toogle!!!
            didFollowToggle(currentVerb)
        }
    }
    return user ? <div>
        <UserPicture userOUserPicture={user} hideLink />
        <p><UserDisplay userOUserDisplay={user} isFullName hideLink /></p>
        <p>
            <DisplayCount>
                {user.follower_count}
            </DisplayCount> {(user.follower_count === 1 || user.follower_count === 0) ? "follower" : "followers"}
        </p>
        <p>
            <DisplayCount>
                {user.following_count}
            </DisplayCount> following
        </p>
        <p>Location: {user.location}</p>
        <p>Bio: {user.bio}</p>
        <button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>
    </div> : null
}

export function ProfileBadgeComponent(props) {
    const { username } = props
    const [isDidLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
    const [isProfileLoading, setProfileLoading] = useState(false)
    const handleBackendLookup = (response, status) => {
        if (status === 200) {
            setProfile(response)
        }
    }
    useEffect(() => {
        if (!isDidLookup) {
            apiProfileDetail(username, handleBackendLookup)
            setDidLookup(true)
        }
    }, [username, isDidLookup, setDidLookup])
    const handleNewFollow = (actionVerb) => {
        apiProfileFollowToggle(username, actionVerb, (response, status) => {
            if (status === 200) {
                setProfile(response)
            }
            setProfileLoading(false)
        })
        setProfileLoading(true)
    }
    return (!isDidLookup) ? "Loading..." : profile ? <ProfileBadge user={profile} didFollowToggle={handleNewFollow} isProfileLoading={isProfileLoading} /> : null
} 