import { Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const ProtectedRoute = () => {
    const { currentUser, loading } = useAuth();

    if (loading) return null;

    return (
        <>
            <Outlet />

        </>
    );
};

export default ProtectedRoute;
