import React from "react";
import "./App.css";

// Components
import Hero from "./components/Hero";
import GetDetailsForm from "./components/GetDetailsForm";

type AppProps = {
  message: string;
};

const App = ({ message }: AppProps): JSX.Element => {
  return (
    <div className="app min-h-screen max-w-screen p-2">
      <Hero />
      <GetDetailsForm />
    </div>
  );
};
export default App;
