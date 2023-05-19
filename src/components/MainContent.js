import React from "react";
import style from "./MainContent.module.css";
import DateContainer from "../UI/DateContainer";

const MainContent = () => {
  return (
    <main className={style.main}>
      <DateContainer text="year" />
      <DateContainer text="month" />
      <DateContainer text="luni | marti | miercuri | joi se da la coi | vineri | sambata | duminica" />
    </main>
  );
};

export default MainContent;
