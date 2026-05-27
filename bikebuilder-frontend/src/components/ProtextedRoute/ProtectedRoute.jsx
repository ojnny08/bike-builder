import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import NavBar from '../Bars/NavBar'

const ProtectedRoute = ({ children }) => {
    const { currentUser, loading } = useAuth();

    if (loading) return null;
    if (!currentUser) return <Navigate to="/login" replace />;

    return (
        <div>
            <NavBar />
            <main style={{ marginTop: '90px', padding: '32px' }}>
                <Outlet />
            </main>
        </div>
    );
};

export default ProtectedRoute;
