import { createContext, useState, useEffect } from 'react'
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom'


const AuthContext = createContext()

export default AuthContext;


export const AuthProvider = ({children}) => {
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem(('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null))
    let [user, setUser] = useState(()=> localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null)
    let [error, setError] = useState('')
    let [loading, setLoading] = useState(true)

    const navigate = useNavigate()

    let loginUser = async (e ) => {
        e.preventDefault()
        
        let response = fetch('/api/token',{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({'username':e.target.username.value, 'password': e.target.password.value})
        })
        let data = await response.json()
        if(response.ok){
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
            navigate('/')
        }else{
            setError(data.detail || 'Login failed');
        }
    }

    let logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem('authTokens')
        navigate('/login')
    }

    let updateToken = async ()=> {

        let response = await fetch('/token/refresh/', {
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({'refresh':authTokens?.refresh})
        })

        let data = await response.json()
        
        if (response.status === 200){
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
        }else{
            logoutUser()
        }


        if(loading){
            setLoading(false)
        }
    }

    let contextData = {
        user:user,
        error:error,
        loginUser:loginUser,
        logoutUser: logoutUser
    }

    useEffect(() => {

        if(loading){
            setLoading(false)
        }

        let nineMinutes = 1000 * 60 * 9
        let interval = setInterval(()=> {
            if(authTokens){
                updateToken()
            }
        }, nineMinutes)
        return ()=> clearInterval()

    }), [authTokens, loading]

    return(
        <AuthContext.Provider value={contextData} >
            {loading ? null : children}
        </AuthContext.Provider>
    )
}