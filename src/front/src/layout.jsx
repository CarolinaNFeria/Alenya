import {
  createBrowserRouter,
  createRoutesFromElements,
  Route
} from "react-router-dom";

import { Navbar } from "./components/Navbar";

import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { Dashboard } from "./pages/Dashboard";
import { AnalyzeBehavior } from "./pages/AnalyzeBehavior";
import { MyAnalyses } from "./pages/MyAnalyses";

const Layout = ({ children }) => {
  return (
    <>
      <Navbar />
      {children}
    </>
  );
};

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route
        path="/"
        element={
          <Layout>
            <Home />
          </Layout>
        }
      />

      <Route
        path="/login"
        element={
          <Layout>
            <Login />
          </Layout>
        }
      />

      <Route
        path="/register"
        element={
          <Layout>
            <Register />
          </Layout>
        }
      />

      <Route
        path="/dashboard"
        element={
          <Layout>
            <Dashboard />
          </Layout>
        }
      />

      <Route
        path="/analyze"
        element={
          <Layout>
            <AnalyzeBehavior />
          </Layout>
        }
      />

      <Route
        path="/my-analyses"
        element={
          <Layout>
            <MyAnalyses />
          </Layout>
        }
      />
    </>
  )
);