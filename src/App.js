import "./App.css";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState();
  const api_URL = "http://localhost:8080/api/calendar?month=5&year=2023";

  useEffect(() => {
    const dataFetch = async () => {
      const data = await (await fetch(api_URL)).json();

      setData(data);
    };

    dataFetch();
  }, []);

  console.log(data);

  return (
    <div className="App">
      <div className="row">
        <Sidebar />
        <MainContent />
      </div>
      <Footer />
    </div>
  );
}

export default App;
