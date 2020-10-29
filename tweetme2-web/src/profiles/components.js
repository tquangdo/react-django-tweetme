import React from 'react'

const userLinkStyle = {
    cursor: 'pointer'
}
export function UserLink(props) {
    const { usernameOUserLink } = props
    const handleUserLink = () => {
        window.location.href = `/profiles/${usernameOUserLink}`
    }
    return <span style={userLinkStyle} onClick={handleUserLink}>
        {props.children}
    </span>
}

export function UserDisplay(props) {
    const { userOUserDisplay, isFullName, hideLink } = props
    const nameDisplay = (isFullName) ? `${userOUserDisplay.first_name} ${userOUserDisplay.last_name} ` : null
    return <React.Fragment>
        {nameDisplay}
        {
            (hideLink) ? `@${userOUserDisplay.username}` : <UserLink usernameOUserLink={userOUserDisplay.username}>@{userOUserDisplay.username}</UserLink>
        }
    </React.Fragment>
}

export function UserPicture(props) {
    const { userOUserPicture, hideLink } = props
    const userIdSpan = <span className='mx-1 px-3 py-2 rounded-circle bg-dark text-white'>
        {userOUserPicture.username.substring(0, 4)}
    </span>
    return (hideLink) ? userIdSpan : <UserLink username={userOUserPicture.username}>{userIdSpan}</UserLink>
}